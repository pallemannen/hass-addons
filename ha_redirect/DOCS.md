# HA Redirect

Redirects requests on common web ports to your actual Home Assistant
instance - automatically choosing an internal or external destination based
on whether the request came from your LAN.

## How internal/external detection works

This add-on inspects the client's source IP. Requests from private ranges
(10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, loopback, IPv6 ULA) are treated
as internal; everything else is treated as external. This only works
reliably if this add-on receives the true client IP directly - if you put
another reverse proxy in front of it, the source IP it sees will be the
proxy's, not the real client's, and detection will break unless you also
configure that proxy to preserve/pass through the original address.

If you have the same hostname internally and externally, just set all four
host/port options to the same values.

## Configuration

### `internal_target_host` / `internal_target_port`
Where LAN clients get redirected. `internal_target_port` should be the port
Home Assistant actually binds to *locally* on this host - not a port
forwarding target.

### `external_target_host` / `external_target_port`
Where non-LAN clients get redirected. `external_target_port` is the port
people use to reach you from *outside* your firewall, after any port
forwarding (e.g. 443) - this is frequently different from the internal
port, and does not bind anything locally.

### `use_ssl`
When enabled, redirects use `https://` instead of `http://` (applies to
both internal and external targets). **Make sure SSL is actually configured
on the destination (Settings -> System -> Network) before enabling this** -
otherwise you'll redirect users to a connection that doesn't exist.

## Port collisions - read before enabling ports

This add-on can listen on five common ports: 80, 8080, 443, 8443, and 8123.
Each row in the **Network** section below Options is an editable port-number
field, not a checkbox - to disable a specific listener entirely, clear that
field so it's blank rather than entering a port number.

**`internal_target_port` cannot also be enabled here.** That's the port
Home Assistant actually binds to on this host directly. If Home Assistant
already has that port bound, this add-on will fail to start with a
port-conflict error. This is not a rare edge case:

- Home Assistant's traditional default port is **8123** - one of this
  add-on's five listener options.
- As of Home Assistant 2026.8.0, new installations default to **port 80**
  instead - also one of this add-on's five listener options.

`external_target_port` generally does *not* need to be disabled here - it's
the port people use from outside your firewall after port forwarding, which
your router translates, not something bound locally on this host, so it
typically doesn't collide with anything.

Before starting this add-on, clear (blank out) whichever Network-section
port field matches your `internal_target_port`. The failure is not silent -
the add-on simply won't start, and the error will be visible in its log and
in the Supervisor's add-on list.

## Installation

1. Set `internal_target_host`/`internal_target_port` to where LAN clients
   should land, matching where Home Assistant actually binds locally
2. Set `external_target_host`/`external_target_port` to where everyone else
   should land (can match step 1 if you don't need a distinction)
3. Enable `use_ssl` only if HTTPS is actually configured on those destinations
4. In the Network section, clear (leave blank) whichever port field matches
   your `internal_target_port`
5. Start the add-on
