# DDNS Updater

DDNS Updater polls your current public IP and, when it changes, pushes an
RFC 2136 dynamic DNS update straight to your own authoritative BIND server -
no third-party dynamic DNS provider involved.

## Installation

1. Add repo https://github.com/pallemannen/hass-addons to Home Assistant
   -> Settings -> Apps -> "Install app" -> three-dot menu -> Repositories.
2. Search for DDNS Updater in the App store and click "Install".

## Prerequisites

Your BIND server needs a TSIG key and an `update-policy` scoped to the one
record this add-on is allowed to touch - do not grant it broad zone-write
access. For example:

```
key "ddns-key" {
    algorithm hmac-sha256;
    secret "<base64-secret-from-tsig-keygen>";
};

zone "dyn.example.com" {
    type master;
    file "/usr/local/etc/namedb/master/dyn.example.com.db";
    update-policy { grant ddns-key name home.dyn.example.com. A; };
};
```

Generate the key with `tsig-keygen -a hmac-sha256 ddns-key`, which ships
with BIND itself.

If your zone has a hand-maintained SOA serial (e.g. `YYYYMMDDXX`), keep the
dynamically-updated record in its own delegated subzone like the example
above rather than making your whole zone dynamic - dynamic-update
auto-increment only touches the SOA of the zone actually being written, and
BIND flattens `$INCLUDE` structure on the next journal sync of a dynamic
zone. Point your real hostname at it with a static `CNAME` in your normal,
hand-managed zone:

```
home.example.com. CNAME home.dyn.example.com.
```

## Configuration

### `tsig_algorithm` / `tsig_keyname` / `tsig_secret`
Must match the TSIG key configured on your BIND server exactly - algorithm
(e.g. `hmac-sha256`), key name, and the base64 secret from `tsig-keygen`.

### `fqdn`
The record this add-on updates, fully qualified with a trailing dot (e.g.
`home.dyn.example.com.`).

### `zone`
The zone that record lives in, as configured in the `update-policy` on
BIND (e.g. `dyn.example.com`).

### `bind_server`
Your BIND server's IP address (a static/public one, since this add-on talks
to it directly over port 53 - no NAT or DNS lookup involved for this field).

### `ip_echo_url`
An HTTP endpoint that echoes back the caller's public IP as plain text.
Point this at your own service if you have one, or any public "what's my
IP" endpoint. Must be reachable from wherever this add-on runs.

### `poll_interval`
How often, in seconds, to check for an IP change (minimum 60). No update is
sent to BIND unless the IP has actually changed since the last check.

## Security note

The record's TTL is fixed at 300s in the update itself, regardless of your
zone's default `$TTL`, so IP changes propagate quickly without needing a
zone-wide TTL change.

## License

MIT - see [LICENSE](LICENSE).
