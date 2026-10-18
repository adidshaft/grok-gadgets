# ADR 014 — Ready for others: measured capacity, sign-in for the registration change, a clear sign-in page

**Date:** 18 October 2026

**Status:** Proposed on 18 October 2026. The owner took the five decisions below on 18 October 2026. Nothing here is measured yet.

**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)

**Phase:** 13, "Ready for others" ([HUB-READY-001 #363](https://github.com/adidshaft/grok-gadgets/issues/363)). ADR numbers differ from phase numbers. The shared-relay decision is Phase 14 ([#270](https://github.com/adidshaft/grok-gadgets/issues/270)).

**Issues:** gateway [GW-SCALE-001 #181](https://github.com/adidshaft/grok-gadgets-gateway/issues/181), [GW-PROTO-002 #182](https://github.com/adidshaft/grok-gadgets-gateway/issues/182), [GW-COMPAT-002 #176](https://github.com/adidshaft/grok-gadgets-gateway/issues/176), [GW-UX-001 #207](https://github.com/adidshaft/grok-gadgets-gateway/issues/207), [GW-OAUTH-REFRESH-001 #211](https://github.com/adidshaft/grok-gadgets-gateway/issues/211) (closed; residual below); hub [#185](https://github.com/adidshaft/grok-gadgets/issues/185), [#269](https://github.com/adidshaft/grok-gadgets/issues/269)

## Context

Phases 9 to 12a give a builder a relay, phone setup, claim codes, signed updates and a one-afternoon guide. The website already invites an outside builder. Strangers can arrive before four things are true:

1. **Nobody has measured a relay.** No capacity statement exists.
2. **Sign-in uses a registration method the protocol deprecated.** MCP 2026-07-28 prefers Client ID Metadata Documents (an HTTPS URL as `client_id`). It keeps dynamic registration for at least twelve months ([client registration](https://modelcontextprotocol.io/specification/latest/basic/authorization/client-registration)). The Grok Bot connector backend registered by dynamic registration on 13 October 2026.
3. **The sign-in page is plain text.** In the Phase 11 test a person saw one bare field (#207).
4. **Grok Bot on Android has not called a gadget.** Phone setup passed on Android; a Grok Bot call from Android did not happen.

Facts this design depends on (gateway `0.1.0a17`, ESP32 `v0.2.0-alpha.18`, Linux `0.1.0a9`):

- **A relay holds at most 64 gadgets today.** The relay listener accepts 64 sessions plus 32 waiting handshakes (`RELAY_SESSIONS`, `RELAY_PENDING` in `service.py`). The device registry refuses a 65th device ID with `busy` (`domain.py`). Protocol 0.1.0 states the 64-device limit.
- **One source address gets 20 connections a minute and 4 waiting handshakes.** Each session may send 30 frames a second.
- **Gadgets poll all the time.** ESP32 firmware polls every 100 ms and sends state every 3 s (`GrokSession.h`), so about 10.3 frames a second. A Linux agent on a relay polls every 500 ms. A session closes after 15 s without a request.
- **Idle memory is small; polling is the load.** Research estimated tens of KB for each idle TLS connection (asyncio buffers; OpenSSL releases idle buffers). At 100 ms, 1,000 ESP32 gadgets send about 10,000 frames a second to one Python process. That is an estimate, not a measurement.
- **The pinned MCP SDK (`mcp==2.3.0`) looks up clients through one provider hook, `get_client`.** It has no server-side code for metadata documents. The gateway's metadata says `client_id_metadata_document_supported: false`, so a client that follows the specification falls back to registration.
- **Grok Bot's access token lasts 1 hour** (`ACCESS_SECONDS`). Gateway `0.1.0a17` logs refresh results. On 17 October one automatic refresh was observed. Two earlier `401 invalid_token` failures on `0.1.0a16` stay unexplained.
- **Grok Bot runs on iPhone (iOS 18+) and Android 9+** with the same Bots and connectors ([mobile](https://docs.x.ai/grok-bot/mobile)).

## Decision

### 1. Capacity: measure, then state only what was measured (gateway #181)

**A fleet tool.** `grok-gadgets-gateway fleet` runs N simulated gadgets against a relay's device port. Each gadget:

- It connects with TLS, pins the relay CA and checks the name, as the ESP32 does.
- It sends a protocol 0.1.0 hello with its enrolled token.
- It polls at the firmware rate (100 ms by default; `--poll-ms`) and sends state every 3 s.
- It acknowledges each command at once with `executed`.

The tool ramps up within the relay's per-address limits (18 new connections a minute by default). It does not bypass them, so the test exercises the real relay. A ramp to 1,000 gadgets takes about an hour.

A driver sends `gadgets_command` calls through the relay's MCP endpoint at a fixed rate (1 a second by default) to random gadgets. It times each call from request to the `executed` result.

`grok-gadgets-gateway fleet sample --pid PID` runs on the relay host. It writes the gateway's CPU share and resident memory every 5 s.

**A relay option.** `serve --max-devices N` (default 64, at most 2,000) sets the session limit and the registry limit together. Waiting handshakes stay at 32. The test needs it for 200 and 1,000 gadgets. A builder needs it to go past 64.

**The run.** The host has 512 MB of memory and one virtual CPU. We run 50, 200 and 1,000 gadgets, each for 15 minutes after the ramp:

| Measure | From |
| --- | --- |
| Gateway CPU share (mean, p95) | `fleet sample` |
| Gateway resident memory (peak) | `fleet sample` |
| Command latency (p50, p95, p99) | the driver |
| Frames a second offered and answered | the fleet tool |
| Sessions refused, dropped or `busy` | the fleet tool and the relay log counts |

The record keeps the raw CSV files and the command lines. It holds no token, address or host name.

**What the docs say.** The support matrix states the numbers measured on that host, with the host size, gateway version and poll rate. It makes no claim beyond the measured sizes. "One small host" is a measurement, not a guarantee. If a size fails, the docs say so and give the largest size that passed.

**Long-poll follows the numbers (gateway #182).** Take 1,000 gadgets polling every 100 ms. If p95 command latency stays under 2 s and CPU under 70 %, the size passes. Then long-poll goes to Later. Otherwise, or if the owner decides now, it ships as follows:

- A poll may carry `wait_ms` (100–10,000). The device requests it; the relay never asks for it.
- The relay holds that poll until a command, an update offer or a claim change is ready, or until `wait_ms` passes. Then it answers as it does today.
- A relay before this change answers the field with `invalid_request`. The device then polls without it until the next boot, as with `claim` and `update`.
- A device that sends no `wait_ms` gets the same replies as today. Protocol 0.1.0 devices change in nothing.
- The ESP32 SDK and Linux SDK opt in with a build or constructor setting. The kit needs one signed update to use it.

### 2. Sign-in by Client ID Metadata Document (gateway #176)

When `client_id` is an HTTPS URL, `get_client` fetches and checks the document before the sign-in starts:

- HTTPS only, port 443, a public DNS name; no IP-literal hosts, no user info, no fragment.
- The resolved addresses must all be public: no private, loopback, link-local, shared or reserved ranges. The connection goes to the checked address.
- At most 5 s and 16 KB; no redirects; `application/json` only.
- The document's `client_id` must equal the URL exactly. `redirect_uris` must be HTTPS, or `http` on loopback, as for registration. `token_endpoint_auth_method` must be `none`.
- A cache keeps a good document for 10 minutes, at most 32 documents. A changed document replaces the cached one at the next fetch.
- The sign-in page shows `client_name` as self-declared ("calls itself …").
- Floods: fetches share the sign-in budgets of hub ADR 008. The relay logs a failed fetch once a minute (`oauth_cimd_rejected` with reason; never the document).

Dynamic registration stays on. The metadata says `client_id_metadata_document_supported: true` only after the tests pass. Accounts mode stays the same. A metadata-document client has one `client_id` for every person. So the account still comes from the claim code and the refresh-token family, never from `client_id` (ADR 011).

Proof: a scripted client signs in by metadata document against a test relay, and registration still works. **Grok Bot via metadata document is Not tested** unless the relay log shows Grok Bot doing it.

### 3. A clear sign-in page (gateway #207)

- Project mark and colours, inline; phone-first, large type; light and dark.
- One code field shown as `XXXX-XXXX`, upper case, paste-friendly; a drawing of a gadget screen showing `Code XXXX-XXXX`.
- Plain errors: "That code did not work. Codes change every 10 minutes." and the attempts left.
- The page shows the name the client gives as self-declared.
- Kept: the redirect straight back to Grok Bot after a right code (GW-CLAIM-005), and a page policy without `form-action` (GW-CLAIM-006).
- Kept: `default-src 'none'`, no scripts, no external assets, `X-Frame-Options: DENY`, `no-store` and `no-referrer`.

Proof: tests for content and headers; screenshots at phone size reviewed by the owner; then a stranger-style sign-in on the live relay.

### 4. Sign-in lifetime (#211 residual)

The access token keeps its 1-hour lifetime. The owner uses Grok Bot on three ordinary days with no fresh sign-in. The relay log must show `oauth_token_refreshed` lines and no `401` after an `oauth_access_expired`. If the watch shows a refresh failure, a new issue proposes a fix under the ADR 008 threat model. The lifetime does not change without that issue.

### 5. Platform statements

- **Android:** Grok Bot on Android calls a gadget through the relay (claim, then text on the kit). Until the owner sees that, the support matrix says "Grok Bot on Android: Not tested".
- **Windows:** the gateway, the SDKs and a relay are not tested on Windows. A relay runs on Linux. The docs say "Windows: Not tested" and do not claim it.

### 6. Calls for testers and builders

Drafts in `community/drafts/phase13/` stay unposted: a tester call (#185), a builder call (#269) and one report template. The template asks for versions, steps, Pass / Fail / Not tested, what the tester saw and what they redacted. The owner posts them. Reports go to the issue; security reports go by private email.

### 7. Proof

Record `docs/verification/ready-for-others-2026-10-DD.md`. Each item says Pass, Fail or Not tested, the tier (software, owner, outside), and the log lines.

| Item | Tier |
| --- | --- |
| Load test at 50, 200, 1,000 on the chosen host | Owner-run host, software gadgets |
| Metadata-document sign-in by a scripted client; registration still works | Software |
| Grok Bot via metadata document | Not tested unless the log shows it |
| Three days of Grok Bot with no fresh sign-in | Owner |
| Sign-in page screenshots, then a stranger-style sign-in on the live relay | Owner |
| Grok Bot on Android: claim and text on the kit | Owner, if a phone is available |
| Kit on a released image by signed update, if firmware changed | Owner |

## Threat model

| # | Threat | Control |
| --- | --- | --- |
| R1 | A metadata URL makes the relay fetch internal addresses (SSRF) | HTTPS on 443, public DNS names only, every resolved address checked, connect to the checked address, no redirects, size and time caps |
| R2 | A metadata document claims another client's name | `client_name` shown as self-declared; the claim code or the operator's approval decides every sign-in |
| R3 | Fetch floods | Shared sign-in budgets, a 32-entry cache, one log line a minute |
| R4 | `--max-devices` raised past what the host carries | Docs give the measured sizes; the relay logs `device_flood` at the limit |
| R5 | A load test leaks data | Only test tokens on a fresh host; the record holds counts, never tokens, addresses or names |
| R6 | The new page breaks the phone sign-in sheet | Redirect and page-policy tests stay; a phone-size check before release |
| R7 | Long-poll holds sockets the relay needs | `wait_ms` capped below the 15 s idle timeout; held polls count in the session limit |

## Owner decisions

Taken on 18 October 2026. The load test runs on a fresh droplet, destroyed after. Long-poll follows the numbers. The owner borrows an Android phone; the docs state Windows as Not tested. The calls go to GitHub issues #185 and #269 first. On the same day the owner's account held only the live relay droplet, so no earlier test host remained to delete.


1. **Load-test host:** a fresh 512 MB droplet for a few hours, destroyed after (well under US$1 at hourly billing; the fleet runs from the Mac). Or the Mac only, which gives no relay-host numbers. Recommendation: the droplet.
2. **Long-poll:** now, or Later unless the numbers ask for it. Recommendation: Later; decide from the numbers.
3. **Android phone:** borrow one with Grok Bot for one session (the Phase 11 second account). Recommendation: borrow.
4. **Windows:** state "Not tested", or find a Windows computer to test. Recommendation: state "Not tested".
5. **Where the calls go:** GitHub issues #185 and #269 only, or also r/GrokGadgets and the owner's X account. Recommendation: the issues first; the owner decides on the others.

## Not in scope

- The shared-relay decision (Phase 14, #270), connection research (#336), hardware identity (ESP32 #126), the Home Assistant bridge (HA #62) and gateway #221.
- Posting, secure boot, a kit binary, mains switching and words that encourage selling gadgets.
