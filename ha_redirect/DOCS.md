# HA Redirect

HA Redirect is a general purpose port forwarder for Home Assistant.

It's the perfect tool if you are transitioning from port 8123 to 
post-2026.8.0 port 80 - This tool can make HA listen to both ports 
simultaneously, by forwarding port 8123 to localhost port 80.

You can also use it to forward any port anywhere, as long as the
source port is not already claimed.

## Installation

1. Add repo https://github.com/pallemannen/hass-addons to Home Assistant
   -> Settings -> Apps -> Install app -> three-dot menu -> Repositories.
2. Search for HA Redirect in the App store and click "Install".
 
## Configuration

### `forwarders`
A list of forwarding rules. Each has:
- **`target_host`** - where to relay traffic to. `localhost` for Home
  Assistant itself (the traditional use case), or any other reachable
  hostname/IP to relay elsewhere.
- **`target_port`** - the port on `target_host` that actually serves the
  traffic.
- **`source_ports`** - comma-separated list of ports to listen on for this
  rule, each forwarded to `target_host:target_port`.

Add or remove rules with the +/- controls in the add-on's Configuration tab.
Each rule is independent of the other ones.

If a listen port matches its own rule's `target_port` on `localhost`/
`127.0.0.1`, it's skipped (forwarding a port to itself is pointless, and if
Home Assistant already has that port bound, binding it here would fail
anyway).

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
