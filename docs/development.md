# Development

## Layout

| Path | What it is |
| :--- | :--- |
| `custom_components/music_assistant/` | The integration: Home Assistant core's at the followed release, plus `extended.py` (the fork's actions) |
| `tests/components/music_assistant/` | Core's tests for it, plus the fork's `test_extended.py` |
| `scripts/sync-upstream.sh` | Brings a Home Assistant release in: see [Following Home Assistant](following-home-assistant.md) |
| `UPSTREAM`, `NOTICE`, `LICENSE` | The followed release, attribution, and Apache 2.0 |
| `hacs.json` | The Marketplace's repository metadata |

## Set up and test

Python 3.14, as the workflows use:

```bash
uv venv --python 3.14 .venv && uv pip install -r requirements-test.txt
.venv/bin/ruff check custom_components
.venv/bin/ruff format --check custom_components
.venv/bin/python -m pytest -q
```

[The Test workflow](../.github/workflows/test.yaml) runs the same three steps on pushes to `master` and on pull requests. [The Validate workflow](../.github/workflows/validate.yaml) runs hassfest and the repository checks of the Home Assistant Marketplace's validation action, weekly too.

Keep the fork's changes small and in `extended.py`: the pure functions there (`queue_page()`, `episode_page()`) shape Music Assistant's answers and are tested without a server.

## Brand icons

`custom_components/music_assistant/brand/icon.png` (256px) and `icon@2x.png` (512px) are Music Assistant's own logo, from Home Assistant's brands (`https://brands.home-assistant.io/music_assistant/icon.png` and `icon@2x.png`). Music Assistant's name and logo are its project's; this fork isn't affiliated with or endorsed by the Music Assistant project or the Open Home Foundation.

## Releasing

Change the manifest's version (a Home Assistant release plus a revision, never 1.0), add a CHANGELOG entry and push to `master`. When the Test workflow passes, the Release workflow publishes `v<version>`. See [Following Home Assistant](following-home-assistant.md).
