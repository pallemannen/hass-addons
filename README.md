# Home Assistant Add-ons

A collection of Home Assistant Supervisor add-ons.

## Installation

1. Settings -> Add-ons -> Add-on Store -> (menu) -> Repositories
2. Add `https://github.com/pallemannen/hass-addons`
3. Install whichever add-on(s) you want from the store

## Add-ons

### [HA Redirect](ha_redirect/DOCS.md)

A blind TCP port forwarder - listens on common web ports (80, 8080, 443,
8443, 8123) and relays all traffic straight to your real Home Assistant
address. Perfect if you want HA post 2026.8.0 to listen to both port 80 
and 8123. See [ha_redirect/DOCS.md](ha_redirect/DOCS.md) for configuration,
including an important note about port collisions with Home Assistant
itself.

## License

MIT - see [LICENSE](LICENSE).
