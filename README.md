# Music Assistant for Home Assistant (raine-works)

Home Assistant's own [Music Assistant](https://music-assistant.io) integration, with more of Music
Assistant in it: the whole queue (not just what's playing and next) with edits, podcast episodes,
the Party link and the Party dashboard on your TVs.

It's a fork of the built-in integration and keeps its domain (`music_assistant`), so it **replaces
it in place**: your config entry, speakers, entity ids, history and every `music_assistant.*`
action in your automations stay as they are, and the new actions are added beside them. Remove it
and Home Assistant goes back to the built-in one.

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey.svg?style=for-the-badge)](LICENSE)

## What it adds

Coming in the next releases (see [CHANGELOG.md](CHANGELOG.md)):

- **The queue:** every item from the playing one (`get_queue_items`), and edits: play an item, move
  it, remove it, resume the queue after a live input (`edit_queue`)
- **Podcast episodes:** a podcast's episodes, newest first, with your progress
- **Party:** Music Assistant's Party guest link, and its Party dashboard shown on (or taken off) your
  TVs

## Installation

1. In HACS, add `https://github.com/raine-works/ha-music-assistant` as a custom repository
   (Integration), then install **Music Assistant (raine-works)**.
2. Restart Home Assistant. Home Assistant logs that the built-in Music Assistant integration is
   overridden by a custom one; that's this.

Already set up Music Assistant? Nothing else to do. New to it? Add the Music Assistant integration
as usual (Settings → Devices & services).

## Following Home Assistant

Each release follows a Home Assistant release (`UPSTREAM`, and the manifest's version): the
built-in integration's code and tests at that release, with this fork's changes on top. Home
Assistant's own tests run on every change (`pytest`, on `pytest-homeassistant` at that release).
`scripts/sync-upstream.sh <release>` brings a newer release in as a diff to merge.

Use the release matching your Home Assistant's: the built-in integration changes with Home
Assistant, and so does this.

## License

Apache 2.0, as Home Assistant's: see [LICENSE](LICENSE) and [NOTICE](NOTICE).
