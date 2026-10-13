# Grok Bot Remote HTTPS test, runs 1 and 2 — 13 October 2026

Run of the [owner checklist](../grok-remote-test.md) on the owner's Mac, 13 October 2026, Asia/Kolkata (UTC+05:30). The owner authorized it and delegated the on-screen steps to a computer-use session on the Mac. Screen observations below are that session's narrative unless the gateway log confirms them.

**Result: not completed.** The gateway side passed. No Remote HTTPS server was added to Grok Bot, so Grok Bot made no tool calls and no prompts were sent. This is not a refusal by Grok Bot: the session looked for a settings form and found none, and it did not try the documented chat path.

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
