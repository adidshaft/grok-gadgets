# ADR 006 — Always-on gateway and a stable device address

**Date:** 12 October 2026  
**Status:** Accepted by the owner on 12 October 2026. On 12–13 October the owner's Mac and OLED kit passed name, address-change and restart checks ([record](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/verification/always-on-2026-10-13.md)). Linux systemd is not yet tested on a real host.  
**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)  
**Issues:** hub [#212](https://github.com/adidshaft/grok-gadgets/issues/212), [#22](https://github.com/adidshaft/grok-gadgets/issues/22) (HUB-SERVICE-001), gateway [#109](https://github.com/adidshaft/grok-gadgets-gateway/issues/109) (GW-SVC-001), gateway [#110](https://github.com/adidshaft/grok-gadgets-gateway/issues/110) (GW-LAN-002), ESP32 [#99](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/99) (ESP-MDNS-001)

## Context

Phase 4 ([ADR 005](005-wifi-device-route.md)) put the ESP32-S3 OLED kit on home Wi-Fi.
Two gaps remain before the kit works without someone at the Mac:

1. **The gateway runs only in a terminal.** After a reboot or logout, nobody starts
   `serve --lan-listen`, so the board waits at **Gateway...**.
2. **The board stores the Mac's IP address.** The LAN certificate and the provisioning
   settings name one IPv4 address. On 12 October 2026 the Mac's address moved from `.42`
   to `.252` when it changed Wi-Fi band. The old certificate and board settings stopped
   working until both were redone. A router reservation avoids this, but not every router
   offers one, and a stranger following the guide may not know to set it.

The listener rules from ADR 005 stay: one private address, TLS from the local CA, private
peers only, per-device tokens, never forwarded or tunnelled.

## Decision

### 1. Gateway as a per-user background service

- New command group `grok-gadgets-gateway service install|uninstall|status|logs`.
- **macOS:** a launchd **user agent** (`~/Library/LaunchAgents/`), `RunAtLoad` and
  `KeepAlive`. It starts at login. **Linux:** a systemd **user** unit
  (`~/.config/systemd/user/`), `Restart=on-failure`; the docs explain `loginctl enable-linger`
  for start at boot without a login.
- No root, no system-wide files. The unit runs the absolute gateway executable from the
  install, with the same flags the person passes to `service install` (for example
  `--lan-listen`). Logs and the request log go to a per-user log folder that `service logs`
  prints.
- `install` refuses to run while another gateway holds the ports, and prints how to stop it.
  `uninstall` stops the service and removes the unit file. Config, CA and tokens stay.
- Installing or activating the service on the owner's Mac needs the owner's yes.

### 2. A stable name instead of a raw address

- `lan-cert NAME` accepts a `.local` mDNS name as well as an IPv4 address. The certificate's
  subject alternative names hold the name; the CA and its pinning do not change.
- `serve --lan-listen NAME[:PORT]` resolves the name to this computer's current private
  address when it starts. It applies the ADR 005 address rules to the result and re-checks the
  address periodically. When the address changes, it closes the LAN listener and binds the new
  address. The service restarts it if it exits.
- `wifi-provision --lan NAME[:PORT]` stores the name. The firmware resolves it with mDNS
  (`ESPmDNS`, part of the pinned Arduino-ESP32 2.0.17 core) before each connection and verifies
  the TLS certificate against the name. A stored IPv4 address keeps working as today.
- Docs use a generic example such as `my-mac.local`; never the owner's hostname.

## Consequences

- After a reboot, the kit reaches **Online** with nobody at the Mac, once the person is logged
  in (macOS) or lingering is enabled (Linux).
- An address change no longer breaks the setup; a router reservation becomes optional.
- mDNS works only on the local network segment. Networks that block multicast (some guest or
  mesh setups) still need the IPv4 form; troubleshooting covers this.
- The service is a long-running process on the person's computer; `service status` and
  `service logs` must make it easy to see and stop.

## Not in scope

Native Grok Bot tool calls through a tunnel (#4, #154), setup without USB (ESP32 #72) and
OAuth (gateway #71) stay parked. Nothing is exposed beyond the home network.

## Acceptance

- Gateway: `service` commands with tests on macOS (launchd plist) and Linux (systemd unit
  text); `lan-cert`, `serve --lan-listen` and `wifi-provision` accept a `.local` name; tests.
- ESP32: provisioning stores a name; the firmware resolves it with mDNS and verifies TLS by
  name; host tests.
- Owner check on the kit: reboot the Mac and log in. The board shows **Online** without a manual
  `serve`. Then change the Mac's address, for example by switching Wi-Fi band. The board returns
  to **Online** without new certificates or provisioning.
