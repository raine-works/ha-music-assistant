# Changelog

## 2026.11.2.4

- The manifest pins `music-assistant-client==1.6.0` (the version Home Assistant 2026.11.2 pins) instead of a
  minimum, and the test requirements are pinned.

## 2026.11.2.3

- The icon is Music Assistant's own (from Home Assistant's brands), with a note that this fork
  isn't affiliated with the Music Assistant project. The README has the Buy Me a Coffee button.

## 2026.11.2.2

- Passes Home Assistant's and HACS's validation: the manifest's keys sorted, a minimum
  music-assistant-client version (Home Assistant pins it itself), brand icons.

## 2026.11.2.1

Home Assistant 2026.11.2's integration, plus (extended.py; the built-in integration's code is
otherwise unchanged, but for one line registering them):

- `music_assistant.get_queue_items`: a speaker's whole queue, a page at a time from the playing
  item (or an offset), with what it came from (the playlist or album) and its shuffle, repeat
  and Don't stop the music
- `music_assistant.edit_queue`: play an item, move it, remove it, or resume the queue after a live
  input
- `music_assistant.set_dont_stop_the_music`: on or off for a speaker's queue
- `music_assistant.get_podcast_episodes`: a podcast's episodes, newest first, with the listener's
  progress and short show notes
- `music_assistant.get_party_url`: the Party plugin's guest link

The Party dashboard on a display needs nothing new: the built-in integration's display media
players show it (`media_player.play_media`, content type `dashboard`, id `party`) and take it
off (`media_player.turn_off`).

## 2026.11.2

- Home Assistant's built-in Music Assistant integration at 2026.11.2, unchanged, as a custom
  integration (its translations compiled in; a manifest version), with its tests.
