"""The fork's own actions: more of Music Assistant than the built-in integration has.

Kept in this one module (and one line in services.py), so each Home Assistant release's
integration merges in with as little conflict as possible.

On a speaker (a Music Assistant player entity):
- get_queue_items: the queue from the playing item (or an offset), a page at a time, with what
  it came from (the playlist or album) and its settings
- edit_queue: play an item, move it, remove it, or resume the queue (after a live input)
- set_dont_stop_the_music: Music Assistant's "Don't stop the music" for the speaker's queue

On a Music Assistant server (its config entry; the only one when there's one):
- get_podcast_episodes: a podcast's episodes, newest first, with the listener's progress
- get_party_url: the Party plugin's guest link (none while guest access is off)

The Party dashboard on a display is the built-in integration's already: each display is a
media player; `media_player.play_media` with content type `dashboard` and id `party` shows it,
`media_player.turn_off` takes it off, and the player's state says what shows.
"""

from html import unescape
import re
from typing import TYPE_CHECKING, Any

import probatio

from homeassistant.components.media_player import DOMAIN as MEDIA_PLAYER_DOMAIN
from homeassistant.const import ATTR_CONFIG_ENTRY_ID
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
    callback,
)
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers import config_validation as cv, service

from .const import DOMAIN
from .helpers import get_music_assistant_client

if TYPE_CHECKING:
    from music_assistant_client import MusicAssistantClient

    from .media_player import MusicAssistantPlayer

SERVICE_GET_QUEUE_ITEMS = "get_queue_items"
SERVICE_EDIT_QUEUE = "edit_queue"
SERVICE_SET_DONT_STOP_THE_MUSIC = "set_dont_stop_the_music"
SERVICE_GET_PODCAST_EPISODES = "get_podcast_episodes"
SERVICE_GET_PARTY_URL = "get_party_url"

QUEUE_EDITS = ("play", "move", "remove", "resume")
PODCAST_URI = re.compile(r"^([A-Za-z0-9_-]+)://podcast/([^/?#]+)$")
DESCRIPTION_MAX = 280


# What the actions answer, shaped from Music Assistant's own (pure, tested) ----------------


def _image(value: Any) -> str | None:
    """An image's path, when a browser can load it (remotely accessible)."""
    if isinstance(value, dict) and value.get("remotely_accessible"):
        return value.get("path")
    return None


def queue_page(queue: dict[str, Any], items: list[Any], offset: int) -> dict[str, Any]:
    """A page of the queue, with its current index, length, source and settings.

    Each item: its id, index, name, artist, album, length, cover and URI.
    """
    source = (queue.get("sources") or [None])[0]
    page = []
    for n, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        media = (
            item.get("media_item") if isinstance(item.get("media_item"), dict) else {}
        )
        page.append(
            {
                "id": item.get("queue_item_id"),
                "index": offset + n,
                "name": media.get("name") or item.get("name"),
                "artist": ", ".join(
                    a.get("name", "") for a in media.get("artists") or [] if a
                ),
                "album": (media.get("album") or {}).get("name"),
                "duration": item.get("duration"),
                "image": _image(item.get("image")),
                "uri": media.get("uri"),
            }
        )
    return {
        "current_index": queue.get("current_index")
        if isinstance(queue.get("current_index"), int)
        else 0,
        "total": queue.get("items") if isinstance(queue.get("items"), int) else 0,
        "offset": offset,
        "items": page,
        "source": {
            "name": source.get("name"),
            "uri": source.get("uri"),
            "media_type": source.get("media_type"),
            "image": _image(source.get("image")),
        }
        if isinstance(source, dict)
        else None,
        "shuffle": bool(queue.get("shuffle_enabled")),
        "repeat": queue.get("repeat_mode"),
        "dont_stop_the_music": bool(queue.get("dont_stop_the_music_enabled")),
    }


def _plain(text: str) -> str:
    """Show notes as text: tags taken out, entities read."""
    return unescape(re.sub(r"<[^>]+>", "", text)).replace("\xa0", " ").strip()


def episode_page(episodes: list[Any], offset: int, limit: int) -> dict[str, Any]:
    """Episodes newest first (by release date, else the provider's own order), a page of them."""
    usable = [e for e in episodes if isinstance(e, dict) and e.get("uri")]

    def key(e: dict[str, Any]) -> str:
        released = (e.get("metadata") or {}).get("release_date") or ""
        return f"{released}|{int(e.get('position') or 0):08d}"

    page = []
    for e in sorted(usable, key=key, reverse=True)[offset : offset + limit]:
        metadata = e.get("metadata") or {}
        image = next(
            (i.get("path") for i in metadata.get("images") or [] if _image(i)), None
        )
        notes = _plain(metadata.get("description") or "")
        if len(notes) > DESCRIPTION_MAX:
            notes = notes[: DESCRIPTION_MAX - 1] + "…"
        page.append(
            {
                "uri": e["uri"],
                "name": e.get("name"),
                "released": metadata.get("release_date"),
                "duration": int(e.get("duration") or 0),
                "resume": round(int(e.get("resume_position_ms") or 0) / 1000),
                "played": e.get("fully_played") is True,
                "description": notes or None,
                "image": image,
            }
        )
    return {"total": len(usable), "offset": offset, "episodes": page}


# On a speaker ---------------------------------------------------------------------------


def _queue_id(entity: MusicAssistantPlayer) -> str:
    """The queue the speaker plays from, else its own (a live input parks the queue)."""
    queue = entity.active_queue
    return queue.queue_id if queue else entity.player_id


async def _command(mass: MusicAssistantClient, command: str, **args: Any) -> Any:
    try:
        return await mass.send_command(command, **args)
    except Exception as err:
        raise HomeAssistantError(f"Music Assistant refused {command}: {err}") from err


async def _get_queue_items(
    entity: MusicAssistantPlayer, call: ServiceCall
) -> ServiceResponse:
    queue_id = _queue_id(entity)
    queue = await _command(entity.mass, "player_queues/get", queue_id=queue_id) or {}
    current = queue.get("current_index") if isinstance(queue, dict) else None
    offset = call.data.get("offset")
    start = offset if offset is not None else current if isinstance(current, int) else 0
    items = await _command(
        entity.mass,
        "player_queues/items",
        queue_id=queue_id,
        limit=call.data["limit"],
        offset=start,
    )
    return queue_page(queue if isinstance(queue, dict) else {}, items or [], start)


async def _edit_queue(entity: MusicAssistantPlayer, call: ServiceCall) -> None:
    queue_id = _queue_id(entity)
    action, item = call.data["action"], call.data.get("item")
    if action != "resume" and item in (None, ""):
        raise ServiceValidationError(f"{action} needs the item")
    if action == "play":
        await _command(
            entity.mass, "player_queues/play_index", queue_id=queue_id, index=item
        )
    elif action == "move":
        await _command(
            entity.mass,
            "player_queues/move_item",
            queue_id=queue_id,
            queue_item_id=item,
            pos_shift=call.data.get("shift", 0),
        )
    elif action == "remove":
        await _command(
            entity.mass,
            "player_queues/delete_item",
            queue_id=queue_id,
            item_id_or_index=item,
        )
    else:
        await _command(entity.mass, "player_queues/resume", queue_id=queue_id)


async def _set_dont_stop_the_music(
    entity: MusicAssistantPlayer, call: ServiceCall
) -> None:
    await _command(
        entity.mass,
        "player_queues/dont_stop_the_music",
        queue_id=_queue_id(entity),
        dont_stop_the_music_enabled=call.data["enabled"],
    )


# On a Music Assistant server ------------------------------------------------------------


def _server(call: ServiceCall) -> MusicAssistantClient:
    """The config entry's client; with none given, the only loaded one."""
    if entry_id := call.data.get(ATTR_CONFIG_ENTRY_ID):
        return get_music_assistant_client(call.hass, entry_id)
    entries = call.hass.config_entries.async_loaded_entries(DOMAIN)
    if len(entries) != 1:
        raise ServiceValidationError(
            "Name the Music Assistant server (config_entry_id)"
        )
    return entries[0].runtime_data.mass


async def _get_podcast_episodes(call: ServiceCall) -> ServiceResponse:
    if not (parts := PODCAST_URI.match(call.data["uri"])):
        raise ServiceValidationError("Not a podcast's URI (<provider>://podcast/<id>)")
    episodes = await _command(
        _server(call),
        "music/podcasts/podcast_episodes",
        item_id=parts.group(2),
        provider_instance_id_or_domain=parts.group(1),
    )
    return episode_page(episodes or [], call.data["offset"], call.data["limit"])


async def _get_party_url(call: ServiceCall) -> ServiceResponse:
    url = await _command(_server(call), "party/url")
    return {"url": url if isinstance(url, str) and url else None}


SERVER = {probatio.Optional(ATTR_CONFIG_ENTRY_ID): cv.string}


@callback
def async_setup_extended_services(hass: HomeAssistant) -> None:
    """Register the fork's actions (from services.async_setup_services)."""
    for name, func, schema, response in (
        (
            SERVICE_GET_QUEUE_ITEMS,
            _get_queue_items,
            {
                probatio.Optional("offset"): probatio.All(
                    probatio.Coerce(int), probatio.Range(min=0)
                ),
                probatio.Optional("limit", default=50): probatio.All(
                    probatio.Coerce(int), probatio.Range(min=1, max=500)
                ),
            },
            SupportsResponse.ONLY,
        ),
        (
            SERVICE_EDIT_QUEUE,
            _edit_queue,
            {
                probatio.Required("action"): probatio.In(QUEUE_EDITS),
                probatio.Optional("item"): probatio.Any(int, cv.string),
                probatio.Optional("shift", default=0): probatio.Coerce(int),
            },
            SupportsResponse.NONE,
        ),
        (
            SERVICE_SET_DONT_STOP_THE_MUSIC,
            _set_dont_stop_the_music,
            {probatio.Required("enabled"): cv.boolean},
            SupportsResponse.NONE,
        ),
    ):
        service.async_register_platform_entity_service(
            hass,
            DOMAIN,
            name,
            entity_domain=MEDIA_PLAYER_DOMAIN,
            schema=schema,
            func=func,
            supports_response=response,
        )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_PODCAST_EPISODES,
        _get_podcast_episodes,
        schema=probatio.Schema(
            {
                **SERVER,
                probatio.Required("uri"): cv.string,
                probatio.Optional("offset", default=0): probatio.All(
                    probatio.Coerce(int), probatio.Range(min=0)
                ),
                probatio.Optional("limit", default=50): probatio.All(
                    probatio.Coerce(int), probatio.Range(min=1, max=200)
                ),
            }
        ),
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_PARTY_URL,
        _get_party_url,
        schema=probatio.Schema(SERVER),
        supports_response=SupportsResponse.ONLY,
    )
