# HA Redirect

Redirects requests on common web ports to your actual Home Assistant instance.

## Configuration

### Option: `target_host`
The hostname to redirect all incoming requests to - typically your Home
Assistant's real external or internal hostname.

### Option: `target_port`
The port your real Home Assistant instance is actually listening on.

### Option: `use_ssl`
When enabled, redirects use `https://` instead of `http://`. **Make sure SSL
is actually configured on the destination (Settings -> System -> Network)
before enabling this** - otherwise you'll redirect users to a connection that
doesn't exist.

## Port collisions - read before enabling ports

This add-on can listen on five common ports: 80, 8080, 443, 8443, and 8123.
Each is independently enabled, disabled, or remapped in the **Network**
section below Options.

**The port your real Home Assistant is running on (`target_port`) cannot
also be enabled here.** If Home Assistant already has that port bound on
this host, this add-on will fail to start with a port-conflict error. This
is not a rare edge case:

- Home Assistant's traditional default port is **8123** - one of this
  add-on's five listener options.
- As of Home Assistant 2026.8.0, new installations default to **port 80**
  instead - also one of this add-on's five listener options.

Before starting this add-on, disable whichever Network-section port matches
your actual Home Assistant port, regardless of what `target_port` is set to.
The failure is not silent - the add-on simply won't start, and the error
will be visible in its log and in the Supervisor's add-on list.

## Installation

1. Set `target_host` to your Home Assistant's real hostname
2. Set `target_port` to match
3. Enable `use_ssl` only if HTTPS is actually configured on that destination
4. In the Network section, disable the port matching `target_port`
5. Start the add-on
