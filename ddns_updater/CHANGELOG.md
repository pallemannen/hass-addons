# Changelog

## 1.0.0
- Initial release: polls a configurable IP-echo endpoint, and pushes an
  RFC2136/TSIG dynamic DNS update to a configurable BIND server only when
  the public IP has actually changed. All connection details (TSIG key,
  target record/zone, BIND server, IP-echo URL, poll interval) are
  configurable options.
