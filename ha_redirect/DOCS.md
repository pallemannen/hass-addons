# HA Redirect

HA Redirect is a general purpose port forwarder for Home Assistant.

It's the perfect tool if you are transitioning from port 8123 to 
post-2026.8.0 port 80 - This tool can make HA listen to both ports 
simultaneously, by forwarding port 8123 to localhost port 80.

You can also use it to forward any port anywhere, as long as the
source port is not already claimed.

## Installation

1. Add repo https://github.com/pallemannen/hass-addons to Home Assistant
   -> Settings -> Apps -> "Install app" -> three-dot menu -> Repositories.
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

## HA add-on app forwarding

If an HA add-on app is listening to a port, you can forward traffic to that 
port. 

The apps are usually docker containers that are not exposed to network 
traffic from the surrounding network. That means that there is no way to 
directly access the app from the rest of your network, the only way is going
through the HA web-based GUI, either by clicking on the designated sidepanel
icon (for apps in ingress mode), or by clicking "Open web UI" on the app page.

But with a port forward, we can bypass that requirement, and get direct access
to the app independent of HA restarts, and without the HA graphical framework
around the app. For this, you need two things:

- The slug of the app. If you click on the sidepanel or "Open web UI" button,
  the URL in the address field of your browser will give you a string similar
  to "a0d7b954_grafana". Replace the underscore with a dash, and you have the
  hostname of the app. Put "a0d7b954-grafana" into the `Target Host` field.
  Note: That slug is tied to the repo the app was installed fromm, and is
  the same in all HA installations, so any HA server running an app from 
  the same repo should be able to use the same slug.
  
- The port to forward to. This can be trickier. A good guess is the default port
  of the upstream app that was packeged. Grafana is listening to its usual port
  3000. MariaDB is 3306. Mosquitto is 1883. Etc.
  If it's not a well-known app with a default port, or if the packager changed
  to some other port, you can always check the logs. Most apps log a message
  of what port they are listening to.
  And if you still can't find the port, you can always run a port scan. Download
  the "Terminal & SSH" app from the official app store, and run this at the prompt:
  ```bash
  target=a0d7b954-grafana
  seq 1 65535 | xargs -P 200 -I{} bash -c \
  'timeout 0.3 bash -c "echo >/dev/tcp/'"$target"'/{}" 2>/dev/null && echo "{} open"' 2>/dev/null
  ```
  It will take a while, but it will result in a list of all TCP ports the app is
  listening to. Try them one by one until you find what you are looking for.

Once you have the hostname and the port, put them into the `Target Host` and
`Target Port` fields, choose a port to listen on (it can be the same as the 
target port) and try it out.

**NOTE! This can be a security hole!** For some apps, HA is handling the
authentication, and the app will be wide open without any protection.
Only do this if you know what you are doing.

## No HTTP awareness

This add-on relays raw bytes - no HTTP parsing, no SSL termination, no
scheme redirects. Whatever protocol you connect with passes through
unchanged. If you use the wrong scheme for what Home Assistant actually
expects on that port, the connection will simply fail rather than redirect
you - that's expected, not a bug.

## No UDP forwarding

This app is TCP only.

## License

MIT - see [LICENSE](LICENSE).

