# Run the gateway away from your Mac

Today the gateway runs on your Mac, so Grok Bot reaches your gadget only while the Mac is awake. This guide moves the gateway to a small Linux host that stays on. Your Wi-Fi gadget connects out to that host. Grok Bot reaches it through your tunnel with OAuth sign-in, as before. The Mac can then sleep or stay off.

**Status:** this is Phase 9, proposed in [ADR 009](../decisions/009-relay-route.md). The gateway and firmware support is in development on `dev` and passes their tests. No owner's kit has run this route yet. Use the [Mac route](connect-grok-bot.md) for a tested setup.

```text
Grok Bot (Mac or iPhone) ─HTTPS + OAuth─▶ gadgets.example.net (tunnel) ─▶ gateway /mcp      ┐
Wi-Fi gadget at home ─TLS, outbound─▶ devices.example.net:8443 (device listener)          ┘ Linux host
```

## What you need

- A Linux host that stays on. A small VPS is the simplest choice. A home Linux box also works, but devices must reach it on port 8443, which usually means a router port forward.
- Two names on a domain you control:
  - `gadgets.example.net` for Grok Bot, through your tunnel.
  - `devices.example.net` for devices, a DNS-only record that points at the host's public address.
- Your tunnel, moved from the Mac to the host, or a new one.
- A Wi-Fi gadget on firmware that accepts a DNS name for the gateway, and a computer with a USB data cable to provision it once.
- The gateway and the firmware from the next releases.

The host costs whatever your provider charges. The project runs no relay service and pays for nothing.

## 1. Set up the host

Follow the gateway's [relay host guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/dev/docs/relay-host.md). It has two ways:

- **Container:** Docker Compose runs the gateway and the tunnel client together. It publishes only port 8443.
- **Linux user service:** `service install` with `--device-listen` and `loginctl enable-linger`.

Either way, run these once on the host:

```sh
grok-gadgets-gateway init
grok-gadgets-gateway device-cert devices.example.net
grok-gadgets-gateway enroll oledkit-0123456789ab
```

The gateway starts with `serve --oauth --allowed-host gadgets.example.net --device-listen 0.0.0.0:8443`. Open TCP port 8443 in the host's firewall. Never publish port 8766.

## 2. Move the tunnel

Point `gadgets.example.net` at `http://127.0.0.1:8766` on the host. If the tunnel ran on the Mac, stop it there first. Only one machine may run it.

Check from any computer:

```sh
curl -s -o /dev/null -w "%{http_code}\n" https://gadgets.example.net/.well-known/oauth-protected-resource/mcp
curl -s -o /dev/null -w "%{http_code}\n" -X POST https://gadgets.example.net/mcp
```

Expected: `200`, then `401`.

## 3. Provision the gadget

Plug the gadget into your computer with a data cable. Copy the host's `lan/ca.pem` and `credentials.json` to the computer, as the relay host guide shows. Then run, in your own terminal:

```sh
grok-gadgets-gateway wifi-provision /dev/cu.usbmodem101 --device oledkit-0123456789ab \
  --gateway devices.example.net --ca relay-ca.pem --credentials relay-credentials.json
rm relay-credentials.json relay-ca.pem
```

The command asks for your Wi-Fi name and password. They go to the gadget only, never to the host. Delete the copied files at once: `credentials.json` holds every device token.

Power the gadget from a USB charger. The top row shows `WiFi...`, then `Relay...`, then `Online`. If it shows `Relay name?`, check the DNS record. If it shows `TLS rejected`, provision again with the host's CA.

## 4. Connect Grok Bot

If Grok Bot already lists `grok-gadgets` and the tunnel kept its name, nothing changes. Otherwise, follow [Connect your Grok Bot](connect-grok-bot.md#3-add-the-server-in-grok-bot) with the new URL. Approve the sign-in code on the host:

```sh
grok-gadgets-gateway oauth approve K7QX-M2PA --name grok-bot
```

Put the Mac to sleep, and ask Grok Bot on the iPhone: "Show "Hello from Grok Bot" on my OLED gadget."

## Daily check

- The two `curl` commands give `200` and `401`.
- The gadget shows `Online`.
- The host's request log has `device_hello` for the gadget and `mcp_tool_call` lines with `"remote":true`.
- No `device_flood` or `oauth_flood` lines appear that you cannot explain.

## Turn it off

```sh
grok-gadgets-gateway remote off              # every remote request gets 503 at once
grok-gadgets-gateway oauth revoke grok-bot
grok-gadgets-gateway revoke oledkit-0123456789ab
```

Then stop the tunnel and the gateway on the host. To go back to the Mac, provision the gadget again with `--lan my-mac.local`.

## Safety

- Port 8443 accepts any address. The device token, TLS with your own CA and per-address limits protect it.
- Anyone with a shell on the host can approve sign-ins and read device tokens. Keep the host updated and allow only SSH and port 8443 in.
- The host sees device IDs, commands, reported state and events. It never receives your Wi-Fi password.
- A button press does not wake Grok Bot. Events wait until Grok Bot reads them.

Next: [track usage](track-usage.md) · [Hosting and remote access](hosting.md)
