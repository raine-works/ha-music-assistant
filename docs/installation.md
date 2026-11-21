# Installation

This integration replaces Home Assistant's built-in Music Assistant integration in place. It keeps the domain `music_assistant`, so your config entry, speakers, entity ids, history and every `music_assistant.*` action in your automations stay as they are.

You need a Home Assistant that can install custom repositories from the Home Assistant Marketplace, and a Music Assistant server. Setting up Music Assistant itself is covered by [Home Assistant's own Music Assistant documentation](https://www.home-assistant.io/integrations/music_assistant/).

## Install

[![Open your Home Assistant instance and open this repository in the Home Assistant Marketplace.](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=raine-works&repository=ha-music-assistant&category=integration)

1. Open the Home Assistant Marketplace (Settings → Marketplace, or the button above).
2. If **Music Assistant (raine-works)** isn't listed, add `https://github.com/raine-works/ha-music-assistant` as a custom repository, with type **Integration**.
3. Download it. Choose the release that matches your Home Assistant's (see below).
4. Restart Home Assistant.

Home Assistant logs that the built-in Music Assistant integration is overridden by a custom one. That's this integration.

Already set up Music Assistant? Nothing else to do. New to it? Add the Music Assistant integration as usual (Settings → Devices & services).

## Match the release to Home Assistant

A release's version follows a Home Assistant release: `2026.11.2.2` is Home Assistant 2026.11.2's integration with this fork's second revision on top. The built-in integration changes with Home Assistant, and so does this one, so download the release whose first three numbers are your Home Assistant's version. [hacs.json](../hacs.json) names the minimum Home Assistant version (`homeassistant`), and [UPSTREAM](../UPSTREAM) names the release the code follows. See [Following Home Assistant](following-home-assistant.md).

## Updating

When you update Home Assistant, update this integration to the release for the new version before or right after, then restart. The releases are listed on the [releases page](https://github.com/raine-works/ha-music-assistant/releases), and [CHANGELOG.md](../CHANGELOG.md) says what each changed.

## Going back to the built-in integration

Remove the custom integration in the Marketplace and restart Home Assistant. Home Assistant goes back to the built-in one, with your config entry intact. The fork's five actions then no longer exist, so automations that call them will fail.
