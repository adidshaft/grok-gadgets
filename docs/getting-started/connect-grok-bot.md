# Connect your Grok Bot

Your existing Grok Bot can call the six gadget tools itself, from the desktop app and from the phone app. It reaches the gateway on your Mac through an HTTPS name that you run. On 13 October 2026 the owner's Grok Bot did this from a Mac and an iPhone. It showed text on the OLED kit ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/grok-remote-https-2026-10-13.md), [ADR 007](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/007-grok-bot-remote-https.md)).

On 13 October 2026 the owner also left the route on behind a fixed hostname. The [daily record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md) covers Mac and phone calls, cellular, a gateway restart, Mac sleep and a Mac restart.

The tunnel is optional. Without it, Grok Bot can still run approved local commands on the Mac; see [the no-tunnel route](#without-a-tunnel).

```text
Grok Bot (Mac or phone) ─HTTPS─▶ gadgets.example.net (your tunnel) ─▶ 127.0.0.1:8766 /mcp (gateway)
                                                                        devices: never tunnelled
```

## What you need

- The gateway `0.1.0a12` or later, with your gadget working locally first ([first success](first-success.md) or [the kit](repeat-the-kit.md)).
- A tunnel that you run, which ends HTTPS at a hostname and forwards only to `http://127.0.0.1:8766`. For daily use, take a tunnel with a fixed hostname on your own domain, run as a login service ([daily use](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/daily-use.md)). An account-free quick tunnel works for one session, but it gets a new hostname each time.
- Grok Bot on the desktop and, if you want, on the phone, signed in to the same account.

In the commands, `gadgets.example.net` is your tunnel hostname and `my-mac.local` is your Mac's name.

## 1. Start the gateway with sign-in

With the always-on service:

```sh
grok-gadgets-gateway service uninstall
grok-gadgets-gateway service install --lan-listen my-mac.local --allowed-host gadgets.example.net --oauth
```

Or in a terminal:

```sh
grok-gadgets-gateway serve --allowed-host gadgets.example.net --oauth \
  --request-log ~/grok-gadgets-requests.jsonl
```

`--oauth` makes the gateway its own sign-in server at `https://gadgets.example.net`. You approve each sign-in on the Mac, so no password or token goes into a web page or a chat. The request log is always on with a tunnel.

## 2. Open the tunnel

Start your tunnel client so that `https://gadgets.example.net` forwards to `http://127.0.0.1:8766`. Check from outside:

```sh
curl -s -o /dev/null -w "%{http_code}\n" https://gadgets.example.net/.well-known/oauth-protected-resource/mcp
```

Expected: `200`. The [tunnel guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/tunnel.md) has more checks.

## 3. Add the server in Grok Bot

The app has no settings form for a custom server. Ask Grok Bot in a one-to-one chat on the desktop:

> Please add a custom MCP server for yourself. Name: grok-gadgets. Type: Remote HTTPS. URL: https://gadgets.example.net/mcp. Authentication: OAuth sign-in, no header and no token.

1. Confirm Grok Bot's card "Add grok-gadgets as a Remote HTTPS server with OAuth sign-in?".
2. On the connect card choose **Authorize**, then **Continue**. A page opens in your browser with a code such as `K7QX-M2PA`.
3. On the Mac, check the code and approve it:

   ```sh
   grok-gadgets-gateway oauth pending
   grok-gadgets-gateway oauth approve K7QX-M2PA --name grok-bot
   ```

Approve only the code that your own page shows. Grok Bot then lists "grok-gadgets, 6 tools".

## 4. Use it from the Mac and the phone

Ask in the chat, for example:

- "Using the grok-gadgets tools, list my gadgets."
- "Show "Hello from Grok Bot" on my OLED gadget."
- "What is the OLED gadget's state now?"

The same server works from the Grok Bot phone app with no setup there. Its tools run where the Bot runs, so the phone's plugin list may not show it.

Check the gateway log. Each call adds an `mcp_tool_call` line with `"token":"grok-bot"` and `"remote":true`. A reported state is the device's own report; look at the device for the physical result.

## Leave it on

With gateway `0.1.0a12` or later, the route can stay on. The gateway limits sign-in floods, rotates its logs and shows the route in `service status`. Follow [daily use](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/daily-use.md) for the tunnel client as a login service, a one-minute daily check, sleep settings and a notification on each remote call.

What the owner's setup showed on 13 October ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md)):

- **Gateway restart:** the board was back in about 1 second, and the next call needed no new sign-in.
- **Mac asleep:** Grok Bot got a 502 from the tunnel provider and no gadget result. Nothing was queued. The tunnel and the board came back within seconds of the wake.
- **Mac restart:** after login the gateway, the tunnel and the board came back by themselves, 66–72 seconds after boot. The sign-in stayed valid.
- **`remote off`:** Grok Bot reported that remote access was off and did not retry.

If Grok Bot still lists an older `grok-gadgets` server, for example from a quick tunnel, ask it to replace that server with the new URL.

## Turn it off

```sh
grok-gadgets-gateway remote off           # every remote request gets 503 at once
grok-gadgets-gateway oauth revoke grok-bot
```

Then stop the tunnel, and remove `grok-gadgets` in Grok Bot under **Connect apps** → the connected list → **Uninstall**. Run `grok-gadgets-gateway remote on` before the next session. To leave the tunnel off for good, reinstall the service without `--allowed-host` and `--oauth`.

## Without a tunnel

Grok Bot can run an approved command on the Mac through **Execution on Local Computer**. That command calls the gateway on `127.0.0.1`:

```sh
grok-gadgets-gateway rehearse --device DEVICE --command display.text --args '{"text":"Hello from Grok Bot"}'
```

This works only from the desktop app, needs your approval for each command, and runs one fixed command instead of the six tools. See the [local test](https://github.com/adidshaft/grok-gadgets/blob/main/docs/grok-local-test.md) and [ADR 004](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/004-grok-bot-route.md).

## Safety

- Forward only port 8766. Never forward the device port or the Wi-Fi listener.
- Anyone who can run `oauth approve` on your Mac controls access. A sign-in lasts until `oauth revoke`, or 30 days without use.
- The limits apply per name: 60 tool calls and 10 commands a minute.
- Leave the tunnel on only with gateway `0.1.0a12` or later, and run the [daily check](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/daily-use.md#3-daily-check).

Next: [track usage](track-usage.md).
