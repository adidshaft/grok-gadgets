# Daily native route — 13 October 2026

Phase 8 ([#251](https://github.com/adidshaft/grok-gadgets/issues/251), [ADR 008](../decisions/008-daily-native-route.md)). Grok Bot on the owner's Mac and iPhone called the gadgets through a fixed-hostname tunnel that the owner runs, with gateway OAuth sign-in. Times are UTC. The owner authorized each step. A computer-use session on the Mac did the Mac-side steps; the owner did the phone and kit steps, and restarted the Mac.

**One day only.** The owner chose to run every check on 13 October. The plan asked for two separate days; a second day is not recorded.

Evidence levels: **log** is the gateway request log, read after each step; **owner** is what the owner saw; **Bot** is Grok Bot's reply, which is narrative only.

| Item | Value |
| --- | --- |
| Gateway | `0.1.0a12` (release `v0.1.0-alpha.12`), always-on launchd service with `--lan-listen my-mac.local`, one `--allowed-host`, `--oauth` and the macOS notification hook |
| Tunnel | Cloudflare named tunnel, one hostname (here `gadgets.example.net`) to `http://127.0.0.1:8766` only, 404 for anything else; `cloudflared` as a login agent |
| Grok Bot | Desktop app on macOS 27.0; iPhone app |
| Device | Owner's ESP32-S3 OLED kit on Wi-Fi, USB charger |

## Before sign-in

The service was reinstalled at 12:06:13 and logged `serve_started` `0.1.0a12` at 12:06:15. The board sent `lan_hello` at 12:06:16.

Checks on loopback with the tunnel Host (log): no token 401, the local `default` token 403, a wrong Host 421. HTTP on the device port was closed (`device_http_rejected`). `remote off` gave 503, `remote on` 200. Through the public hostname: metadata 200, `/mcp` without a token 401 with the metadata link, a forged Host refused.

`cloudflared service install` without `sudo` wrote a login agent that ran plain `cloudflared`, which exits with "use `cloudflared tunnel run`". The agent's arguments were changed to `tunnel --config ~/.cloudflared/config.yml run`. The tunnel then registered 3 connections.

## Sign-in

| Time | What happened | Source |
| --- | --- | --- |
| 12:13 | Asked Grok Bot in the existing one-to-one chat to add `grok-gadgets` with the fixed URL and OAuth sign-in. It found the 13 October quick-tunnel server still configured and asked to replace it. The replacement was confirmed | Bot, screen |
| 12:14:00–12:14:16 | Two 401s on `/mcp`, three `oauth_client_registered` | Log |
| 12:14 | **Authorize**, then **Continue** in "Connect to grok-gadgets" | Screen |
| 12:14:32 | `oauth_sign_in_requested`, code `3B4D-K78K`; the page on the tunnel hostname showed the same code | Log, screen |
| 12:14:45 | `oauth_sign_in_approved` as `grok-bot` with `oauth approve` | Log |
| 12:14:48 | `oauth_token_issued` to `grok-bot`; refresh valid to 12 November | Log |

## Tool calls

Every `mcp_tool_call` on 13 October after the sign-in. The connector backend's client name is left out, as in the [13 October Remote HTTPS record](grok-remote-https-2026-10-13.md).

```json
{"ts": "2026-10-13T12:15:18.082082+00:00", "token": "grok-bot", "remote": true, "tool": "gadgets_list_devices", "outcome": "ok", "duration_ms": 0.6, "bytes_in": 2, "bytes_out": 1921}
{"ts": "2026-10-13T12:15:34.812452+00:00", "token": "grok-bot", "remote": true, "tool": "gadgets_command", "device_id": "oledkit-84c7bb57148c", "capability": "display.text", "outcome": "ok", "status": "executed", "duration_ms": 110.2, "bytes_in": 123, "bytes_out": 607}
{"ts": "2026-10-13T12:15:58.713592+00:00", "token": "grok-bot", "remote": true, "tool": "gadgets_get_state", "device_id": "oledkit-84c7bb57148c", "outcome": "ok", "duration_ms": 1.0, "bytes_in": 36, "bytes_out": 1917}
{"ts": "2026-10-13T12:16:51.559523+00:00", "token": "grok-bot", "remote": true, "tool": "gadgets_list_devices", "outcome": "ok", "duration_ms": 0.5, "bytes_in": 2, "bytes_out": 1920}
{"ts": "2026-10-13T12:22:48.613096+00:00", "token": "grok-bot", "remote": true, "tool": "gadgets_command", "device_id": "oledkit-84c7bb57148c", "capability": "display.text", "outcome": "ok", "status": "executed", "duration_ms": 130.0, "bytes_in": 129, "bytes_out": 619}
{"ts": "2026-10-13T12:26:06.713155+00:00", "token": "grok-bot", "remote": true, "tool": "gadgets_read_events", "outcome": "ok", "duration_ms": 0.7, "bytes_in": 43, "bytes_out": 143}
{"ts": "2026-10-13T12:30:40.232237+00:00", "token": "grok-bot", "remote": true, "tool": "gadgets_read_events", "outcome": "ok", "duration_ms": 0.3, "bytes_in": 75, "bytes_out": 733}
{"ts": "2026-10-13T12:39:02.793448+00:00", "token": "grok-bot", "remote": true, "tool": "gadgets_list_devices", "outcome": "ok", "duration_ms": 0.8, "bytes_in": 2, "bytes_out": 1903}
{"ts": "2026-10-13T12:44:34.906954+00:00", "token": "grok-bot", "remote": true, "tool": "gadgets_list_devices", "outcome": "ok", "duration_ms": 0.5, "bytes_in": 2, "bytes_out": 1903}
```

The log does not show which app or network sent a call. "From the phone" and "on cellular" are the owner's reports.

| Check | From | Result | Source |
| --- | --- | --- | --- |
| List gadgets | Mac | `gadgets_list_devices` ok | Log |
| "Day 1 from my Mac" on the OLED | Mac | `display.text` `executed`; the owner saw the text | Log, owner |
| Gateway restart, then a call | Mac | `launchctl kickstart -k`: `serve_stopped` 12:15:45.169, `serve_started` 12:15:45.753, board `lan_hello` 12:15:46.861. `gadgets_get_state` at 12:15:58 as `grok-bot`, with no sign-in lines in between | Log |
| `remote off`, then a call | Mac | `http_rejected` 503 `remote_disabled` at 12:16:21. Grok Bot said the gateway refused with "Remote access is turned off on this gateway" and did not retry | Log, Bot |
| `remote on`, then a call | Mac | `gadgets_list_devices` ok at 12:16:51, no new sign-in | Log |
| OLED text from the phone on cellular, Wi-Fi off | iPhone | `display.text` `executed` at 12:22:48; the owner reported that it worked | Log, owner |
| BOOT, then "read my gadget events" (first try) | iPhone, cellular | A wire came loose during the press. The owner reconnected it and replugged USB: `lan_disconnected` 12:25:44, `lan_hello` 12:25:46, OLED **Online Grok Bot**. The read at 12:26:06 returned no events (143 bytes); Grok Bot said "No events yet" | Log, owner, Bot |
| BOOT, then "read my gadget events" (second try) | iPhone | The read at 12:30:40 returned 733 bytes, so it held events. The gateway does not log event bodies. The owner reported that this step worked | Log, owner |
| Mac asleep | iPhone | Sleep 12:32:44 (on power), wake 12:33:19 (macOS power log). During sleep Grok Bot reported "Cloudflare returned a 502 Bad Gateway"; no line reached the gateway, and nothing was queued. After the wake the tunnel registered 4 connections at 12:33:21–24, and the board sent `lan_hello` at 12:33:25. The stale session closed at 12:33:27 | macOS log, Bot, log |
| A call after the wake | iPhone | `gadgets_list_devices` ok at 12:39:02; the owner reported that it worked | Log, owner |

## Mac restart

The owner restarted the Mac and logged in. No one touched the gateway, the tunnel or the board.

| Time | Event | After boot | Source |
| --- | --- | --- | --- |
| 12:41:27 | `serve_stopped`; `cloudflared` "no more connections active and exiting" | — | Log |
| 12:41:48 | Boot (`kern.boottime`) | 0 s | macOS |
| 12:42 | Console login (to the minute, from `last`) | 12–71 s | macOS |
| 12:42:53 | `cloudflared` "Starting tunnel" | 65 s | Tunnel log |
| 12:42:54 | `serve_started` `0.1.0a12`; first tunnel connection registered (4 by 12:42:57) | 66 s | Log, tunnel log |
| 12:43:00 | Board `lan_hello`, **Online** | 72 s | Log |
| 12:44:34 | `gadgets_list_devices` ok as `grok-bot` from the phone, no new sign-in. Grok Bot reported the board online with a blank screen, and said its boot ID had changed since 12:39, so the board itself had restarted | — | Log, owner, Bot |

The board restart fits a board powered from the Mac's USB port after the replug at 12:25. That was not checked. `serve` listened within a minute of login. Before the fix in gateway [#115](https://github.com/adidshaft/grok-gadgets-gateway/issues/115) the owner saw about 90 seconds after login.

## Usage

| Reading | Page | Value | Time |
| --- | --- | --- | --- |
| R0 desktop | Settings → Usage & Billing, **Weekly usage limit** | "1% used", "Resets in 4 days"; on-demand "None" | 12:15 |
| R1 desktop | same | "1% used", "Resets in 4 days" | 12:45 |

`grok-gadgets-gateway usage --token grok-bot --since 2026-10-13T12:14 --until 2026-10-13T12:46`:

```text
total:  calls=9  errors=0  commands=2  duration_ms=244.6  bytes=12080
by token:
  grok-bot  calls=9  errors=0  commands=2  duration_ms=244.6  bytes=12080
by device:
  -  calls=6  errors=0  commands=0  duration_ms=3.4  bytes=8649
  oledkit-84c7bb57148c  calls=3  errors=0  commands=2  duration_ms=241.2  bytes=3431
by capability:
  -  calls=7  errors=0  commands=0  duration_ms=4.4  bytes=10602
  display.text  calls=2  errors=0  commands=2  duration_ms=240.2  bytes=1478
by day:
  2026-10-13  calls=9  errors=0  commands=2  duration_ms=244.6  bytes=12080
Days are UTC. Counts come from this gateway's request log only.
```

`--calibrate 0 --unit "% weekly usage"` over the same window saved "0 % weekly usage per call". The page shows whole percent only, so a change below one point reads as zero. The saved rate was deleted, because it would make every later estimate zero. **Not calibrated.** The session used less than one point of the weekly allowance. It had 9 tool calls and about 12 prompts: 6 from the Mac and 6 from the phone, as the owner reported. `--calibrate` accepted a zero change without a warning.

## Not done

- A second, separate day of use.
- A calibrated usage rate.
- Another person's setup.
