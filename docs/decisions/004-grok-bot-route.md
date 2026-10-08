# ADR 004 — Phase 2 route from Grok Bot to the gateway

**Date:** 8 October 2026  
**Status:** Proposed. Waiting for the owner's [local-execution test](../grok-local-test.md).  
**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)  
**Issues:** [#31](https://github.com/adidshaft/grok-gadgets/issues/31), [#4](https://github.com/adidshaft/grok-gadgets/issues/4), [#12](https://github.com/adidshaft/grok-gadgets/issues/12), gateway [#65](https://github.com/adidshaft/grok-gadgets-gateway/issues/65)

## Context

The [research note](../research/grok-local-execution-2026-10.md) found that Grok Bot can run approved shell commands on the owner's computer through the desktop app. The official docs do not say that a Grok Bot MCP server can reach a local server. The gateway now writes an opt-in request log, so the owner test produces gateway-side evidence.

## Decision rule

The owner test decides the next step. Record only what the request log shows.

| Test result | Next step |
| --- | --- |
| **(a)** The log shows Bot tool calls from a client other than `grok-gadgets-rehearse` | Local route. Polish the docs and the website "Connect your Grok Bot" path for local use only. No remote service. |
| **(b)** Only approved `rehearse` commands reach the log | Keep (b) as a documented manual experiment. Design the remote route below for native tool calls. |
| Neither | Same as (b). Record the Bot's refusal text as a narrative, not as evidence. |

## If (a) works: local polish

1. Gateway: document the exact Grok Bot MCP server settings that worked.
2. Hub: rewrite [hosting](../getting-started/hosting.md) path 2 and the website "Connect your Grok Bot" path around those settings.
3. Hub: close or narrow [#4](https://github.com/adidshaft/grok-gadgets/issues/4) to "optional remote access", and close [#12](https://github.com/adidshaft/grok-gadgets/issues/12) and [#31](https://github.com/adidshaft/grok-gadgets/issues/31) against the recorded log.

## If (a) does not work: remote route design

The gateway keeps listening on `127.0.0.1`. Nothing below is deployed without a separate owner approval.

### Transport

| Option | How it works | For | Against |
| --- | --- | --- | --- |
| **TLS tunnel** (owner-run) | A tunnel client on the owner's computer gives `127.0.0.1:8766` a public HTTPS name. `serve --allowed-host` already accepts that name. | No project-run service. Smallest code change. | A public URL per owner. The owner needs a tunnel account. The gateway must defend itself on the internet. |
| **Hosted relay** (project-run) | The gateway opens an outbound connection to a relay. Grok Bot calls the relay's HTTPS MCP URL. | No inbound port. Works behind any NAT. | The project runs a service: cost, uptime, data handling and abuse response. Needs an owner decision on spending. |

**Proposal:** start with the owner-run TLS tunnel as a documented reference. Reconsider a hosted relay only after real users ask for it.

### Authentication

- **Bearer token** matches Grok Bot's Remote HTTPS "Bot's own credential" mode. It works with the existing `mcp-token` file and `rotate-mcp-token`. **Proposal:** use it first, with separate named tokens per client.
- **OAuth** gives each person their own sign-in, which Team Bots need. It needs an authorization server and discovery metadata. **Proposal:** a later issue, after the bearer route works.

### Revocation and limits

- Named MCP tokens: `issue`, `list` and `revoke`, effective at once, without a restart. `rotate-mcp-token` stays.
- Rate limits per token, for example 60 tool calls and 10 `gadgets_command` calls a minute. Return a clear `rate_limited` error.
- Caps on concurrent sessions, request body size and request time. Redacted diagnostics only.
- A kill switch: stopping the tunnel or `serve` ends all remote access.

### Proposed issues

These issues are created only if the test result is (b) or neither.

1. **HUB-REMOTE-ADR-001:** accept this design and choose the transport. Owner decision.
2. **GW-TOKENS-001:** named MCP tokens with `issue`, `list` and `revoke`, with regression tests for missing, invalid and revoked tokens.
3. **GW-RATE-001:** per-token rate limits, session caps, body limits and timeouts, with tests.
4. **GW-TUNNEL-DOC-001:** an owner-run TLS tunnel reference guide in front of `127.0.0.1`. No project-owned URL.
5. **HUB-GROK-REMOTE-TEST-001:** an owner test of Grok Bot Remote HTTPS through the tunnel, with the request log. Needs a specific owner yes for the tunnel.
6. **GW-OAUTH-001 (later):** OAuth for Team Bots.

## Consequences

The gateway request log becomes the standard evidence for every Grok Bot test. Docs keep (b) as a manual experiment, not product support, because the Bot runs a fixed command and never calls the tools itself.
