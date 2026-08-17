# Home Assistant Add-ons

A collection of Home Assistant Supervisor add-ons.

[![Open your Home Assistant instance and show the add app repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fpallemannen%2Fhass-addons)

## Installation

1. Settings -> Add-ons -> Add-on Store -> (menu) -> Repositories
2. Add `https://github.com/pallemannen/hass-addons`
3. Install whichever add-on(s) you want from the store

## Add-ons

### [HA Redirect](ha_redirect/DOCS.md)

HA Redirect
HA Redirect is a general purpose port forwarder for Home Assistant.

It's the perfect tool if you are transitioning from port 8123 to post-2026.8.0 port 80 - This tool can make HA listen to both ports simultaneously, by forwarding port 8123 to localhost port 80.

You can also use it to forward any port anywhere, as long as the source port is not already claimed. You can even forward ports to add-on apps running in HA.

See [ha_redirect/DOCS.md](ha_redirect/DOCS.md) for details and configuration.

### [DDNS Updater](ha_ddns_updater/DOCS.md)

Polls your current public IP and, when it changes, pushes an RFC 2136
dynamic DNS update straight to your own authoritative DNS server - no
third-party dynamic DNS provider involved.

See [ha_ddns_updater/DOCS.md](ha_ddns_updater/DOCS.md) for details and configuration.

## License

MIT - see [LICENSE](LICENSE).
