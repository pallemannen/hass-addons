# HA Redirect

Blind TCP port forwarder that runs on the host's own network (no Docker
port-mapping layer) and relays traffic from any number of listener ports
straight to Home Assistant's real port on the same machine.

Because this add-on shares the host's network directly, there's no
separate "destination host" to configure - it's always this machine.

## Configuration

### `target_port`
The port Home Assistant actually binds to on this host - its real port.
8123 is the traditional default; new installations from Home Assistant
2026.8.0 onward default to port 80 instead.

### `listen_ports`
Comma-separated list of ports to listen on, each forwarded to
`target_port` (e.g. `80,8080,443,8443,8123`). Any number of ports, any
values - not limited to a fixed set.

If a listed port matches `target_port`, it's automatically skipped (a line
is logged noting this, not a hard failure) - forwarding a port to itself
would be pointless, and if Home Assistant already has that port bound,
trying to also bind it here would fail anyway.

Invalid entries (anything that isn't a valid port number 1-65535) are
silently skipped before ever being used. If a valid port is already bound
by something else on this host, only that one listener fails - it's logged
so you can see why, but every other configured port keeps working
normally. The add-on itself does not fail to start over one bad port.

## No HTTP awareness

This add-on relays raw bytes - no HTTP parsing, no SSL termination, no
scheme redirects. Whatever protocol you connect with passes through
unchanged. If you use the wrong scheme for what Home Assistant actually
expects on that port, the connection will simply fail rather than redirect
you - that's expected, not a bug.

## Installation

1. Set `target_port` to Home Assistant's real port
2. Set `listen_ports` to whatever ports you want reachable (comma-separated)
3. Start the add-on
