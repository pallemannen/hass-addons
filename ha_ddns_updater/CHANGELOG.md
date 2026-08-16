# Changelog

## 1.1.0
- Removed the `zone` option. `nsupdate` auto-detects the zone via an SOA
  query, so it no longer needs to be configured separately - one less
  field to keep in sync with your DNS server.

## 1.0.2
- New icons
  
## 1.0.1
- Added icons
  
## 1.0.0
- Initial release: polls a configurable IP-echo endpoint, and pushes an
  RFC2136/TSIG dynamic DNS update to a configurable DNS server only when
  the public IP has actually changed. All connection details (TSIG key,
  target record/zone, DNS server, IP-echo URL, poll interval) are
  configurable options.
