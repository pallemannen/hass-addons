# Home Assistant Add-ons

A collection of Home Assistant Supervisor add-ons.

## Installation

1. Settings -> Add-ons -> Add-on Store -> (menu) -> Repositories
2. Add `https://github.com/pallemannen/hass-addons`
3. Install whichever add-on(s) you want from the store

## Add-ons

### [HA Redirect](ha_redirect/DOCS.md)

Listens on common web ports (80, 8080, 443, 8443, 8123) and issues an HTTP
301 redirect to your actual Home Assistant instance - internal or external
clients get routed to different destinations automatically. See
[ha_redirect/DOCS.md](ha_redirect/DOCS.md) for configuration, including an
important note about port collisions with Home Assistant itself.

## License

MIT - see [LICENSE](LICENSE).
