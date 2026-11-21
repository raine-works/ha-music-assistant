# Actions

The five actions the fork adds, written from [services.yaml](../../custom_components/music_assistant/services.yaml) and [extended.py](../../custom_components/music_assistant/extended.py). The built-in integration's actions are in [Home Assistant's documentation](https://www.home-assistant.io/integrations/music_assistant/).

Two kinds of target:

- **A speaker**: a `media_player` from this integration (target `entity_id`, like any entity action). The action works on the queue the speaker plays from. While a live input parks the queue (the speaker has no active queue), it works on the speaker's own queue, the Music Assistant player id.
- **A Music Assistant server**: no entity. Pass `config_entry_id` to name the server; leave it out when exactly one Music Assistant server is loaded. With several loaded and none named, the action fails with "Name the Music Assistant server (config_entry_id)".

If Music Assistant refuses a command, the action fails with `Music Assistant refused <command>: <reason>`.

## music_assistant.get_queue_items

Target: a speaker. Returns a response (response only: use `response_variable`).

| Field | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `offset` | no | the playing item | Index of the first item to return, 0 or more. |
| `limit` | no | 50 | How many items, 1 to 500. |

Response:

| Key | Description |
| :--- | :--- |
| `current_index` | Index of the playing item (0 if unknown). |
| `total` | Number of items in the queue. |
| `offset` | Index of the first item returned. |
| `items` | The page, in order (below). |
| `source` | What the queue came from (`name`, `uri`, `media_type`, `image`), or `null`. |
| `shuffle` | Whether shuffle is on. |
| `repeat` | The repeat mode as Music Assistant reports it. |
| `dont_stop_the_music` | Whether Don't stop the music is on. |

Each item has `id` (the queue item id), `index`, `name`, `artist` (artists joined with a comma), `album`, `duration` (seconds), `image` (only when a browser can load it, else `null`) and `uri`.

## music_assistant.edit_queue

Target: a speaker. No response.

| Field | Required | Description |
| :--- | :--- | :--- |
| `action` | yes | `play`, `move`, `remove` or `resume`. |
| `item` | for all but `resume` | What the action applies to (below). |
| `shift` | no, default 0 | For `move`: places to move the item, negative for up, -1000 to 1000. |

What `item` is for each action:

- `play`: the queue index to play from.
- `move`: the queue item id (the `id` from `get_queue_items`).
- `remove`: the queue item id or index.
- `resume`: not used. Resumes the queue from where it stopped, after a live input.

An action other than `resume` without an `item` fails with "<action> needs the item".

## music_assistant.set_dont_stop_the_music

Target: a speaker. No response.

| Field | Required | Description |
| :--- | :--- | :--- |
| `enabled` | yes | `true` or `false`. |

## music_assistant.get_podcast_episodes

Target: a Music Assistant server (`config_entry_id`, optional). Returns a response.

| Field | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `config_entry_id` | no | the only server | The Music Assistant config entry. |
| `uri` | yes | | The podcast's URI, `<provider>://podcast/<id>`. Anything else fails with "Not a podcast's URI". |
| `offset` | no | 0 | Episodes to skip. |
| `limit` | no | 50 | How many, 1 to 200. |

Episodes are sorted newest first by release date, else by the provider's own order. Response:

| Key | Description |
| :--- | :--- |
| `total` | Episodes the podcast has. |
| `offset` | Episodes skipped. |
| `episodes` | The page (below). |

Each episode has `uri`, `name`, `released`, `duration` (seconds), `resume` (your resume point, in seconds), `played` (fully played), `description` (show notes as plain text, cut to 280 characters, or `null`) and `image` (or `null`).

## music_assistant.get_party_url

Target: a Music Assistant server (`config_entry_id`, optional). Returns a response.

| Field | Required | Description |
| :--- | :--- | :--- |
| `config_entry_id` | no | The Music Assistant config entry. |

Response: `{ "url": "<guest link>" }`, with `url` `null` while the Party plugin's guest access is off.
