# Mac-free route — 13 October 2026

Phase 9 ([#261](https://github.com/adidshaft/grok-gadgets/issues/261), [ADR 009](../decisions/009-relay-route.md), stage 1). The owner's ESP32-S3 OLED kit connected out to a gateway on an always-on Linux server, not the Mac. Grok Bot on the iPhone, on cellular, showed text on the OLED while the Mac slept. Times are UTC; the owner's local evening ran past midnight, so their local date was 14 October. The owner authorized each step.

Evidence levels:

- **Log**: the relay's request log, read after each step.
- **Mac log**: the Mac's power log (`pmset -g log`).
- **Owner**: what the owner saw.
- **Bot**: Grok Bot's reply, which is narrative only.

| Item | Value |
| --- | --- |
| Relay host | A small cloud server the owner already rented (1 vCPU, 512 MB RAM, Ubuntu 24.04, 1 GB swap file). No new paid resources |
| Gateway | Development commit `c771d99` from `dev` (version string `0.1.0a12`), installed as a user tool, run by `service install --allowed-host --oauth --device-listen 0.0.0.0:8443` as a systemd user unit with linger |
| Names | `gadgets.example.net` through the owner's Cloudflare named tunnel to `127.0.0.1:8766`; `devices.example.net`, a DNS-only record that points at the server |
| Tunnel | `cloudflared` 2026.7.3 as a system service on the server. The Mac's tunnel agent was stopped and disabled first |
| Firewall | `ufw`: SSH and TCP 8443 only |
| Device | The owner's ESP32-S3 OLED kit, ESP32 SDK `dev` commit `2483f43` (`esp32s3-oled-kit-wifi`), on home Wi-Fi from a USB charger |
| Grok Bot | Desktop app on macOS 27.0; iPhone app |

The container example (`examples/docker`) was built and checked only on the Mac. The server ran the Linux user-service route instead, because 512 MB is tight for a container engine.

## Setup and outside checks

| Check | Result | Source |
| --- | --- | --- |
| `init`, `device-cert devices.example.net`, `enroll` | Key files mode 0600 | Server |
| Tunnel metadata from outside | `200` | Log |
| `POST /mcp` without a sign-in, from outside | `401`, `http_rejected` `invalid_token` | Log |
| TLS on 8443 with the relay's CA and the device name | Verified (OpenSSL return code 0) | Mac |
| TLS on 8443 with the system CA bundle | Refused | Mac |
| Plain HTTP to 8443 | No HTTP reply; `device_tls_failed` | Log |
| Ports 8765 and 8766 from outside | Closed | Mac |

## Kit through the relay

The kit was flashed once on the Mac over USB. The owner then provisioned it in their own terminal with `wifi-provision --gateway devices.example.net --ca … --credentials …` and deleted the copied files.

| Time | What happened | Source |
| --- | --- | --- |
| 19:11:15 | `device_hello` from `oledkit-84c7bb57148c` on the relay listener | Log |
| 19:11 | The OLED showed **Online** on a USB charger | Owner |
| 19:28:57–19:30:21 | The kit dropped, failed TLS a few times, then said hello again by itself. The log does not show why | Log |

## Grok Bot sign-in

The relay is a new gateway, so Grok Bot signed in again. A computer-use session drove the desktop app. The sign-in page showed a code. Exactly one sign-in was waiting, and its code matched the page. It was approved as `grok-bot` with `oauth approve` over SSH.

| Time | What happened | Source |
| --- | --- | --- |
| 19:27:27–19:27:57 | 401s on `/mcp` and four `oauth_client_registered` | Log |
| 19:28:01 | `oauth_sign_in_requested` | Log |
| 19:28:37 | `oauth_sign_in_approved` as `grok-bot` | Log |
| 19:28:38 | `oauth_token_issued`; refresh valid to 12 November | Log |

The client's registered name is the connector's own label and is not shown here. Any caller can choose that name. The code match on the owner's screen was the check.

## The main check: phone on cellular, Mac asleep

| Time | What happened | Source |
| --- | --- | --- |
| 20:17:40 | The Mac entered sleep (lid closed) | Mac log |
| 20:17:43–20:17:53 | A 10-second dark wake for network housekeeping, then sleep again | Mac log |
| 20:19:13 | `mcp_tool_call` `gadgets_command` `display.text` `executed`, `grok-bot`, `remote: true` | Log |
| 20:19 | The OLED showed "Mac asleep". The iPhone was on cellular with Wi-Fi off | Owner |
| 20:20 | The owner pressed BOOT once | Owner |
| 20:20:36 | `mcp_tool_call` `gadgets_read_events` ok | Log |
| 20:20 | Grok Bot reported one press, then a release about 0.18 seconds later, and no lost events | Bot |
| 20:20:57 | The Mac woke | Mac log |

```json
{"ts": "2026-10-13T20:19:13.480566+00:00", "event": "mcp_tool_call", "token": "grok-bot", "remote": true, "tool": "gadgets_command", "outcome": "ok", "duration_ms": 184.5, "device_id": "oledkit-84c7bb57148c", "capability": "display.text", "status": "executed", "simulated": false}
{"ts": "2026-10-13T20:20:36.770105+00:00", "event": "mcp_tool_call", "token": "grok-bot", "remote": true, "tool": "gadgets_read_events", "outcome": "ok", "duration_ms": 0.2}
```

The lines are shortened. The log does not show which app or network sent a call. "From the iPhone" and "on cellular" are the owner's reports.

## Recovery and controls

| Check | Result | Source |
| --- | --- | --- |
| `remote off`, then a call from outside | `http_rejected` 503 `remote_disabled` at 19:22:34. Checked with `curl` from the Mac, not from Grok Bot | Log |
| `remote on` | 401 again at 19:22:36 | Log |
| `remote off`, then a call from Grok Bot (14 October) | `remote off` at 05:36:03. The owner asked Grok Bot on the iPhone, about 80 km from home, to list the gadgets: `http_rejected` 503 `remote_disabled` at 05:37:07 | Log, owner |
| `remote on`, then the same request (14 October) | `remote on` at 05:37:17; `mcp_tool_call` `gadgets_list_devices` ok as `grok-bot`, `remote: true`, at 05:37:28 | Log, owner |
| Server reboot | Reboot command 19:22:44; `serve_stopped` 19:22:45.9; system up 19:22:49; tunnel registered 19:23:02; `serve_started` 19:23:03.8; kit `device_hello` 19:23:08.7. **24 seconds**, with no login | Log, server |
| Linux user service at boot ([#22](https://github.com/adidshaft/grok-gadgets/issues/22)) | The systemd user unit started at boot through linger, with nobody logged in | Log, server |
| `revoke` | `device_auth_rejected` `revoked` at 20:24:05; the OLED showed **Token rejected** | Log, owner |
| `enroll --rotate`, then the old token | `device_auth_rejected` `unauthorized` at 20:25:06 and 20:25:32 | Log |
| Re-provision with the new token and the right CA | `device_hello` at 20:26:39 and 20:27:33 | Log |
| First try at a wrong CA | The OLED showed `WiFi...`, `Relay...`, then **Wrong password** and **Check password**. The relay logged no TLS attempt, so this try did not test the CA. The Wi-Fi password was most likely mistyped | Owner, log |
| Provision with a wrong CA, second try | The kit restarted at 20:40:01. From 20:40:20 the relay logged `device_tls_failed` `TLSV1_ALERT_UNKNOWN_CA` every 4–5 seconds: the kit refused the relay's certificate and retried within its backoff. The OLED showed **TLS rejected** | Log, owner |
| Provision with the right CA again | `device_hello` at 20:43:45 | Log |

## Results

| Item | Result |
| --- | --- |
| Online through the relay | **Pass** |
| Mac asleep; iPhone on cellular; `display.text` executed and seen | **Pass** |
| BOOT press, then read events | **Pass** |
| Server reboot to Online | **Pass**: 24 s |
| Linux user service at boot (#22) | **Pass** on this server |
| `remote off`, then on | **Pass**: with `curl` on 13 October and from Grok Bot on the iPhone, away from home, on 14 October |
| Revoke, re-enroll, re-provision | **Pass** |
| Wrong CA rejected by the kit | **Pass**: `TLSV1_ALERT_UNKNOWN_CA` from 20:40:20; **TLS rejected** on the OLED |
| Weekly usage before and after | **Not tested**: the account page shows whole percent; the owner saw no change, so no reading could be paired with the log |

## Limits

- One kit, one server, one evening. No second person ran this route.
- The gateway and firmware were development commits, not releases.
- The server is the owner's own relay. It has one operator and no accounts.
- Today a person needs a USB cable, a terminal and an approval on the server. Phases 10–12 plan to remove those steps for end users.
- The request log file records command arguments with secret fields redacted, for example the displayed text. It never records tokens.
