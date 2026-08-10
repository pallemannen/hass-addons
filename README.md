# Home Assistant Add-ons

A collection of Home Assistant Supervisor add-ons.

## Installation

1. Settings -> Add-ons -> Add-on Store -> (menu) -> Repositories
2. Add `https://github.com/pallemannen/hass-addons`
3. Install whichever add-on(s) you want from the store

## Add-ons

### [HA Redirect](ha_redirect/DOCS.md)

Minimal Home Assistant add-on that redirects requests on common web ports
(80, 8080, 443, 8443, 8123) to your actual Home Assistant instance -
picking an internal or external destination automatically based on where
the request came from. Perfect if you want to transition to HA 2026.8.0
port 80, but without giving up port 8123.

## License

MIT - see [LICENSE](LICENSE).
