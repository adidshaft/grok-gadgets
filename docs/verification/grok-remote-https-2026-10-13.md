# Grok Bot Remote HTTPS test, runs 1 to 4 — 13 October 2026

Run of the [owner checklist](../grok-remote-test.md) on the owner's Mac, 13 October 2026, Asia/Kolkata (UTC+05:30). The owner authorized it and delegated the on-screen steps to a computer-use session on the Mac. Screen observations below are that session's narrative unless the gateway log confirms them.

**Final result (run 4): Grok Bot called all six tools itself, from the Mac and from the phone, through OAuth sign-in.** Runs 1 to 3 below did not get that far.

Run 1 result: not completed. The gateway side passed. No Remote HTTPS server was added to Grok Bot, so Grok Bot made no tool calls and no prompts were sent. This is not a refusal by Grok Bot: the session looked for a settings form and found none, and it did not try the documented chat path.

| Item | Value |
| --- | --- |
| Grok Bot desktop app | 0.70.2 (reported) |
| macOS | 27.0 (26A5388g) (reported) |
| Phone app and OS | Not checked |
| Gateway under test | `dev` `1cab13f`, package `0.1.0a11` (log: `serve_started` `0.1.0a11` at 07:04:15 UTC) |
| Tunnel | An account-free quick tunnel run by the owner's session; hostname not recorded |
| Device | Owner's ESP32-S3 OLED kit on Wi-Fi, through the always-on service |

## What the gateway log shows

Independently read from the service request log after the run. Times are UTC.

| Time | Line | Meaning |
| --- | --- | --- |
| 07:04:10 | `serve_stopped`, then `serve_started` `0.1.0a11` at 07:04:15 | Service reinstalled from `dev` with the tunnel name |
| 07:04:43 | `http_rejected` 401 `invalid_token` (twice) | A request without a token was refused |
| 07:04:59 | `http_rejected` 403 `named_token_required`, token `default` | The local token was refused for a tunnel Host |
| 07:05:09 | `http_rejected` 503 `remote_disabled` | The kill switch refused a remote request |
| — | No `mcp_tool_call` line with `"token":"grok-bot"` | Grok Bot never called a tool |
| 07:16:34 | `serve_stopped`, then `serve_started` `0.1.0a10` at 07:16:43 | Service restored to `main` |

The service's own log shows the board reconnecting at 07:16:52 (`lan_hello`). The owner did not look at the OLED.

The log does not record whether a 401 came through the tunnel or from loopback. The session reported 401, 200, 421 and 403 for the section 0 checks, and 401, then 503, through the tunnel. The 200 and 421 results are not in the log, because accepted `initialize` calls and Host rejections are not logged.

## What the session reported (narrative)

- It inspected **Connect apps**, **Your plugins** and the Bot details. It found no form to add a custom Remote HTTPS server and no OAuth option. It did not ask the Bot in chat to add one.
- An earlier **Grok Gadgets Simulator** server is still installed. It is the Command server that Grok Bot added on its own cloud computer on 4 October 2026 ([record](real-grok-experiment.md)). The session did not change it.
- Usage reading R0: desktop **Weekly usage limit** "1% used", "Resets in 4 days"; phone **Weekly usage** "1%". No screenshot was kept, and the owner has not confirmed these values. R1 and R2 were not taken. No prompts were sent, so there is no usage per prompt or per tool call.

## Clean-up, checked independently after the run

- The gateway checkout is on `main`. The service runs `0.1.0a10` with no `--allowed-host`.
- `mcp-token list` shows `grok-bot` revoked at 07:04:01 UTC. The token file is deleted.
- No tunnel process is running. The session reported that the old tunnel URL answered 530, not the gateway's 401.

## Next step

The [Team Bots page](https://docs.x.ai/grok-bot/team-bots) says a Bot is set up from its info pane "or ask the Bot in chat". On 4 October 2026, Grok Bot added a Command server when asked in chat. Run 2 asks the Bot in chat to add the Remote HTTPS server, and gives the token only through a masked credential prompt. If the Bot then declines the public HTTPS server, that is the recorded outcome.

# Run 2 — 13 October 2026

Same Mac, app versions, gateway build and tunnel type as run 1. Grok Bot was asked in chat to add the server. **Result: stopped at registration by the test operator, not refused by Grok Bot.** No server was added and no token was given to Grok Bot.

## What the gateway log shows

| Time (UTC) | Line | Meaning |
| --- | --- | --- |
| 07:39:35 | `serve_started` `0.1.0a11` | Service reinstalled from `dev` with the tunnel name |
| 07:39:57, 07:40:25 | `http_rejected` 401 `invalid_token` | Requests without a token refused |
| 07:40:15 | `http_rejected` 403 `named_token_required`, token `default` | Local token refused for a tunnel Host |
| 07:40:35 | `http_rejected` 503 `remote_disabled` | Kill switch refused a remote request |
| — | No `mcp_tool_call` with `"token":"grok-bot"` | Grok Bot never called a tool |
| 07:48:41 | `serve_started` `0.1.0a10` | Service restored to `main` |

## What Grok Bot said (narrative)

Asked in chat to add `grok-gadgets` as a Remote HTTPS server, Grok Bot did not refuse. It explained that its secure prompt stores a hidden value that a Remote server's `Authorization` header cannot refer to. To fill the header, it would read the token back and put it in its setup call, so the token would appear in its tool history. It also noted that anyone with the quick-tunnel URL and the token could reach the gateway while the tunnel is up. In a group chat it said secure prompts do not work there; in the one-to-one chat it showed a card asking whether to ask for the token. The test operator chose **No, don't add it**, because the checklist then required the token to stay out of the Bot's history. Grok Bot confirmed it changed no connectors.

## Usage

| Reading | Page | Value | Time (local) |
| --- | --- | --- | --- |
| R0 desktop | Settings → Usage & Billing, **Weekly usage limit** | "1% used", "Resets in 4 days" | 13:12:10 |
| R0 phone | Settings → **Weekly usage** | "1%", "Resets in 4 days" | 13:12:40 |
| On-demand | **On-demand monthly limit** | "None" | 13:12:10 |

Row-only screenshots are kept privately on the owner's Mac. They show the same values. R1 and R2 were not taken. Two setup messages and no gadget prompts were sent. The page shows whole percent only, so a short test may show no change.

## Clean-up, checked independently

`grok-bot` revoked at 07:39:21 UTC (a new token for this run), token file deleted, no tunnel process, service on `main` with no `--allowed-host`. The owner saw "online grok bot" on the OLED. `grok-gadgets` is not in the installed plugins on the desktop or the phone (operator report).

## Next step

The only registration path Grok Bot offered puts the token in its tool history. Run 3 needs the owner's decision on that.

# Run 3 — 13 October 2026

Same Mac, app versions, gateway build and tunnel type. The owner accepted that a new, single-run token could enter Grok Bot's setup tool history. **Result: Grok Bot could not add the server with a fixed token.** No server was added and Grok Bot made no tool calls.

## What the gateway log shows

| Time (UTC) | Line | Meaning |
| --- | --- | --- |
| 08:07:47 | `serve_started` `0.1.0a11` | Service reinstalled from `dev` with the tunnel name |
| 08:08:11, 08:08:19 | `http_rejected` 401 `invalid_token` | Requests without a token refused |
| 08:08:11 | `http_rejected` 403 `named_token_required`, token `default` | Local token refused for a tunnel Host |
| 08:08:33 | `http_rejected` 503 `remote_disabled` | Kill switch refused a remote request |
| — | No `mcp_tool_call` with `"token":"grok-bot"` | Grok Bot never called a tool |
| 08:16:03 | `serve_started` `0.1.0a10` | Service restored to `main` |

## What Grok Bot said (narrative)

The token was pasted into Grok Bot's masked secure prompt at 13:42:30 local time. At 13:43:35 Grok Bot replied that the token arrived, that its computer blanks the token in anything shown to it, and that the server setup step does not accept a reference to the saved value. It said the only ways around that would bypass a safeguard, so it would not. It suggested adding the server in the app with the header, or a gateway sign-in method that needs no fixed token. It corrected its run 2 statement that it could read the token back. No setup step or log line shows the token in its tool history. The session again found no custom-server form in the Bot's info pane or **Connect apps**, and no OAuth offer. The token was revoked by 13:45:24.

## Usage

R0 desktop **Weekly usage limit** "1% used", "Resets in 4 days" (13:39:48); phone **Weekly usage** "1%" (13:40:28); on-demand monthly limit "None". Row-only screenshots on the owner's Mac show the same values. No gadget prompts were sent.

## Clean-up, checked independently

Token revoked, token file deleted, no tunnel process, service on `main` with no `--allowed-host`. The owner saw "Online Grok Bot" on the OLED.

## Finding after three runs

On this personal Grok Bot (desktop 0.70.2), a Remote HTTPS server with a fixed bearer header could not be added: no form for it was found, and Grok Bot will not place a fixed token in the setup step. The Team Bots page names the other documented credential: "each person's sign-in if the server uses OAuth". The gateway does not offer OAuth yet ([gateway #71](https://github.com/adidshaft/grok-gadgets-gateway/issues/71)).

# Run 4 — 13 October 2026: native tool calls from the Mac and the phone

The gateway now offers OAuth sign-in (`serve --oauth`, [gateway #71](https://github.com/adidshaft/grok-gadgets-gateway/issues/71)). The owner authorized the run and delegated the on-screen steps to a computer-use session on the Mac. The owner looked at the OLED. **Result: outcome (a).** Grok Bot discovered the six tools, and its own calls reached the gateway from the desktop app and from the iPhone app.

| Item | Value |
| --- | --- |
| Grok Bot desktop app | 0.70.2; macOS 27.0 (26A5388g) |
| Phone | iPhone 15 Pro, Grok Bot app, reached through iPhone Mirroring |
| Gateway | `dev` `e9f39d0`, package `0.1.0a11`, always-on service with `--lan-listen`, one `--allowed-host` and `--oauth` |
| Tunnel | An account-free quick tunnel to `127.0.0.1:8766` only, 08:45–09:06 UTC; hostname not recorded |
| Device | Owner's ESP32-S3 OLED kit on Wi-Fi |

## Gateway checks before the test

Through the service, 08:46 UTC: no token 401; the local `default` token with the tunnel Host 403; a wrong Host on the sign-in metadata 421; protected-resource metadata from outside 200; `/mcp` from outside 401 with `resource_metadata` in the challenge; sign-in metadata from outside with `remote off` 503.

## Sign-in

| Time (UTC) | What happened | Source |
| --- | --- | --- |
| 08:47 | Asked in the one-to-one chat to add `grok-gadgets` as a Remote HTTPS server with OAuth sign-in, URL only, no header or token | Chat |
| 08:48:27 | Two 401s on `/mcp`, then two `oauth_client_registered` | Gateway log |
| 08:48 | Grok Bot's card "Add grok-gadgets as a Remote HTTPS server with OAuth sign-in?" was confirmed | Screen |
| 08:50 | The connect card's **Authorize**, then Grok Bot's "Connect to grok-gadgets" dialog, **Continue**; a third registration at 08:50:05 | Screen, gateway log |
| 08:52:33 | `oauth_sign_in_requested`, code `DN62-8KAC`; the sign-in page opened in Chrome and showed the same code | Gateway log, screen |
| 08:52:46 | `oauth_sign_in_approved` as `grok-bot`, by `oauth approve` on the Mac | Gateway log |
| 08:52:47 | `oauth_token_issued` to `grok-bot`; Grok Bot showed "grok-gadgets, 6 tools, Added" | Gateway log, screen |

No password or token was typed into a page or a chat.

## What the gateway log shows

Every `mcp_tool_call` with `"token":"grok-bot"` in the window. The `client` field is the name that Grok Bot's connector backend sends in `initialize`; it is replaced here by `<connector client>` because it names a third-party company. It is not `grok-gadgets-rehearse`.

```json
{"ts": "2026-10-13T08:53:12.445187+00:00", "client": "<connector client>/1.0.0", "token": "grok-bot", "remote": true, "tool": "gadgets_list_devices", "outcome": "ok", "duration_ms": 0.5, "bytes_in": 2, "bytes_out": 1903}
{"ts": "2026-10-13T08:53:52.137768+00:00", "client": "<connector client>/1.0.0", "token": "grok-bot", "remote": true, "tool": "gadgets_command", "device_id": "oledkit-84c7bb57148c", "capability": "display.text", "outcome": "ok", "status": "executed", "duration_ms": 167.8, "bytes_in": 125, "bytes_out": 611}
{"ts": "2026-10-13T08:54:15.193817+00:00", "client": "<connector client>/1.0.0", "token": "grok-bot", "remote": true, "tool": "gadgets_command_status", "outcome": "ok", "status": "executed", "duration_ms": 0.3, "bytes_in": 52, "bytes_out": 593}
{"ts": "2026-10-13T08:54:35.121024+00:00", "client": "<connector client>/1.0.0", "token": "grok-bot", "remote": true, "tool": "gadgets_get_state", "device_id": "oledkit-84c7bb57148c", "outcome": "ok", "duration_ms": 0.4, "bytes_in": 36, "bytes_out": 1918}
{"ts": "2026-10-13T08:54:57.831872+00:00", "client": "<connector client>/1.0.0", "token": "grok-bot", "remote": true, "tool": "gadgets_read_events", "outcome": "ok", "duration_ms": 0.1, "bytes_in": 43, "bytes_out": 143}
{"ts": "2026-10-13T08:57:29.120688+00:00", "client": "<connector client>/1.0.0", "token": "grok-bot", "remote": true, "tool": "gadgets_diagnostics", "outcome": "ok", "duration_ms": 0.5, "bytes_in": 2, "bytes_out": 435}
{"ts": "2026-10-13T09:02:58.571598+00:00", "client": "<connector client>/1.0.0", "token": "grok-bot", "remote": true, "tool": "gadgets_list_devices", "outcome": "ok", "duration_ms": 0.4, "bytes_in": 2, "bytes_out": 1922}
{"ts": "2026-10-13T09:03:18.739281+00:00", "client": "<connector client>/1.0.0", "token": "grok-bot", "remote": true, "tool": "gadgets_command", "device_id": "oledkit-84c7bb57148c", "capability": "display.text", "outcome": "ok", "status": "executed", "duration_ms": 107.8, "bytes_in": 125, "bytes_out": 611}
{"ts": "2026-10-13T09:03:38.657072+00:00", "client": "<connector client>/1.0.0", "token": "grok-bot", "remote": true, "tool": "gadgets_get_state", "device_id": "oledkit-84c7bb57148c", "outcome": "ok", "duration_ms": 0.3, "bytes_in": 36, "bytes_out": 1918}
```

| Prompt | From | Tool calls |
| --- | --- | --- |
| 1 "Using the grok-gadgets tools, list my gadgets." | Mac | `gadgets_list_devices` |
| 2 "… show "Hello from Grok Bot" on my OLED gadget." | Mac | `gadgets_command` `display.text`, `executed` |
| 3 "Check the status of that command." | Mac | `gadgets_command_status` |
| 4 "What is the OLED gadget's state now?" | Mac | `gadgets_get_state` |
| 5 "Read my gadget events." (no button press) | Mac | `gadgets_read_events`, no events |
| 6 "Run the gadget diagnostics." | Mac | `gadgets_diagnostics` |
| 7 "Using the grok-gadgets tools, list my gadgets." | Phone | `gadgets_list_devices` |
| 8 "… show "Hello from my phone" on my OLED gadget." | Phone | `gadgets_command` `display.text`, `executed` |
| 9 "What is the OLED gadget's state now?" | Phone | `gadgets_get_state` |

Each prompt gave exactly one tool call: 9 calls, 0 errors, 2 commands. Prompt 5 differs from the checklist: nobody pressed BOOT, so the call returned no events.

## Physical check

The owner looked at the OLED after prompt 2 and saw "Hello from Grok Bot". After prompt 8 the device reported "Hello from my phone"; the owner did not report a second look.

## Usage

| Reading | Page | Value | Time (UTC) |
| --- | --- | --- | --- |
| R0 desktop | Settings → Usage & Billing, **Weekly usage limit** | "1% used", "Resets in 4 days"; on-demand "None" | 08:46:57 |
| R1 desktop | same | "1% used", "Resets in 4 days" | 08:57:51 |
| R2 phone | Settings → Usage, **Weekly usage** | "1%", "Resets in 4 days" | 09:04 |
| R2 desktop | same as R0 | "1% used", "Resets in 4 days" | 09:04:22 |

Messages sent to Grok Bot in the window: two setup messages (two questions, then the add request) and nine gadget prompts. `grok-gadgets-gateway usage --token grok-bot --since 2026-10-13T08:46 --until 2026-10-13T09:05`:

```text
total:  calls=9  errors=0  commands=2  duration_ms=278.1  bytes=10477
by token:
  grok-bot  calls=9  errors=0  commands=2  duration_ms=278.1  bytes=10477
by device:
  -  calls=5  errors=0  commands=0  duration_ms=1.8  bytes=5097
  oledkit-84c7bb57148c  calls=4  errors=0  commands=2  duration_ms=276.3  bytes=5380
by capability:
  -  calls=7  errors=0  commands=0  duration_ms=2.5  bytes=9005
  display.text  calls=2  errors=0  commands=2  duration_ms=275.6  bytes=1472
by day:
  2026-10-13  calls=9  errors=0  commands=2  duration_ms=278.1  bytes=10477
Days are UTC. Counts come from this gateway's request log only.
```

The pages show whole percent only, and all readings stayed at 1%. The rate was not calibrated: a zero change gives no useful rate. The estimate is in [ADR 007](../decisions/007-grok-bot-remote-https.md).

## Turn-off, checked independently

`remote off`, then `oauth revoke grok-bot` at 09:06:41 UTC; `oauth list` shows no sign-in. The tunnel was stopped; its URL then answered 530. `grok-gadgets` was uninstalled from Grok Bot (Connect apps → Manage plugins). The service was put back on `main` (`0.1.0a10`) without `--allowed-host` or `--oauth` at 09:07:44, and the board reconnected at 09:07:46 (`lan_hello`). `remote on` restores the default only.

## Narrative and observations (not evidence)

- Grok Bot's replies matched the log: one OLED kit, state reads, no events, a healthy gateway. It said each time that reported state is not physical proof.
- On the phone, **Your plugins** did not list `grok-gadgets`, but the phone chat used it. Its tools run where the Bot runs, not on the phone.
- The diagnostics reply noted that the loopback device listener showed no session; the board uses the Wi-Fi listener.
- Run 3 left a revoked token as a saved secret named "grok-gadgets bearer token" in Grok Bot. It no longer works anywhere.
