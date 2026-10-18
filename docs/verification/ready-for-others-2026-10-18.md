# Ready for others — from 18 October 2026

Phase 13 ([#363](https://github.com/adidshaft/grok-gadgets/issues/363), [ADR 014](../decisions/014-ready-for-others.md)). Times are UTC. Each item says Pass, Fail or Not tested, and its tier.

Tiers:

- **Software:** tests and scripted clients; no person, phone or gadget.
- **Fresh host:** a new 512 MB droplet, created for the load test and destroyed after it. Simulated gadgets only.
- **Owner:** the owner's relay, kit, phones and Grok Bot, and what the owner saw.

## Summary

| Item | Result | Tier |
| --- | --- | --- |
| Load test at 50 and 200 gadgets, 100 ms polls | Pass | Fresh host |
| Load test at 1,000 gadgets, 100 ms polls | Fail (CPU from about 400; out of memory at about 660) | Fresh host |
| Load test at 1,000 gadgets, long-poll 2,500 ms | Pass | Fresh host |
| Sign-in by Client ID Metadata Document, scripted client | Pass | Software |
| Registration still works beside documents | Pass | Software |
| Grok Bot via a metadata document | Not tested | — |
| Sign-in page screenshots reviewed by the owner | Pass, after one change | Owner |
| Stranger-style sign-in on the live relay | Not tested yet | Owner |
| Three days of Grok Bot with no fresh sign-in | Not tested yet | Owner |
| Grok Bot on Android: claim and text on the kit | Not tested yet | Owner |
| Kit on a released image by signed update | Not tested yet | Owner |

## Load test (tier: fresh host, 18 October 2026)

**Host:** DigitalOcean `s-1vcpu-512mb-10gb` in Bangalore (1 vCPU, 458 MB usable), Ubuntu 24.04, Python 3.12.3, OpenSSL 3.0.13. The droplet was created for this test and destroyed after it.

**Relay:** gateway `dev`, `serve --device-listen 0.0.0.0:8444 --max-devices 1000 --commands-per-minute 120` with the example name `devices.example.net`, no tunnel and no OAuth. A fresh relay process for each size.

**Gadgets:** `fleet run` from the owner's Mac over the internet (round trip about 50 ms), from one address, so the ramp stayed at 18 new connections a minute. TLS with the relay CA and name, a hello, a poll every 100 ms (or a waiting poll), state every 3 s. One `gadgets_command` a second through MCP over an SSH forward, timed until `executed`. Each size ran 15 minutes after the ramp. CPU and memory are the relay process's, from `fleet sample` every 5 s in that window.

### Final code (gateway `70fbd43`)

| Gadgets | Polls | Online at end | Frames answered a second | Command latency p50 / p95 / p99 | Commands executed | Relay CPU mean / p95 | Relay memory peak |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 100 ms | 50 | 499 | 181 / 274 / 333 ms | 900 of 900 | 20 % / 26 % | 78 MB |
| 200 | 100 ms | 200 | 1,991 | 201 / 304 / 383 ms | 900 of 900 | 61 % / 72 % | 88 MB |
| 1,000 | long-poll 2,500 ms | 1,000 | 713 | 167 / 406 / 1,596 ms | 899 of 900 (1 in flight at the end) | 67 % / 75 % | 137 MB |

No session dropped in any size. The relay logged no error and no `device_flood`.

A first run of the 50 size on this code was discarded: the Mac also ran builds and test suites, and the command driver lost its MCP session after 388 commands. The relay log showed no error. The rerun above ran alone.

### Earlier code and what it found

| Run | Code | Result |
| --- | --- | --- |
| 50, 100 ms | `f55acd8` | All 50 online; 900 of 900 executed; latency p50 202, p95 286, p99 410 ms; CPU mean 18 %, p95 22 %; 77 MB |
| 200, 100 ms | `f55acd8` | All 200 online; 900 of 900 executed; latency p50 217, p95 311, p99 394 ms; CPU mean 62 %, p95 73 %; 131 MB |
| 1,000, 100 ms | `f55acd8` | **Fail.** CPU mean 90 % from about 400 gadgets. At about 660 gadgets the kernel killed the relay for memory (249 MB). 136 sessions dropped before that |
| 1,000, long-poll | `9a9dd76` | **Fail.** CPU stayed low, but the kernel killed the relay for memory at 572 gadgets (221 MB) |

The memory came from asyncio's 256 KiB TLS read buffer, which became resident on Linux: about 220 KB per gadget. On the same host, 300 idle loopback TLS pairs took 580 KB per pair with that buffer and 133 KB with 32 KiB. Gateway [#235](https://github.com/adidshaft/grok-gadgets-gateway/pull/235) sets 32 KiB; the final code above includes it.

Two run faults were found and fixed before the final runs: an aborted run left fleet workers alive, which replaced the next run's sessions (gateway #232); and a lost MCP endpoint ended a run without a summary (gateway #234). Those runs are not counted.

### What this means

- One small relay host of this size carried 200 gadgets polling every 100 ms (the ESP32 firmware before long-poll) at about 60 % CPU.
- With long-poll (gateway 0.1.0a18 and SDKs that opt in), it carried 1,000 gadgets at about 67 % CPU and 137 MB.
- These are measurements of one host, one network path and simulated gadgets, not guarantees. Real gadgets also send events, and Grok Bot calls arrive in bursts.

## Sign-in (tier: software)

- Gateway [#227](https://github.com/adidshaft/grok-gadgets-gateway/pull/227): the SDK's own OAuth client with `client_metadata_url` signed in by document, listed devices and refreshed its token. Registration still worked in the same relay. Tests cover the address, response and document rules, and a real local HTTPS server.
- The relay metadata now says `client_id_metadata_document_supported: true`.
- **Grok Bot via a metadata document: Not tested.** Grok Bot registered by dynamic registration on 13 October 2026; no log yet shows it using a document.

## Sign-in page (tier: owner)

- 18 October 2026: the owner reviewed phone-size screenshots of the first design and asked for less text, the website's theme and the text behind a toggle. Gateway [#231](https://github.com/adidshaft/grok-gadgets-gateway/pull/231) made that change.
- Current screenshots at 375 × 812: [code](sign-in-page-2026-10-18-code.jpg), [wrong code](sign-in-page-2026-10-18-wrong.jpg), [operator waiting](sign-in-page-2026-10-18-waiting.jpg).
- The page policy, the redirect back to Grok Bot and the frame, cache and referrer headers are unchanged and tested.
