"""The fork's own actions (extended.py): the whole queue, its edits, podcasts, the Party link.

Not one of Home Assistant's tests: scripts/sync-upstream.sh leaves this file alone.
"""

from unittest.mock import MagicMock, call

import pytest

from custom_components.music_assistant.const import DOMAIN
from custom_components.music_assistant.extended import episode_page, queue_page
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError

from .common import setup_integration_from_fixtures

PLAYER = "media_player.test_player_1"
PLAYER_ID = "00:00:00:00:00:01"

QUEUE = {
    "current_index": 3,
    "items": 40,
    "shuffle_enabled": True,
    "repeat_mode": "off",
    "dont_stop_the_music_enabled": True,
    "sources": [
        {
            "name": "Road Trip",
            "uri": "spotify://playlist/abc",
            "media_type": "playlist",
            "image": {"path": "https://img/rt.jpg", "remotely_accessible": True},
        }
    ],
}
ITEMS = [
    {
        "queue_item_id": "q4",
        "name": "fallback",
        "duration": 201,
        "image": {"path": "/local/cover.jpg", "remotely_accessible": False},
        "media_item": {
            "name": "Song",
            "uri": "spotify://track/1",
            "artists": [{"name": "A"}, {"name": "B"}],
            "album": {"name": "Album"},
        },
    }
]


def test_a_queue_page() -> None:
    """Each item as the dashboards show it; a cover only when a browser can load it."""
    assert queue_page(QUEUE, ITEMS, 3) == {
        "current_index": 3,
        "total": 40,
        "offset": 3,
        "items": [
            {
                "id": "q4",
                "index": 3,
                "name": "Song",
                "artist": "A, B",
                "album": "Album",
                "duration": 201,
                "image": None,
                "uri": "spotify://track/1",
            }
        ],
        "source": {
            "name": "Road Trip",
            "uri": "spotify://playlist/abc",
            "media_type": "playlist",
            "image": "https://img/rt.jpg",
        },
        "shuffle": True,
        "repeat": "off",
        "dont_stop_the_music": True,
    }
    assert queue_page({}, [], 0)["source"] is None


def test_an_episode_page() -> None:
    """Newest first, a page of them, the show notes as short plain text."""
    episodes = [
        {"uri": "p://e/1", "name": "Old", "position": 1, "metadata": {"release_date": "2026-01-01"}},
        {
            "uri": "p://e/2",
            "name": "New",
            "position": 2,
            "duration": 3600,
            "resume_position_ms": 61400,
            "fully_played": False,
            "metadata": {
                "release_date": "2026-11-20",
                "description": "<p>Hi &amp; welcome" + " x" * 200 + "</p>",
                "images": [{"path": "https://img/e2.jpg", "remotely_accessible": True}],
            },
        },
        {"name": "No URI"},
    ]
    page = episode_page(episodes, 0, 1)
    assert page["total"] == 2 and page["offset"] == 0
    (newest,) = page["episodes"]
    assert newest["name"] == "New" and newest["resume"] == 61 and newest["played"] is False
    assert newest["image"] == "https://img/e2.jpg"
    assert newest["description"].startswith("Hi & welcome") and len(newest["description"]) == 280
    assert [e["name"] for e in episode_page(episodes, 1, 5)["episodes"]] == ["Old"]


async def test_get_queue_items(hass: HomeAssistant, music_assistant_client: MagicMock) -> None:
    """From the playing item, by default, on the speaker's queue."""
    await setup_integration_from_fixtures(hass, music_assistant_client)
    music_assistant_client.send_command.side_effect = [QUEUE, ITEMS]
    response = await hass.services.async_call(
        DOMAIN,
        "get_queue_items",
        {ATTR_ENTITY_ID: PLAYER, "limit": 10},
        blocking=True,
        return_response=True,
    )
    queue_id = music_assistant_client.send_command.call_args_list[0].kwargs["queue_id"]
    assert music_assistant_client.send_command.call_args_list[1] == call(
        "player_queues/items", queue_id=queue_id, limit=10, offset=3
    )
    assert response[PLAYER]["items"][0]["name"] == "Song"


@pytest.mark.parametrize(
    ("data", "command", "args"),
    [
        ({"action": "play", "item": 5}, "player_queues/play_index", {"index": 5}),
        (
            {"action": "move", "item": "q4", "shift": -2},
            "player_queues/move_item",
            {"queue_item_id": "q4", "pos_shift": -2},
        ),
        ({"action": "remove", "item": "q4"}, "player_queues/delete_item", {"item_id_or_index": "q4"}),
        ({"action": "resume"}, "player_queues/resume", {}),
    ],
)
async def test_edit_queue(
    hass: HomeAssistant, music_assistant_client: MagicMock, data, command, args
) -> None:
    """Each edit as Music Assistant's own command."""
    await setup_integration_from_fixtures(hass, music_assistant_client)
    await hass.services.async_call(DOMAIN, "edit_queue", {ATTR_ENTITY_ID: PLAYER, **data}, blocking=True)
    sent = music_assistant_client.send_command.call_args
    assert sent.args == (command,)
    assert {k: v for k, v in sent.kwargs.items() if k != "queue_id"} == args


async def test_an_edit_needs_its_item(
    hass: HomeAssistant, music_assistant_client: MagicMock
) -> None:
    await setup_integration_from_fixtures(hass, music_assistant_client)
    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN, "edit_queue", {ATTR_ENTITY_ID: PLAYER, "action": "remove"}, blocking=True
        )


async def test_dont_stop_the_music(hass: HomeAssistant, music_assistant_client: MagicMock) -> None:
    await setup_integration_from_fixtures(hass, music_assistant_client)
    await hass.services.async_call(
        DOMAIN, "set_dont_stop_the_music", {ATTR_ENTITY_ID: PLAYER, "enabled": False}, blocking=True
    )
    sent = music_assistant_client.send_command.call_args
    assert sent.args == ("player_queues/dont_stop_the_music",)
    assert sent.kwargs["dont_stop_the_music_enabled"] is False


async def test_podcast_episodes_and_the_party_link(
    hass: HomeAssistant, music_assistant_client: MagicMock
) -> None:
    """On the only server when none is named."""
    await setup_integration_from_fixtures(hass, music_assistant_client)
    music_assistant_client.send_command.side_effect = [
        [{"uri": "spotify://podcast_episode/9", "name": "Ep"}],
        "https://party.example/join",
    ]
    episodes = await hass.services.async_call(
        DOMAIN,
        "get_podcast_episodes",
        {"uri": "spotify://podcast/abc"},
        blocking=True,
        return_response=True,
    )
    assert music_assistant_client.send_command.call_args_list[0] == call(
        "music/podcasts/podcast_episodes",
        item_id="abc",
        provider_instance_id_or_domain="spotify",
    )
    assert episodes["episodes"][0]["name"] == "Ep"
    link = await hass.services.async_call(DOMAIN, "get_party_url", {}, blocking=True, return_response=True)
    assert link == {"url": "https://party.example/join"}
    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            DOMAIN, "get_podcast_episodes", {"uri": "spotify://album/abc"}, blocking=True, return_response=True
        )
