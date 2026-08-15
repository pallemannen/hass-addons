# DDNS Updater

DDNS Updater polls your current public IP and, when it changes, pushes an
RFC 2136 dynamic DNS update straight to your own authoritative DNS server -
BIND, Knot, PowerDNS, Windows DNS Server, or anything else that speaks
RFC 2136 - no third-party dynamic DNS provider involved.

## Installation

1. Add repo https://github.com/pallemannen/hass-addons to Home Assistant
   -> Settings -> Apps -> "Install app" -> three-dot menu -> Repositories.
2. Search for DDNS Updater in the App store and click "Install".

## Prerequisites

Your DNS server needs a TSIG key and an update policy scoped to the one
record this add-on is allowed to touch - do not grant it broad zone-write
access. The wire protocol (RFC 2136 + TSIG) is the same everywhere, but the
server-side config syntax to set this up differs by software. Here's a BIND
example:

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

Generate the key with `tsig-keygen -a hmac-sha256 ddns-key` (ships with
BIND). Other RFC 2136-capable servers (Knot's `acl`/`zone.acl`, PowerDNS's
API-based dynamic updates, Windows DNS Server's secure dynamic updates,
etc.) achieve the same record-scoped restriction with their own syntax -
check your server's docs for the equivalent of BIND's `update-policy`.

If your zone has a hand-maintained SOA serial (e.g. `YYYYMMDDXX`), keep the
dynamically-updated record in its own delegated subzone like the example
above rather than making your whole zone dynamic - dynamic-update
auto-increment only touches the SOA of the zone actually being written, and
most nameservers (BIND included) flatten `$INCLUDE`/split-file structure on
the next journal sync of a dynamic zone. Point your real hostname at it
with a static `CNAME` in your normal, hand-managed zone:

```
home.example.com. CNAME home.dyn.example.com.
```

## Configuration

### `tsig_algorithm` / `tsig_keyname` / `tsig_secret`
Must match the TSIG key configured on your DNS server exactly - algorithm
(e.g. `hmac-sha256`), key name, and the base64 secret.

### `fqdn`
The record this add-on updates, e.g. `home.dyn.example.com`. A trailing dot
isn't required - one is added automatically if missing.

### `zone`
The zone that record lives in, as configured in your DNS server's update
policy (e.g. `dyn.example.com`).

### `dns_server`
Your DNS server's IP address (a static/public one, since this add-on talks
to it directly over port 53 - no NAT or DNS lookup involved for this field).
Works with any RFC 2136-capable server, not just BIND.

### `ip_echo_url`
An HTTP endpoint that echoes back the caller's public IP as plain text.
Point this at your own service if you have one, or any public "what's my
IP" endpoint. Must be reachable from wherever this add-on runs.

### `poll_interval`
How often, in seconds, to check for an IP change (minimum 60). No update is
sent unless the IP has actually changed since the last check.

## Security note

The record's TTL is fixed at 300s in the update itself, regardless of your
zone's default `$TTL`, so IP changes propagate quickly without needing a
zone-wide TTL change.

## License

MIT - see [LICENSE](LICENSE).
