#!/usr/bin/env bash
# Bring Home Assistant core's Music Assistant integration and tests at a release into this fork, as
# a diff to review and merge: `scripts/sync-upstream.sh 2026.12.0`. It copies core's integration
# over custom_components/music_assistant and its tests over tests/components/music_assistant (with
# the imports pointed at custom_components), leaving git to show what core changed beside what this
# fork changed. Then: resolve the fork's own changes back in, run the tests, set UPSTREAM, the
# manifest's version and requirements-test.txt's pytest-homeassistant to the release.
set -euo pipefail
tag="${1:?usage: scripts/sync-upstream.sh <home-assistant release, e.g. 2026.12.0>}"
root="$(cd "$(dirname "$0")/.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

git clone -q --depth 1 --branch "$tag" --filter=blob:none --sparse https://github.com/home-assistant/core "$work/core"
git -C "$work/core" sparse-checkout set homeassistant/components/music_assistant tests/components/music_assistant \
  tests/components/tts tests/components/hassio
core="$work/core"

rsync -a --delete --exclude translations "$core/homeassistant/components/music_assistant/" "$root/custom_components/music_assistant/"
rsync -a --delete "$core/tests/components/music_assistant/" "$root/tests/components/music_assistant/"
cp "$core/tests/components/conftest.py" "$root/tests/components/conftest.py"
cp "$core/tests/components/tts/common.py" "$root/tests/components/tts/common.py"
cp "$core/tests/components/hassio/__init__.py" "$core/tests/components/hassio/common.py" "$root/tests/components/hassio/"
perl -pi -e 's/homeassistant\.components\.music_assistant/custom_components.music_assistant/g' \
  "$root"/tests/components/music_assistant/*.py

echo "Copied core $tag. Now: git diff, put the fork's changes back, update the version and translations"
echo "(pip install homeassistant==$tag, then copy its components/music_assistant/translations), run the tests."
