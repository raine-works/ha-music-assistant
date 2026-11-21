# What it adds

The fork is the built-in Music Assistant integration's code at a Home Assistant release, plus five actions. Everything the built-in integration does (media players, library browsing, `music_assistant.play_media`, `search`, `get_library`, `get_queue`, `transfer_queue` and the rest) is unchanged: see [Home Assistant's Music Assistant documentation](https://www.home-assistant.io/integrations/music_assistant/).

The new actions live in one module, [extended.py](../custom_components/music_assistant/extended.py), registered by one line in `services.py`, so the built-in code stays as it is. They use the integration's own connection to Music Assistant, so there's no token to keep in `secrets.yaml`.

| Action | Target | What it does |
| :--- | :--- | :--- |
| `music_assistant.get_queue_items` | A speaker | The whole queue, a page at a time, with what it came from and its shuffle, repeat and Don't stop the music. The built-in `get_queue` has only the current and next item. |
| `music_assistant.edit_queue` | A speaker | Play an item, move it, remove it, or resume the queue after a live input. |
| `music_assistant.set_dont_stop_the_music` | A speaker | Turns Don't stop the music on or off for the speaker's queue. |
| `music_assistant.get_podcast_episodes` | A Music Assistant server | A podcast's episodes by URI, newest first, with your progress and short show notes. |
| `music_assistant.get_party_url` | A Music Assistant server | The Party plugin's guest link. |

Each is described field by field in the [actions reference](reference/actions.md).

## The Party dashboard on a TV

Showing the Party dashboard on a display needs nothing new: the built-in integration already makes each display Music Assistant can cast to a media player. Call `media_player.play_media` on it with content type `dashboard` and media id `party` to show it, and `media_player.turn_off` to take it off. The player's state says what is showing. Use `music_assistant.get_party_url` to get the guest link for a QR code.

## Example

```yaml
action: music_assistant.get_queue_items
target:
  entity_id: media_player.kitchen
data:
  limit: 10
response_variable: queue
```
