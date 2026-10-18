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
| Stranger-style sign-in on the live relay | Pass | Owner |
| Three days of Grok Bot with no fresh sign-in | Not tested yet | Owner |
| Grok Bot on Android: claim and text on the kit | Pass | Owner |
| Relay on gateway 0.1.0a18 | Pass | Owner |
| Kit on a released image by signed update, with long-poll | Pass | Owner |

## Load test (tier: fresh host, 18 October 2026)

**Host:** DigitalOcean `s-1vcpu-512mb-10gb` in Bangalore (1 vCPU, 458 MB usable), Ubuntu 24.04, Python 3.12.3, OpenSSL 3.0.13. The droplet was created for this test and destroyed after it.

**Relay:** gateway `dev`, `serve --device-listen 0.0.0.0:8444 --max-devices 1000 --commands-per-minute 120` with the example name `devices.example.net`, no tunnel and no OAuth. A fresh relay process for each size.

**Gadgets:** `fleet run` from the owner's Mac over the internet, with a round trip of about 50 ms. All came from one address, so the ramp stayed at 18 new connections a minute. TLS with the relay CA and name, a hello, a poll every 100 ms (or a waiting poll), state every 3 s. One `gadgets_command` a second through MCP over an SSH forward, timed until `executed`. Each size ran 15 minutes after the ramp. CPU and memory are the relay process's, from `fleet sample` every 5 s in that window.

### Final code (gateway `70fbd43`)

| Gadgets | Polls | Online at end | Frames answered a second | Command latency p50 / p95 / p99 | Commands executed | Relay CPU mean / p95 | Relay memory peak |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 100 ms | 50 | 499 | 181 / 274 / 333 ms | 900 of 900 | 20 % / 26 % | 78 MB |
| 200 | 100 ms | 200 | 1,991 | 201 / 304 / 383 ms | 900 of 900 | 61 % / 72 % | 88 MB |
| 1,000 | long-poll 2,500 ms | 1,000 | 713 | 167 / 406 / 1,596 ms | 899 of 900 (1 in flight at the end) | 67 % / 75 % | 137 MB |

No session dropped in any size. The relay logged no error and no `device_flood`.

We discarded a first run of the 50 size on this code. The Mac also ran builds and test suites, and the command driver lost its MCP session after 388 commands. The relay log showed no error. The rerun above ran alone.

### Earlier code and what it found

| Run | Code | Result |
| --- | --- | --- |
| 50, 100 ms | `f55acd8` | All 50 online; 900 of 900 executed; latency p50 202, p95 286, p99 410 ms; CPU mean 18 %, p95 22 %; 77 MB |
| 200, 100 ms | `f55acd8` | All 200 online; 900 of 900 executed; latency p50 217, p95 311, p99 394 ms; CPU mean 62 %, p95 73 %; 131 MB |
| 1,000, 100 ms | `f55acd8` | **Fail.** CPU mean 90 % from about 400 gadgets. At about 660 gadgets the kernel killed the relay for memory (249 MB). 136 sessions dropped before that |
| 1,000, long-poll | `9a9dd76` | **Fail.** CPU stayed low, but the kernel killed the relay for memory at 572 gadgets (221 MB) |

The memory came from asyncio's 256 KiB TLS read buffer, which became resident on Linux: about 220 KB per gadget. On the same host, 300 idle loopback TLS pairs took 580 KB per pair with that buffer and 133 KB with 32 KiB. Gateway [#235](https://github.com/adidshaft/grok-gadgets-gateway/pull/235) sets 32 KiB; the final code above includes it.

We fixed two faults of the tool before the final runs. An aborted run left fleet workers alive, which replaced the next run's sessions (gateway #232). A lost MCP endpoint ended a run without a summary (gateway #234). Those runs are not counted.

### What this means

- One small relay host of this size carried 200 gadgets polling every 100 ms (the ESP32 firmware before long-poll) at about 60 % CPU.
- With long-poll (gateway 0.1.0a18 and SDKs that opt in), it carried 1,000 gadgets at about 67 % CPU and 137 MB.
- These are measurements of one host, one network path and simulated gadgets, not guarantees. Real gadgets also send events, and Grok Bot calls arrive in bursts.

## Sign-in (tier: software)

- Gateway [#227](https://github.com/adidshaft/grok-gadgets-gateway/pull/227): the SDK's own OAuth client with `client_metadata_url` signed in by document, listed devices and refreshed its token. Registration still worked in the same relay. Tests cover the address, response and document rules, and a real local HTTPS server.
- The relay metadata now says `client_id_metadata_document_supported: true`.
- **Grok Bot via a metadata document: Not tested.** Grok Bot registered by dynamic registration on 13 October 2026; no log yet shows it using a document.

## Sign-in page (tier: owner)

- 18 October 2026: the owner reviewed phone-size screenshots of the first design. They asked for less text, the website's theme and the text behind a toggle. Gateway [#231](https://github.com/adidshaft/grok-gadgets-gateway/pull/231) made that change.
- Current screenshots at 375 × 812: [code](sign-in-page-2026-10-18-code.jpg), [wrong code](sign-in-page-2026-10-18-wrong.jpg), [operator waiting](sign-in-page-2026-10-18-waiting.jpg).
- The page policy, the redirect back to Grok Bot and the frame, cache and referrer headers are unchanged and tested.

## Relay and kit (tier: owner, 18 October 2026)

**Releases:** gateway `v0.1.0-alpha.18` (PyPI `0.1.0a18`), ESP32 SDK `v0.2.0-alpha.19` and Linux SDK `v0.1.0-alpha.10`. The owner approved each publication.

**Relay:** the owner's relay went from gateway `0.1.0a17` to `0.1.0a18` from PyPI, after a private backup of its configuration.

| Time | Log line or check |
| --- | --- |
| 13:44:29 | `device_disconnected` for the kit (service restart) |
| 13:44:32 | `serve_started` |
| 13:44:34 | `device_hello` for the kit: back after 5 seconds |
| 13:44 | The relay's metadata says `client_id_metadata_document_supported: true` |

The live Grok Bot sign-ins stayed live through the restart (`service status`).

**Kit:** the kit ran test image `0.2.0-alpha.17.8`. The owner's builder key (`b567ba3923292e09`) signed `0.2.0-alpha.19`, built from the release tag with long-poll on.

| Time | Log line |
| --- | --- |
| 13:45:05 | `update_offered`, `update_started` 0.2.0-alpha.19 |
| 13:45:21–13:45:54 | `update_progress` 25, 50, 75 % |
| 13:46:11 | `update_verified` |
| 13:46:14 | `device_hello`, `update_applied` 0.2.0-alpha.19 |

**Long-poll on hardware:** the relay counted 17 request packets from the kit in 30 seconds after the update. Polling every 100 ms would send about 300. The count is of packets only; no content was read.

## Android and a stranger-style sign-in (tier: owner, 18 October 2026)

The owner used a borrowed Android phone with Grok Bot and the second Grok Bot account from Phase 11. The operator took the kit away from the operator account first, so the kit showed a claim code, as a new owner would see it. Grok Bot on the Android phone added the relay's server and signed in on the new page with that code. The owner then saw `Android ok` on the kit.

| Time | Log line |
| --- | --- |
| 14:47:22 | `device_unclaimed` (operator) |
| 14:51:50 | `http_rejected` 401 `invalid_token` (the first request, before sign-in), `oauth_client_registered` |
| 14:52:03 | `oauth_client_registered` |
| 14:52:04 | `oauth_sign_in_requested` (the new page opens) |
| 14:52:42 | `device_claimed`, `oauth_sign_in_approved` (the code from the kit's screen) |
| 14:52:44 | `oauth_token_issued` (the page handed back to Grok Bot) |
| 14:53:22 | `mcp_tool_call` `gadgets_list_devices` ok, remote |
| 14:53:25 | `mcp_tool_call` `gadgets_name` ok, remote |
| 14:54:00 | `mcp_tool_call` `gadgets_command` ok, `executed`, remote |
| 14:54:54 | `device_claimed` (operator gives the kit back to the operator account) |

- Grok Bot on Android registered by dynamic registration, not by a metadata document.
- After the kit went back, the owner's own Grok Bot got a 401 at 14:56:09, refreshed its sign-in at 14:56:23 and ran `gadgets_command` at 14:56:42 (`executed`). No fresh sign-in was needed.
