# Changelog

## 1.0.0
- Initial release: blind TCP port forward to Home Assistant, running on
  the local server. Configurable destination port plus a
  comma-separated list of listen ports of any length - invalid entries and
  any listen port matching the destination port are automatically skipped,
  and one port failing to bind (e.g. already in use) doesn't affect the
  others.
