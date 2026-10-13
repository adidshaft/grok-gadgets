# Grok Bot Remote HTTPS test: owner checklist

This test shows whether your existing Grok Bot, on the desktop and on the phone, calls the six `gadgets_*` tools itself through a **Remote HTTPS** MCP server. The server is the always-on gateway on your Mac, behind a TLS tunnel that you run. The gateway request log is the evidence; your view of the OLED is the physical check. The Bot's own description of what it did is not evidence.

Run it yourself, in your own Grok Bot account, with a tunnel that you run. The project runs no URL, relay or account for you. Background: [research note](research/grok-remote-https-2026-10.md), [tunnel guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/tunnel.md), [ADR 004](decisions/004-grok-bot-route.md). The earlier [local test](grok-local-test.md) gave outcome (b) on 12 October 2026.

Runs 1 to 3, on 13 October 2026, passed the gateway checks, but Grok Bot could not add a server with a fixed token; see the [record](verification/grok-remote-https-2026-10-13.md).

Possible outcomes:

- **(a)** Grok Bot adds the server and calls the tools. The log shows `mcp_tool_call` lines with `"token":"grok-bot"`, `"remote":true` and a client other than `grok-gadgets-rehearse`.
- **(d)** Grok Bot declines the server, or never reaches it. No `grok-bot` lines appear. Record the Bot's message and stop.

Time: about 40 minutes. In the commands, `my-mac.local` is your Mac's name and `gadgets.example.net` is your tunnel hostname. Do not paste either, a token or a screenshot of your account into a public issue.

## What you need

- The OLED kit on Wi-Fi and the always-on service, as on 13 October 2026.
- A tunnel that you run yourself, ending HTTPS at a hostname and forwarding to `http://127.0.0.1:8766`: either your own account with a hostname you control, or an account-free quick tunnel whose random hostname you use for this run only. Start a quick tunnel before section 0, because the service needs its hostname. It must keep the original Host header, or add a forwarding header. It must not forward any other port.
- The Grok Bot desktop app on this Mac, and the Grok Bot app on your phone, signed in to the same account.
- No other Grok Bot work during the test, so the usage readings belong to it.

## 0. Prepare the gateway (8 minutes)

The tunnel rules, usage summary and OAuth sign-in are on the gateway `dev` branch. They are not released yet.

1. Update the gateway checkout. The service runs from it.

   ```sh
   cd ~/projects/grok-gadgets-gateway && git switch dev && git pull && uv sync --locked
   G="$HOME/projects/grok-gadgets-gateway/.venv/bin/grok-gadgets-gateway"
   "$G" --version
   ```

   Expected: `grok-gadgets-gateway 0.1.0a11` or later, and `"$G" oauth --help` works.

2. No token file is needed. Grok Bot signs in with OAuth, and you approve the sign-in on this Mac.

3. Reinstall the service with the tunnel name and sign-in. This restarts the gateway; the board shows **Gateway...** and then **Online**.

   ```sh
   "$G" service uninstall
   "$G" service install --lan-listen my-mac.local --allowed-host gadgets.example.net --oauth
   "$G" remote on
   "$G" service status
   ```

   Expected: `service: running`. If `install` says a port is in use, wait a few seconds and run it again. The request log is `~/Library/Logs/grok-gadgets/requests.jsonl`. Wait for **Online** on the OLED.

4. Check the rules before any tunnel exists. Each request goes to loopback with the tunnel Host, as the tunnel will send it:

   ```sh
   U=http://127.0.0.1:8766; H="Host: gadgets.example.net"; J="Content-Type: application/json"
   c() { curl -s -o /dev/null -w "%{http_code}\n" "$@"; }
   c -X POST "$U/mcp" -H "$H" -H "$J" -d '{}'
   c -X POST "$U/mcp" -H "$H" -H "Authorization: Bearer $(cat ~/.config/grok-gadgets/mcp-token)" -H "$J" -d '{}'
   c "$U/.well-known/oauth-authorization-server" -H "Host: wrong.example.org"
   c "$U/.well-known/oauth-authorization-server" -H "$H"
   ```

   Expected, in order: `401`, `403`, `421`, `200`. Stop if any differ.

5. In Terminal tab 2, watch the Grok Bot lines only:

   ```sh
   tail -n 0 -f ~/Library/Logs/grok-gadgets/requests.jsonl | grep --line-buffered '"token":"grok-bot"'
   ```

## 1. Open the tunnel (3 minutes)

1. Start your tunnel client so that `https://gadgets.example.net` forwards to `http://127.0.0.1:8766`. Follow your provider's own guide.
2. Check it from outside:

   ```sh
   curl -s -o /dev/null -w "%{http_code}\n" -X POST https://gadgets.example.net/mcp -H "Content-Type: application/json" -d '{}'
   ```

   Expected: `401`. If you get anything else, stop the tunnel and check its target.

3. Check that the gateway sees tunnel requests as remote. The kill switch must stop them:

   ```sh
   "$G" remote off
   curl -s -o /dev/null -w "%{http_code}\n" https://gadgets.example.net/.well-known/oauth-authorization-server
   "$G" remote on
   ```

   Expected: `503`. If you get `200`, your tunnel hides that requests come from outside; stop it and fix its Host setting.

4. Write down the time (T0, local) and run `date -u` for the UTC time.

## 2. Usage reading R0 (1 minute)

On the **desktop**, open Grok Bot **Settings** and find the **Weekly usage limit** row. Write down the exact page name and the value exactly as shown, with the time. If you also see **Settings → Usage & Billing**, write down its on-demand value too. Take the same reading on the **phone** (**Settings → Weekly usage**).

## 3. Add the server and sign in (5 minutes)

Runs 1 to 3 showed that Grok Bot cannot add a server with a fixed token ([record](verification/grok-remote-https-2026-10-13.md)). Run 4 used OAuth sign-in, below.

1. Start a new one-to-one chat with your Grok Bot on the desktop. Send:

   > Please add a custom MCP server for yourself. Name: grok-gadgets. Type: Remote HTTPS. URL: https://gadgets.example.net/mcp. Authentication: OAuth sign-in, no header and no token. When the sign-in step appears, show it to me; I will approve it on my Mac.

2. Grok Bot shows a card "Add grok-gadgets as a Remote HTTPS server with OAuth sign-in?". Choose **Yes, add it** if the URL is yours.
3. On the connect card, choose **Authorize**, then **Continue** in Grok Bot's "Connect to grok-gadgets" dialog. A page opens in your browser. It shows a code such as `K7QX-M2PA` and waits.
4. In a terminal, check that the same code is waiting, then approve it:

   ```sh
   "$G" oauth pending
   "$G" oauth approve K7QX-M2PA --name grok-bot
   ```

   Approve only the code that your own page shows. The page continues by itself, and Grok Bot shows "grok-gadgets, 6 tools".

5. Tab 2 shows nothing yet: registration and sign-in are not tool calls. The log has `oauth_sign_in_approved` and `oauth_token_issued` lines.

If Grok Bot refuses the server or the URL, record its exact message and go to section 7. That is outcome (d).

## 4. Prompts from the Mac (8 minutes)

Start a new one-to-one chat with your Grok Bot on the desktop. Send these six prompts, one at a time, and wait for each answer. After each one, check tab 2 and the OLED.

1. > Using the grok-gadgets tools, list my gadgets.
2. > Using the grok-gadgets tools, show "Hello from Grok Bot" on my OLED gadget.
3. > Check the status of that command.
4. > What is the OLED gadget's state now?
5. Press and release BOOT on the board, then:
   > I just pressed the button on the board. Read my gadget events.
6. > Run the gadget diagnostics.

For each prompt, note whether an approval card appeared and what you chose.

Expected for outcome (a): each prompt adds at least one line like

```json
{"ts":"…","event":"mcp_tool_call","client":"<name the Bot sent>","token":"grok-bot","remote":true,"tool":"gadgets_command","device_id":"…","capability":"display.text","outcome":"ok","status":"executed",…}
```

The tools, in prompt order: `gadgets_list_devices`, `gadgets_command`, `gadgets_command_status`, `gadgets_get_state`, `gadgets_read_events`, `gadgets_diagnostics`. The OLED shows the text after prompt 2. If no line appears, the Bot did not reach the gateway, whatever it says.

Write down the time (T1). Take usage reading **R1** on the desktop page from section 2.

## 5. Prompts from the phone (6 minutes)

On the phone, open the Grok Bot app. Check whether `grok-gadgets` appears under plugins or connectors; do not add it again. Start a new chat with the same Bot and send:

1. > Using the grok-gadgets tools, list my gadgets.
2. > Using the grok-gadgets tools, show "Hello from my phone" on my OLED gadget.
3. > What is the OLED gadget's state now?

Watch tab 2 and the OLED. Approve any card on the phone. Write down the time (T2) and take usage reading **R2** on the phone page and on the desktop page.

## 6. Usage summary (1 minute)

```sh
"$G" usage --token grok-bot --since T0_UTC
```

Replace `T0_UTC` with the UTC time from section 1, for example `2026-10-14T09:00`. Copy the output. Count the prompts you sent: nine if all were sent.

If R0 and R2 use the same unit, record the rate as an estimate:

```sh
"$G" usage --token grok-bot --since T0_UTC --until T2_UTC --calibrate CHANGE --unit "% weekly usage"
```

`CHANGE` is R2 minus R0, in the unit shown. The result is an **estimate**: Grok Bot's usage covers all its work in that window, not only tool calls.

## 7. Turn everything off (5 minutes)

Do this even if the test failed, unless you decide to keep the route.

1. Stop remote access and end the sign-in:

   ```sh
   "$G" remote off
   "$G" oauth revoke grok-bot
   "$G" oauth list
   ```

   `oauth list` prints nothing.

2. Stop the tunnel client. Check: `curl -s -o /dev/null -w "%{http_code}\n" https://gadgets.example.net/mcp` no longer gives `401` from your gateway.
3. Remove `grok-gadgets` from Grok Bot on the desktop: **Connect apps** → the connected list → `grok-gadgets` → **Uninstall**.
4. Put the service back on the released gateway, without the tunnel name:

   ```sh
   "$G" remote on
   "$G" service uninstall
   cd ~/projects/grok-gadgets-gateway && git switch main && uv sync --locked
   "$G" service install --lan-listen my-mac.local
   ```

   Wait for **Online** on the OLED. `remote on` only restores the default for a later test; without `--allowed-host` the service accepts no tunnel Host.
5. Stop `tail` in tab 2 with Ctrl+C. Copy the `grok-bot` lines first:

   ```sh
   grep '"token":"grok-bot"' ~/Library/Logs/grok-gadgets/requests.jsonl
   ```

## 8. Results template

Paste this back. The log has no tokens, but read it before you paste it, and replace your hostname with `gadgets.example.net`.

```text
Date and time zone:
Grok Bot desktop app version, phone app version, macOS and phone OS:
Gateway version and commit (git -C ~/projects/grok-gadgets-gateway rev-parse --short HEAD before section 7):
Tunnel: own account (yes/no); Host kept or forwarding header added:

Section 0 checks (401 / 403 / 421 / 200):
Outside checks through the tunnel (401; 503 with remote off):

Server added on the desktop (yes / no / refused):
  Sign-in code on the page and in `oauth pending` (same / different):
  Grok Bot listed grok-gadgets with 6 tools (yes / no):
  Bot message if refused:

Mac prompts 1-6, for each: tool line seen (yes/no), approval card (yes/no, choice), OLED observation:
Phone: server listed (yes/no); prompts 1-3 as above:

Usage readings (page, exact value, local time):
  R0 desktop:          R0 phone:
  R1 desktop:
  R2 desktop:          R2 phone:
  On-demand (if shown):
Prompts sent:
usage output:
Calibrated estimate (if any):

grok-bot log lines:

Turn-off: remote off, token revoked, tunnel stopped, server removed (desktop/phone), service back on main, Online again:
Keep the route? (no unless you say so):
Other observations:
```

The result is recorded in [#154](https://github.com/adidshaft/grok-gadgets/issues/154), [#4](https://github.com/adidshaft/grok-gadgets/issues/4) and ADR 007, with log lines, usage readings and narrative kept apart. Any per-call usage figure is an estimate.
