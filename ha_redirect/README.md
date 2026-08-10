# HA Redirect

Minimal Home Assistant add-on that redirects requests on common web ports
(80, 8080, 443, 8443, 8123) to your actual Home Assistant instance -
picking an internal or external destination automatically based on where
the request came from. Perfect if you want to transition to HA 2026.8.0
port 80, but without giving up port 8123.

See [DOCS.md](DOCS.md) for full configuration details, including an
important note about port collisions with Home Assistant itself.
