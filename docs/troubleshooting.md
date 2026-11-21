# Troubleshooting

## Home Assistant says the built-in integration is overridden

Expected. Home Assistant logs that the built-in Music Assistant integration is overridden by a custom one when this integration is installed. It's how the replacement works: nothing is wrong.

## An action isn't there

- Restart Home Assistant after installing; the actions register when the integration loads.
- Check you installed this integration and not only the built-in one (Settings → Devices & services → Music Assistant, or the Marketplace's installed list).
- Download the release for your Home Assistant's version: see [Installation](installation.md).

## Errors from the actions

These are the messages the actions raise (see the [actions reference](reference/actions.md)):

| Message | Cause |
| :--- | :--- |
| `Music Assistant refused <command>: <reason>` | Music Assistant's server refused the command. The reason is its own: check the Music Assistant server's log. |
| `<action> needs the item` | `edit_queue` with `play`, `move` or `remove` and no `item`. |
| `Name the Music Assistant server (config_entry_id)` | `get_podcast_episodes` or `get_party_url` with more than one Music Assistant server loaded and no `config_entry_id`. |
| `Not a podcast's URI (<provider>://podcast/<id>)` | `get_podcast_episodes`'s `uri` isn't a podcast's. |

## get_party_url returns no url

`url` is `null` while the Party plugin's guest access is off. Turn it on in Music Assistant's Party plugin settings.

## get_queue_items is empty or wrong after a live input

While a live input plays as the speaker's source, the speaker has no active queue, so the action reads the speaker's own queue, which is parked. Use `edit_queue` with `resume` to continue it.

## The tests fail

See [Development](development.md). Home Assistant's own tests for the integration run on every change, on `pytest-homeassistant-custom-component` at the release in `requirements-test.txt`; a mismatch between that pin and `UPSTREAM` is the usual cause after a sync.

Something else? Open an issue on [GitHub](https://github.com/raine-works/ha-music-assistant/issues).
