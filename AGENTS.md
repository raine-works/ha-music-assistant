# Agent guidance for ha-music-assistant

## Raineworks base rules

This repository follows Raineworks' base rules, in [`.raineworks/base.md`](.raineworks/base.md): read them before
changing anything. They're a copy of `base.md` in `raine-works/agents`, kept current by its sync: change them there,
not here. Where this file is more specific, it wins.

@.raineworks/base.md

## This repository

A fork of Home Assistant core's built-in Music Assistant integration, with more of Music Assistant in it. It keeps the
domain `music_assistant`, so it replaces the built-in integration in place. Each release follows a Home Assistant
release: core's code and tests at that release, with the fork's changes on top. Docs are in [docs/](docs/README.md);
read [Following Home Assistant](docs/following-home-assistant.md) before touching upstream-synced code.

### Layout

- `custom_components/music_assistant/`: core's integration at the followed release (named in `UPSTREAM`), plus
  `extended.py`, the fork's own actions, registered by one line in `services.py` and entries in `services.yaml` and
  `strings.json`.
- `tests/components/music_assistant/`: core's tests for it, plus the fork's `test_extended.py`. The other
  `tests/components/*` files are helpers copied from core.
- `scripts/sync-upstream.sh <release>`: brings a Home Assistant release in as a diff (it overwrites the integration
  and its tests; the fork's changes are then put back by hand).
- `NOTICE`, `LICENSE`: the code is Home Assistant's, under Apache 2.0, and keeps its attribution.

### Rules the code follows

- **Keep the fork's changes small and in `extended.py`**; don't change upstream-synced code beyond what the fork
  needs, so each release merges with as little conflict as possible. The pure functions there (`queue_page()`,
  `episode_page()`) are tested without a server.
- The code is written to Home Assistant core's Ruff settings (`pyproject.toml`, core's at 2026.11.2: docstrings,
  Google convention, import order within sections, `probatio` rather than `voluptuous`). It uses relative imports
  within the integration, as core does.
- Music Assistant's name and logo are its project's: keep the not-affiliated notes in the README and docs.

### Checks and releases

- Python 3.14: `uv venv --python 3.14 .venv && uv pip install -r requirements-test.txt`, then `ruff check
  custom_components`, `ruff format --check custom_components` and `python -m pytest -q`
  ([docs/development.md](docs/development.md)). CI (`test.yaml`, the workflow named `Test`) runs the same;
  `validate.yaml` runs hassfest and HACS validation, weekly too.
- **A release is a version bump:** set `version` in `custom_components/music_assistant/manifest.json` (the followed
  Home Assistant release plus a revision, like `2026.11.2.3`, never 1.0), add a `CHANGELOG.md` entry, and merge to
  `master`. `release.yaml` then publishes `v<version>` once `Test` passes; a push that doesn't change the version
  releases nothing.
- **Dependency exception:** `manifest.json` requires `music-assistant-client>=1.6.0`, a range, on purpose. Home
  Assistant's own requirements already pin that package, and hassfest fails an exact `==` pin of one ("pins a package
  Home Assistant depends on"), so a minimum is the only form that passes `validate.yaml`. Raise the minimum with the
  followed release.
- Moving to a new Home Assistant release also sets `UPSTREAM`, `homeassistant` in `hacs.json` and the
  `pytest-homeassistant` pin in `requirements-test.txt` ([Following Home Assistant](docs/following-home-assistant.md)).
  The hassfest and HACS images in `validate.yaml` are moved weekly by Image pins (`image-pins.yml`), by pull request.
