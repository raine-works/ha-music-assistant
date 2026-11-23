# Following Home Assistant

Each release of this fork follows a Home Assistant release: the built-in Music Assistant integration's code and tests at that release, with this fork's changes on top.

## Versions

A version is Home Assistant's release plus a revision: `2026.11.2.2` is Home Assistant 2026.11.2's integration, second revision. The first three numbers match Home Assistant; the last counts this fork's own releases on it. The version is in the manifest (`custom_components/music_assistant/manifest.json`), the followed release is in [UPSTREAM](../UPSTREAM), and `homeassistant` in [hacs.json](../hacs.json) is the minimum Home Assistant version.

Use the release matching your Home Assistant's: the built-in integration changes with Home Assistant, and so does this.

## What stays upstream's

The fork's own code is in one module, [extended.py](../custom_components/music_assistant/extended.py), registered by one line in `services.py`, plus its entries in `services.yaml` and `strings.json`, and the manifest's own fields. The rest is the built-in integration unchanged, so each release merges in with as little conflict as possible. Don't change upstream-synced code beyond what the fork needs.

## Syncing to a new release

[scripts/sync-upstream.sh](../scripts/sync-upstream.sh) brings a Home Assistant release in as a diff to review and merge:

```bash
scripts/sync-upstream.sh 2026.12.0
```

It clones Home Assistant core at that tag (sparse), copies core's integration over `custom_components/music_assistant` (leaving `translations` alone) and its tests over `tests/components/music_assistant` (keeping the fork's `test_extended*.py`), copies the test helpers the tests need, and points the tests' imports at `custom_components`. Git then shows what core changed beside what the fork changed.

Then:

1. Put the fork's changes back in (the line in `services.py`, the entries in `services.yaml` and `strings.json`, the manifest's own fields).
2. Update the translations: `pip install homeassistant==<release>`, then copy its `components/music_assistant/translations`.
3. Set `UPSTREAM`, the manifest's `version`, `homeassistant` in `hacs.json` and `requirements-test.txt`'s `pytest-homeassistant-custom-component` to the release, and move the hassfest image's digest in [validate.yaml](../.github/workflows/validate.yaml) on to the current one, so hassfest checks against that release's rules.
4. Run the lint and tests, and add a [CHANGELOG.md](../CHANGELOG.md) entry.

## Releases

[The Release workflow](../.github/workflows/release.yaml) runs after the Test workflow passes on `master`. If the manifest's version has no release yet, it publishes one (tag `v<version>`) with generated notes. A push that doesn't change the manifest's version publishes nothing, so a documentation change doesn't cut a release.
