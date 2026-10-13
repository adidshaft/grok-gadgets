# ADR 008 — Daily native route: a public sign-in endpoint that is safe to leave on

**Date:** 13 October 2026  
**Status:** Accepted on 13 October 2026. The owner chose Cloudflare Tunnel with a named tunnel, a hostname on a domain the owner already controls, and a tunnel that stays on. Result: [daily-route record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md).  
**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)  
**Issues:** [#251](https://github.com/adidshaft/grok-gadgets/issues/251) (HUB-DAILY-001), gateway [#142](https://github.com/adidshaft/grok-gadgets-gateway/issues/142) (GW-DAILY-001), gateway [#115](https://github.com/adidshaft/grok-gadgets-gateway/issues/115)

## Context

[ADR 007](007-grok-bot-remote-https.md) proved the route for one 20-minute session: Grok Bot on the Mac and the iPhone called the six tools through `serve --oauth` behind an account-free quick tunnel. The quick tunnel gets a new hostname on every start, so Grok Bot's server had to be added again each time.

Phase 8 keeps the route on every day, at home and away. The gateway's MCP port then has a fixed public HTTPS name for weeks. Anyone who learns the name can send requests to it. The gateway must stay usable for the owner and safe for the gadgets when that happens. The Mac also sleeps, restarts and changes networks.

```text
Grok Bot (Mac, phone) ─HTTPS─▶ gadgets.example.net ─tunnel─▶ 127.0.0.1:8766  serve --oauth
                                                              127.0.0.1:8765  devices (never tunnelled)
                                                              my-mac.local:8767 Wi-Fi devices (LAN only)
```

## What is exposed

Only port 8766 behind the tunnel. Through it, anyone can reach:

| Path | Without a sign-in | Cost to the gateway |
| --- | --- | --- |
| `/.well-known/oauth-*` metadata | 200 | Small, no state |
| `/mcp` | 401 with the metadata link | Small, no state |
| `/register` (dynamic client registration) | Creates a client record in `oauth/state.json` | **State that persists** |
| `/authorize` | Creates a waiting sign-in and a code | **State, up to 10 minutes** |
| `/oauth/approve` | A waiting page | Small |
| `/token`, `/revoke` | Need a client and a code or token | Small |

Tool calls need an approved sign-in or a named token. The local `default` token never works through the tunnel (403). The device listeners are not on the tunnel.

## Threat model

| # | Threat | Today (gateway 0.1.0a11) | Decision |
| --- | --- | --- | --- |
| T1 | **Registration flood locks the owner out.** A stranger registers 20 clients. | `MAX_CLIENTS = 20`. Clients are never removed, and `state.json` keeps them after a restart. The 21st registration, the owner's next one included, fails until someone edits the file. | Fix (gateway). Prune clients that hold no live token and are older than one hour. When the list is full, remove the oldest client without a live token. A client with a live sign-in is never removed. |
| T2 | **Pending-sign-in flood locks the owner out.** A stranger keeps 8 sign-ins waiting. | `MAX_PENDING = 8`, 10 minutes each. The owner's sign-in fails with `temporarily_unavailable`. | Fix (gateway). At most 2 waiting sign-ins per caller. When the list is full, drop the oldest. The owner approves by code, so an extra waiting code does no harm. |
| T3 | **Shared sign-in budget starves refresh.** Floods spend the single 60-a-minute budget for all sign-in paths. | Grok Bot's hourly refresh on `/token` can get 429, so a working sign-in stops working. | Fix (gateway). Separate budgets: `/register` and `/authorize` get their own small budget per caller and in total; `/token` and `/revoke` keep a separate budget. |
| T4 | **Nobody notices an attack.** | Rejections are `http_rejected` lines in the log only. | Fix (gateway). One `oauth_flood` alert line a minute while a cap or budget is hit, and the same count in `service status`. The optional usage hook can show a local notification. |
| T5 | **A stranger's code is approved by mistake.** | The owner approves a code from `oauth pending`. | Docs: approve only the code that your own sign-in page shows, right after you started it. `oauth pending` shows the client name and when the request started. Never approve a code that you did not start. |
| T6 | **Stolen access or refresh token.** | Access token 1 hour. Refresh token 30 days, replaced at every refresh. Only SHA-256 hashes are stored. | Keep. `oauth revoke grok-bot` ends every sign-in for that name at once. The daily check lists live sign-ins. |
| T7 | **Abuse with a valid sign-in.** | 60 tool calls and 10 commands a minute per name, 8 open requests, 64 KiB bodies, 30 s per request. | Keep. Every call is logged with the name and `"remote":true`. |
| T8 | **The owner needs to stop everything now.** | `remote off` returns 503 to every remote request at once and stays off after a restart. | Keep. It is the kill switch. Then `oauth revoke`, then stop the tunnel. Record the result once in Phase 8. |
| T9 | **A device port is tunnelled by mistake.** | The device port refuses HTTP and logs `device_http_rejected`. The Wi-Fi listener accepts private peers only. | Keep. The tunnel config names `http://127.0.0.1:8766` only. The daily check confirms it. |
| T10 | **Logs fill the disk.** | The request log grows without limit, about 20 KB a day at the owner's use so far. A flood writes much more. | Fix (gateway). Rotate the request log at 5 MiB and keep 5 files. `usage` reads the rotated files too. The service log is small; its size is noted in `service status`. |
| T11 | **The Mac sleeps.** | A sleeping Mac runs neither the gateway nor the tunnel. | Expected. Grok Bot gets an error from the tunnel provider, not a gadget result. Phase 8 records what Grok Bot shows. Docs give the sleep settings for staying reachable on power. |
| T12 | **Restart or reboot.** | The service starts at login (ADR 006). Sign-ins are in `state.json`, so they survive a restart. | Record in Phase 8: a call after a gateway restart with no new sign-in, and the time to Online, to `serve` listening and to a working phone call after a Mac restart (#115). The tunnel client also runs as a per-user service. |
| T13 | **The gateway process is attacked directly.** | Python HTTP server on loopback; TLS ends at the tunnel provider. | Accepted risk for an alpha. Keep the gateway and its dependencies on released versions. |

Caller, for T2 and T3: the address in the tunnel's forwarding header when there is one, otherwise the peer address. Behind a tunnel every peer is `127.0.0.1`, so a caller without a header shares one budget. A caller can forge a header only if it can already reach loopback, which means it runs on the Mac.

What remains: an attacker with many addresses can still delay the owner's first sign-in for minutes. The owner's existing sign-in keeps working (T1 and T3), and `remote off` stops everything. A provider-side rate rule (below) is the next step if this happens.

## Tunnel options

The owner's own domain is required; never `grokgadgets.org`. Prices are from the providers' pages on 13 October 2026.

| | Cloudflare Tunnel | ngrok | Tailscale Funnel |
| --- | --- | --- | --- |
| Own domain | Yes. The domain must be added to Cloudflare, with its DNS there ([setup](https://developers.cloudflare.com/tunnel/setup/)) | Only on Pay-as-you-go ([pricing](https://ngrok.com/pricing)) | No. Only `*.ts.net` names ([Funnel](https://tailscale.com/kb/1223/funnel)) |
| Cost | Tunnel: listed in the $0 Zero Trust plan for up to 50 users ([pricing](https://www.cloudflare.com/teams-pricing/)). Domain: the owner's existing registration | $20 a month plus usage, plus $0.01 per active hour for a custom domain | $0 on the Personal plan ([pricing](https://tailscale.com/pricing)), but no own domain |
| Free-tier limits | No published request cap for tunnels | Free: 1 GB, 20,000 requests a month and a warning page in front of the site | Fixed bandwidth limits, not published |
| Runs as a user service on macOS | `cloudflared service install` without `sudo` installs a login agent ([macOS](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/local-management/as-a-service/macos/)) | Agent service | App or `tailscaled` |
| Extra protection | Provider rate rules on the hostname, if needed | Traffic policy | Tailnet only, not public |
| Fits the constraints | **Yes** | Yes, at a monthly cost | **No** (own domain required) |

**Recommendation:** Cloudflare Tunnel with a named tunnel and one hostname on the owner's domain, for example `gadgets.example.net`. It costs nothing beyond the domain, keeps the same hostname across restarts, and its client runs as a login agent like the gateway. Moving the domain's DNS to Cloudflare is the owner's decision, and so is any account. ngrok is the fallback if the DNS cannot move. The ngrok free tier is not suitable: its warning page and the 20,000-request month do not fit a daily public endpoint.

## Mac sleep

- On battery, or with the lid closed and no external display, the Mac sleeps. The gateway and the tunnel stop. Grok Bot gets an error from the tunnel provider. The board shows **Gateway...** until the Mac wakes. No call is queued or replayed.
- To stay reachable on power: System Settings → Battery → Options → **Prevent automatic sleeping on power adapter when the display is off**. A closed lid still sleeps unless an external display, keyboard and power are connected.
- `caffeinate -s` keeps the Mac awake on power while it runs. The docs show it as an option, not a default.
- The owner decides whether the Mac stays awake. Phase 8 records what Grok Bot shows while it sleeps.

## Decision

1. Keep the route from ADR 007: `serve --oauth` with one `--allowed-host`, and an owner-run tunnel to `127.0.0.1:8766` only. No hosted relay.
2. Fix T1–T4 and T10 in the gateway before the tunnel stays on (GW-DAILY-001). Each fix comes with a regression test.
3. `service status` shows the allowed host, `remote` on or off, live sign-ins, the last Grok Bot call and any flood alert.
4. An example usage hook posts a local macOS notification for each remote call. No external service.
5. The gateway docs add the tunnel client as a user service, a one-minute daily check and the sleep settings.
6. The owner chooses the tunnel provider, the hostname on their own domain, and whether the tunnel stays on. Until then, "keep the tunnel on only while you use it" stays in the docs.

## Acceptance

- Gateway: the fixes above merged, with tests for a full client list, a full waiting list, a refresh during a registration flood and log rotation.
- Owner, on two separate days: logged calls from the Mac and the phone, one from the phone on cellular with Wi-Fi off; a BOOT press read from the phone; a call after a gateway restart with no new sign-in; Mac asleep; `remote off` and on; a Mac restart; **Weekly usage** at the start and the end, run through `usage --calibrate`. Records go in `docs/verification/daily-route-2026-10-*.md`.

## Outcome — 13 October 2026

Gateway `0.1.0a12` with the fixes above ran as the always-on service behind the owner's named tunnel. In one day, Grok Bot called the tools from the Mac and from the iPhone on cellular. BOOT events were read from the phone. The route came back after a gateway restart, `remote off` and on, Mac sleep and a Mac restart ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md)).

Not done: a second separate day, by the owner's choice, and a calibrated usage rate, because **Weekly usage** read 1% before and after. The Mac must stay on and awake; a route without it is outside this ADR.
