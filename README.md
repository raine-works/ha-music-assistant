<p align="center">
  <img src="custom_components/music_assistant/brand/icon@2x.png" alt="Music Assistant (raine-works)" width="128">
</p>

# Music Assistant for Home Assistant (raine-works)

Home Assistant's own [Music Assistant](https://music-assistant.io) integration, with more of Music
Assistant in it: the whole queue (not just what's playing and next) with edits, podcast episodes,
the Party link and the Party dashboard on your TVs.

It's a fork of the built-in integration and keeps its domain (`music_assistant`), so it **replaces
it in place**: your config entry, speakers, entity ids, history and every `music_assistant.*`
action in your automations stay as they are, and the new actions are added beside them. Remove it
and Home Assistant goes back to the built-in one.

[![Home Assistant Marketplace](https://img.shields.io/badge/Home_Assistant-Marketplace-41BDF5.svg?style=for-the-badge)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=raine-works&repository=ha-music-assistant&category=integration)
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey.svg?style=for-the-badge)](LICENSE)

## What it adds

Actions (see [CHANGELOG.md](CHANGELOG.md) for each release):

| Action | What it does |
| --- | --- |
| `music_assistant.get_queue_items` | A speaker's whole queue, a page at a time from the playing item (or an `offset`), each item's name, artist, album, length, cover and URI, with what the queue came from and its shuffle, repeat and Don't stop the music. The built-in `get_queue` has only the current and next item. |
| `music_assistant.edit_queue` | `play`, `move` (by `shift` places), `remove` an item, or `resume` the queue after a live input. |
| `music_assistant.set_dont_stop_the_music` | Turns Don't stop the music on or off for a speaker's queue. |
| `music_assistant.get_podcast_episodes` | A podcast's episodes by its URI, newest first, with your progress (resume point, played) and short show notes. |
| `music_assistant.get_party_url` | The Party plugin's guest link (none while guest access is off). |

They use the integration's own connection to Music Assistant: no token to keep in `secrets.yaml`.

The Party dashboard on a TV is the built-in integration's already: each display Music Assistant
can cast to is a media player; `media_player.play_media` with content type `dashboard` and id
`party` shows it, and `media_player.turn_off` takes it off.

## Installation

[![Open your Home Assistant instance and open this repository in the Home Assistant Marketplace.](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=raine-works&repository=ha-music-assistant&category=integration)

1. Open the Home Assistant Marketplace (Settings → Marketplace, or the button above), add
   `https://github.com/raine-works/ha-music-assistant` as a custom repository (type Integration) if
   **Music Assistant (raine-works)** isn't listed, and download it.
2. Restart Home Assistant. Home Assistant logs that the built-in Music Assistant integration is
   overridden by a custom one; that's this.

Already set up Music Assistant? Nothing else to do. New to it? Add the Music Assistant integration
as usual (Settings → Devices & services). Details: [docs/installation.md](docs/installation.md).

## Documentation

| Guide | |
| :--- | :--- |
| [Installation](docs/installation.md) | Replacing the built-in integration, matching the release to Home Assistant, going back |
| [What it adds](docs/what-it-adds.md) | The five actions and the Party dashboard |
| [Actions](docs/reference/actions.md) | Every added action: target, fields and response |
| [Following Home Assistant](docs/following-home-assistant.md) | Versions, syncing, releases |
| [Troubleshooting](docs/troubleshooting.md) | Common messages and fixes |
| [Development](docs/development.md) | Tests, lint, brand icons, releasing |

## Following Home Assistant

Each release follows a Home Assistant release (`UPSTREAM`, and the manifest's version): the
built-in integration's code and tests at that release, with this fork's changes on top. Home
Assistant's own tests run on every change (`pytest`, on `pytest-homeassistant` at that release).
`scripts/sync-upstream.sh <release>` brings a newer release in as a diff to merge.

Use the release matching your Home Assistant's: the built-in integration changes with Home
Assistant, and so does this.

## License

Apache 2.0, as Home Assistant's: see [LICENSE](LICENSE) and [NOTICE](NOTICE).
