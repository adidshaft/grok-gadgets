# ADR 005 — Secure Wi-Fi route from an ESP32 device to the gateway

**Date:** 12 October 2026  
**Status:** Accepted on 12 October 2026. Physical acceptance passed the same day ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md)).  
**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)  
**Issues:** [#168](https://github.com/adidshaft/grok-gadgets/issues/168), gateway [#79](https://github.com/adidshaft/grok-gadgets-gateway/issues/79) (GW-LAN-001), ESP32 [#5](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/5) (ESP-005)

## Context

The ESP32-S3 OLED kit passed physical acceptance over USB on 12 October 2026
([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/dev/docs/verification/oled-kit-2026-10-12.md)).
Over USB, the `usb-bridge` on the Mac adds the device token and forwards protocol 0.1.0
frames to the loopback device listener on `127.0.0.1:8765`. The gateway has no network
listener, and the firmware has no Wi-Fi code.

Phase 4 goal: the kit runs from a USB charger, joins the owner's home Wi-Fi and reaches the
gateway on the owner's Mac securely. USB must keep working. The listener must never be
reachable from the internet.

## Decision

### 1. LAN device listener (gateway)

- `serve --lan-listen ADDRESS[:PORT]` starts a second device listener. The default port is
  **8767**. Without the flag, there is no LAN listener.
- `ADDRESS` is one IPv4 address in a private range (`10.0.0.0/8`, `172.16.0.0/12`,
  `192.168.0.0/16`). The gateway refuses `0.0.0.0`, `::`, loopback, link-local, shared
  (`100.64.0.0/10`) and public addresses. Binding fails if the address is not on this Mac.
- Peer filter: the gateway closes a connection from a source address outside the private
  ranges before the TLS handshake and logs `lan_peer_rejected`. With no port forwarding,
  the router already blocks the internet. The filter is a second barrier.
- The listener uses the same `DeviceServer` code as loopback: the same frames, the same
  hello, polling, acknowledgements, events, timeouts and error codes. Only the socket
  differs.

### 2. TLS from a local CA

- `init` creates a local certificate authority in the config directory:
  `lan/ca.pem` (public) and `lan/ca.key` (mode 0600, never leaves the Mac). An existing
  installation gets the CA on its next `init`.
- `lan-cert ADDRESS` issues the listener certificate for that one address. The address is
  in the subject CN, in an IP SAN and in a DNS SAN. The device's TLS library (mbedTLS 2.28
  in Arduino-ESP32 2.0.17) matches the host string against CN and DNS names only.
- Keys: ECDSA P-256. TLS 1.2 or newer, ECDHE with AES-GCM. No client certificates: the
  device token is the device credential.
- `lan-ca show` prints the CA path and SHA-256 fingerprint. `lan-ca rotate` replaces the
  CA and every device must be provisioned again.
- **Pinning.** The device trusts only the CA certificate that provisioning wrote to its NVS.
  It has no public CA bundle and never skips verification. The CA is not compiled into the
  image, because each owner's CA differs and a per-owner image would make the published
  build checksum useless. The pin is set over the USB cable, a channel the owner controls.
- The firmware has no clock, and this mbedTLS build does not check certificate dates
  (`MBEDTLS_HAVE_TIME_DATE` is off). Certificate expiry is not a control on the device.
  Rotation replaces the CA.

### 3. Authentication and revocation

- The Wi-Fi hello carries the device's existing enroll token, as a TCP device does today.
  The protocol schema already allows it.
- The gateway re-reads the credential file on every frame. The firmware polls every 100 ms,
  so `revoke` closes a live LAN session on its next frame, within about a second. A new
  connection gets `revoked` at hello.
- After `unauthorized` or `revoked`, the firmware waits 60 seconds between attempts and
  shows "Token rejected". `enroll --rotate` issues a new token. The owner provisions the
  new token over USB.

### 4. Limits

| Limit | Value |
| --- | --- |
| LAN sessions | 8, separate from loopback |
| Connections waiting for a hello | 4; the oldest is closed first |
| TLS handshake time | 5 s |
| New connections per source address | 20 a minute; more are closed and logged |
| Frames per session | 30 a second; more get `busy` |
| Frame size, hello and idle timeouts | Same as loopback |

The request log records LAN connects, disconnects, rejected peers, TLS failures and rate
limits with the source address. It never records a token.

### 5. Provisioning over USB serial

- A separate firmware build, `esp32s3-oled-kit-wifi`. The USB build `esp32s3-oled-kit` is
  unchanged.
- In the Wi-Fi build the serial port is a console, not a protocol port. It accepts one-line
  JSON commands: `provision`, `status` and `factory_reset`. Replies never contain a stored
  value.
- `grok-gadgets-gateway wifi-provision PORT --device ID --lan ADDRESS[:PORT]` reads the
  device token from the credential file and the CA from the config directory. It prompts
  for the Wi-Fi name and password. The password prompt does not echo. The tool sends one
  `provision` line and prints only the device's result. Nothing is written to a file, log or
  shell history.
- The firmware stores the Wi-Fi name, password, token, gateway address and CA in NVS
  namespace `grok-wifi`, then restarts.
- **Factory reset:** the `factory_reset` command, or holding BOOT for 10 seconds, erases
  the namespace and restarts. The device then shows "Not provisioned". The owner also runs
  `revoke` for that device. `esptool erase_flash` is the last resort.
- **Known limit:** flash encryption is off. Anyone who holds the board can read NVS and
  learn the Wi-Fi password and the device token. If a board is lost, revoke its token and
  change the Wi-Fi password. Flash encryption burns eFuses and cannot be undone, so it is
  out of scope.

### 6. Firmware behaviour

- Wi-Fi station mode with automatic reconnect. TLS client with the pinned CA. Capped
  backoff: 0.5 s doubling to 5 s for connection loss, 60 s after a rejected token.
- Offline state: the OLED's top row shows `WiFi…`, `Gateway…`, `Online`, `TLS rejected`,
  `Token rejected` or `Not provisioned`. Rows 2–5 keep showing the last text. `display.clear`
  blanks the text rows only.
- The session layer is unchanged except for a link interface: open the link before hello,
  close it on a session reset, add the token to the hello. A command is never replayed into
  a new session.

### 7. Same protocol

No frame changes. Protocol stays 0.1.0. The USB bridge and the Linux SDK are unaffected.

## Design note: can a device event wake or notify Grok Bot?

Sources: the Grok Bot docs pages
[Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations),
[Settings and notifications](https://docs.x.ai/grok-bot/settings-and-notifications) and
[Connect to private networks](https://docs.x.ai/grok-bot/private-networks), read on
12 October 2026.

- **Routines** run on a schedule, at least five minutes apart, or after an event from an
  account integration, such as a chat message or a source-control notification. The docs
  describe no inbound webhook or API that a local device could call.
- **Notifications** go from a Bot to the person when the Bot finishes or needs input. They
  are not an input.
- **Routing egress through a desktop** lets the Bot's cloud computer reach networks
  available from that desktop. It is a per-desktop setting. We did not test it, and the LAN
  listener accepts device frames only, not MCP.

**Conclusion:** no documented route lets a device event wake Grok Bot without a hosted
relay or a third-party service carrying household events. Both are out of scope without a
specific owner decision. Button events stay in the gateway and Grok Bot reads them with
`gadgets_read_events` on its next call. Nothing hosted is built.

## Acceptance

Physical acceptance on the owner's kit, powered from a USB charger, records Pass, Fail or
Not tested for: connect on boot; text and clear; BOOT events; Wi-Fi loss and recovery;
gateway restart; token revoke then re-enroll; wrong-CA rejection; power cycle. Then one
Grok Bot run of `rehearse` shows text on the OLED over Wi-Fi. Each result pairs the owner's
observation with the gateway request-log line. ESP-005 closes only if every item passes.

## Consequences

- The gateway gains a network listener. It is off by default, private-address only and
  TLS-only.
- Provisioning needs the USB cable once per Wi-Fi or token change.
- The device's NVS holds secrets in plain flash. The docs state this limit.
- Grok Bot still reaches the gateway only through the routes in ADR 004.
