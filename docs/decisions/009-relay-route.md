# ADR 009 — Builder-to-end-user route: a relay that gadgets connect out to

**Date:** 13 October 2026

**Status:** Accepted for stage 1 on 14 October 2026 ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/mac-free-route-2026-10-13.md)); released in gateway 0.1.0-alpha.13 and ESP32 SDK 0.2.0-alpha.14. Stages 2–5 remain proposed. The owner decides whether the project ever runs a shared relay.

**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)

**Issues:** hub [HUB-ADR-009 #260](https://github.com/adidshaft/grok-gadgets/issues/260), [HUB-RELAY-001 #261](https://github.com/adidshaft/grok-gadgets/issues/261); gateway GW-RELAY-001, GW-RELAY-002, GW-RELAY-003; ESP32 ESP-RELAY-001, ESP-RELAY-002; ESP32 [#72](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/72) (ESP-ONBOARD-001, later stage)

## Context

[ADR 007](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/007-grok-bot-remote-https.md) and [ADR 008](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/008-daily-native-route.md) verified the owner’s route for one day: Remote HTTPS with owner-approved OAuth sign-in, through a tunnel to `127.0.0.1:8766` on the owner's Mac. The Wi-Fi kit reaches the same Mac through the private LAN TLS listener ([ADR 005](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/005-wifi-device-route.md)).

The Mac is the weak link. On 13 October 2026, while it slept, Grok Bot got a 502 from the tunnel and nothing was queued. After a restart the gateway listened 66 s after boot and the board was Online at 72 s ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md)). The kit also works only on the Mac's own network.

The owner's goal: a builder designs a gadget with the SDKs and gives or sells it. The end user has Grok Bot on an iPhone, a Mac or a PC, owns no developer tools, and installs nothing on a computer. Setup must be as simple as possible.

What exists already: the gateway is close to a single-operator relay. It has OAuth sign-in, named tokens, per-token limits and rotating logs. It also has usage reports, a shared device server and a local CA. The ESP32 `WifiLink` pins a provisioned CA, carries the device token in `hello`, polls on one TLS socket and stores settings in NVS. The Linux SDK agent connects to loopback only.

Grok Bot has no documented inbound webhook, so a device event cannot wake it (ADR 005). Grok Bot adds a Remote HTTPS server from chat with a URL, then uses OAuth. The desktop connection also works from the phone (ADR 007).

## Proposed decision

### 1. Topology

A **relay** is the existing gateway, run on an always-on Linux host with a public name. Gadgets connect **out** to it over TLS. Grok Bot connects to it as a Remote HTTPS server with OAuth sign-in, exactly as in ADR 007. The gadget opens an outbound connection. The relay host must accept inbound device TLS connections. A home-hosted relay needs a separately reviewed reachability plan.

```text
Grok Bot (Mac and iPhone tested; other apps unverified) ─HTTPS + OAuth─▶ relay  gadgets.example.net
                                             ├─ /mcp  six tools, scoped per account (stage 3)
                                             ├─ sign-in: owner CLI (stage 1), account flow TBD (stage 3)
                                             └─ devices.example.net:8443  TLS device listener, pinned CA
                                                   ▲ outbound TLS, protocol 0.1.0
home Wi-Fi ── ESP32 gadget (no port forwarding, no computer at home)
```

### 2. Device transport

- Protocol **0.1.0 is unchanged**: LF-delimited JSON frames over one TLS socket, hello with the device token, poll, ack, state, events.
- The gateway gains `serve --device-listen HOST:PORT` (default port 8443). It uses the same `DeviceServer` as loopback and LAN. Unlike `--lan-listen`, it may bind a public address and accept peers from any address. Proposed per-address limits include 20 new connections each minute, a pending-hello cap and a 5-second handshake. It logs `device_connected`, `device_hello`, `device_auth_rejected`, `device_tls_failed`, `device_rate_limited` and `device_disconnected` with the peer address and never a token. The private-peer filter of ADR 005 stays on `--lan-listen` only.
- `device-cert NAME` issues the listener certificate for a public DNS name from the `init` CA (`lan-cert` keeps its name and behaviour). The gadget verifies the certificate against that name, as it does for `.local` names today.
- Trust: the gadget pins the relay operator's CA, written at provisioning or at the factory. The firmware checks names but leaves expiry unchecked. This is a security limitation. CA rotation needs provisioning again (ADR 005). Public-root trust and CA rotation need a separate review before use. Do not promise them as tested routes.
- No client certificates. The device token stays the credential.
- Idle poll interval over the internet: 500 ms, the upper end of what the protocol already allows. A long-poll field (`wait_ms`) is a later protocol version, not part of this decision.
- **WebSocket is deferred.**

  It could put device traffic behind a CDN or the MCP tunnel. It also needs new firmware, server and SDK transports. The proposed first host has a public device address. Revisit only if a CDN front becomes a requirement.

### 3. Identity, claim and tenancy (staged)

- **Stage 1 (Phase 9):** one operator, the owner. Sign-in approval by `oauth approve` on the relay host or over SSH, as today. Device tokens from `enroll`.
- **Stage 3 (Phase 11):** ADR 011 must define stable account identity and its binding to OAuth authorization. ADR 011 must separate account authentication from the one-time gadget claim flow. The relay would return a temporary claim code in an additive hello field. A display could show it. Displayless gadgets need a reviewed label and claim design. Possession can support a gadget claim; it does not establish account identity. Every tool call is scoped to the caller's account: `gadgets_list_devices` lists only claimed devices, `gadgets_command` refuses others. New tools `gadgets_claim` and `gadgets_remove`, and a share code for a second account. Device tokens are stored as SHA-256 hashes. A proposed reset keeps device identity but clears user settings. Server-side ownership transfer and revocation need ADR 011 before implementation.
- The operator CLI keeps working for tinkerers who run their own relay.

### 4. Hosting model

| Option | Who runs it | Fit |
| --- | --- | --- |
| Builder-hosted relay | The builder, for the gadgets they ship; one deploy serves their customers | **Primary.** Open source; one command; the builder's domain |
| Self-hosted by a tinkerer | The person, on a VPS or a home Linux box | Same software, same command |
| Project-run shared relay | The project, for builders without hosting | **Separate owner decision** (Phase 13): ongoing cost, abuse handling, privacy, terms. Nothing in this design requires it |
| Serverless rewrite | The project or builder, on a workers platform | **Rejected for now:** needs WebSocket, durable per-device objects and a rewrite of a tested OAuth server, for a few users |

The gateway stays one Python package. The relay is `grok-gadgets-gateway serve` with the flags above, in a container or a user service. The owner's named tunnel can serve `/mcp` from the relay host; the device listener uses the host's own address with a DNS-only record.

### 5. Privacy and logs

The relay sees device IDs, capabilities, commands, reported state and events. Provisioning must not send Wi-Fi credentials to the relay. Custom gadget payloads need their own privacy review. The request log file is for the operator: it records command arguments with secret fields redacted, and the state that a state read returned. It never records tokens. A multi-tenant relay must review this before stage 3. Retention follows the existing rotation (5 MiB, 5 files). A builder's page shows only usage counts per device.

### 6. Stages

| Stage | Phase | Scope |
| --- | --- | --- |
| 1 | 9 Mac-free route | Public device listener, DNS names, container example, owner's kit through a relay host |
| 2 | 10 Setup without a cable | Setup hotspot and captive page on the gadget; factory identity separate from user settings |
| 3 | 11 Claim your gadget | Accounts, claim codes, scoped tools, hashed device tokens |
| 4 | 12 Builder kit | One-command deploy, batch identities and labels, builder page, Linux SDK remote transport |
| 5 | 13 Shared relay | Owner decision only |

## Design gates before implementation

- Phase 9 stays single-operator. Do not expose multiple customers before Phase 11 isolation tests pass.
- Set global connection and memory limits as well as per-address limits. Test shared NATs and distributed connection floods.
- Measure internet latency and polling load. There is no verified device-count capacity yet.
- OAuth identifies a client authorization, not automatically a stable person. ADR 011 must define account identity and recovery.
- A claim code proves temporary possession. It must not silently transfer ownership or merge accounts.
- Define one-time claim codes, expiry, authenticated sharing and server-side revocation. Printed labels must not become permanent account credentials.
- A local reset cannot alone revoke server access. Define an authenticated transfer and factory-reset reconciliation flow before shipping.
- Stage 1 commands (`serve --device-listen`, `device-cert`, `wifi-provision --gateway`) are released. The later-stage flags, stores and protocol additions remain design targets.
- Host, device hostname, tunnel migration, flashing and releases require separate owner decisions.

## Threat model (relay)

| # | Threat | Control | Stage |
| --- | --- | --- | --- |
| R1 | Token guessing on the public device port | Tokens 16–256 random characters; one error for unknown and wrong; 20 new connections a minute per address; 5 s handshake; hello timeout | 1 |
| R2 | Handshake or pending-hello flood | Per-address pending cap; required global session, pending-handshake and memory caps; one `device_flood` line a minute while hit | 1 |
| R3 | Device port tunnelled or proxied by mistake | The device listener refuses HTTP and logs it, as port 8765 does today | 1 |
| R4 | OAuth floods, stolen or refreshed tokens, abuse with a live sign-in | ADR 008 T1–T8, applied per account | 1, 3 |
| R5 | Claim-code guessing | 7+ characters from a 32-character alphabet; new code per boot; 10-minute expiry; per-address and per-device limits; the code stops working once claimed | 3 |
| R6 | Cross-tenant read or command | Account scope checked in every tool; a regression test per tool | 3 |
| R7 | Relay host or operator compromise | Hashed device tokens; no Wi-Fi secrets; redacted arguments in the operator's log; short retention; released versions; OS updates; the operator's view is documented | 1, 3 |
| R8 | Lost or opened gadget | The token grants that device only; `revoke`; flash encryption off is documented (ADR 005) | 1 |
| R9 | Relay outage | No queueing; gadget backoff with jitter; honest status; `remote off` and `revoke` still work | 1 |
| R10 | Shared relay cost and abuse | Per-account limits; owner decision; not built | 5 |

## Consequences

- The gateway binds a public address for the first time. It is off by default, TLS-only, token-only, rate-limited and logged.
- The kit needs new firmware and provisioning with a DNS name. One USB flash on the Mac until stage 2 tooling exists.
- The owner's Mac can sleep or stay off once the relay host runs; the Mac is no longer part of the daily path.
- Hub docs gain "Run the gateway away from your Mac"; the website shows Today, Next and Later.
- The Linux SDK's loopback-only rule stays until stage 4.
- Nothing hosted by the project exists until stage 5 is decided.

## Acceptance (stage 1)

- Gateway: Test public binding, peer handling, global and per-address limits, HTTP rejection and log privacy. Test DNS certificates, container setup and the real Linux service.
- ESP32: provisioning accepts a DNS name; host tests; the Wi-Fi build compiles; the status row shows `Relay...` while connecting.
- Owner, on the kit at home and the iPhone: Observe Online through the relay. Show text from the iPhone on cellular while the Mac sleeps. Test BOOT, reboot recovery, remote access controls, revocation and wrong-CA rejection. Record in `docs/verification/mac-free-route-2026-10-*.md` with the gateway log lines and the owner's observations.

## Not in scope

Later stages cover cable-free setup, accounts, claims, builder tooling and the shared-relay decision. Stage 1 excludes WebSocket, long-poll, OTA, Home Assistant bridging and Team Bots.
