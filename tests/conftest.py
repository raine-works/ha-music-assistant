"""The fork's tests are Home Assistant core's own (tests/components/music_assistant), in core's
layout so each release's tests copy straight over; this loads the integration from
custom_components/ over the built-in one."""

import pytest


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Load custom_components/music_assistant, not homeassistant.components.music_assistant."""
