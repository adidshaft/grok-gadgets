# ADR 007 — Grok Bot calls the gadgets through Remote HTTPS with owner-approved sign-in

**Date:** 13 October 2026  
**Status:** Accepted on 13 October 2026 with outcome **(a)**. Evidence: [Remote HTTPS record](../verification/grok-remote-https-2026-10-13.md), run 4.  
**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)  
**Issues:** [#154](https://github.com/adidshaft/grok-gadgets/issues/154), [#4](https://github.com/adidshaft/grok-gadgets/issues/4), gateway [#71](https://github.com/adidshaft/grok-gadgets-gateway/issues/71), [#130](https://github.com/adidshaft/grok-gadgets-gateway/issues/130), [#132](https://github.com/adidshaft/grok-gadgets-gateway/issues/132)

## Context

[ADR 004](004-grok-bot-route.md) gave outcome (b): Grok Bot reached the gateway only through approved local `rehearse` commands, so native tool calls needed a remote route. The [research note](../research/grok-remote-https-2026-10.md) found two documented credentials for a Remote HTTPS server: "the Bot's own credential, or each person's sign-in if the server uses OAuth".

Runs 1 to 3 on 13 October tried the Bot credential, a fixed bearer token in a header. The gateway checks passed each time, but no server could be added: the personal Grok Bot app (desktop 0.70.2) has no form for a custom server, and Grok Bot will not put a fixed token into its setup step. Asked in chat, Grok Bot said it could add an OAuth server with only the URL.

## Decision

1. Grok Bot connects to the gateway as a **Remote HTTPS** MCP server with **OAuth sign-in**. `serve --oauth` makes the gateway its own sign-in server. The owner approves each sign-in with a code on the Mac (`grok-gadgets-gateway oauth approve CODE --name grok-bot`). No password or token is typed into a web page or a chat.
2. The owner runs the HTTPS tunnel. It forwards only `127.0.0.1:8766`. The project runs no URL, relay or account.
3. The tunnel route is optional. Approved local `rehearse` commands (ADR 004) remain the no-tunnel path.
4. The gateway's own log is the evidence and the usage record: `--allowed-host` requires `--request-log`, and `grok-gadgets-gateway usage` summarizes it. Grok Bot's plan usage is read by the owner, never scraped.
5. Fixed named tokens stay for clients that can send a header. Remote requests never accept the local `default` token, and `remote off` stops all remote access at once.
6. No hosted relay. The blocker was the credential, not reachability, and a relay would be a project-run service.

## Outcome — 13 October 2026

Run 4, gateway `0.1.0a11` from `dev`, the owner's OLED kit on Wi-Fi:

- Grok Bot registered with the gateway, the owner approved one sign-in, and Grok Bot listed "grok-gadgets, 6 tools".
- From the **desktop app**, six prompts gave six tool calls, one of each tool. From the **iPhone app**, three prompts gave list, command and state calls. All nine log lines carry `"token":"grok-bot"`, `"remote":true` and the connector backend's client name, not `grok-gadgets-rehearse`. Both `display.text` commands were `executed`.
- The owner saw "Hello from Grok Bot" on the OLED.
- The server added on the desktop worked from the phone with no setup there. The phone's plugin list did not show it.
- Turn-off: `remote off`, sign-in revoked, tunnel stopped, server uninstalled, service back on `main`.

Result: **(a)**. Native Grok Bot tool calls work through this route.

## Usage per prompt and per tool call (estimate)

Measured: Grok Bot's **Weekly usage** read "1%" before, between and after, on the desktop and the phone. In that window Grok Bot received 11 messages (2 setup, 9 gadget prompts) and made 9 tool calls, plus the sign-in. The gateway's own figures: 9 calls, 278 ms in the gateway, 10,477 bytes of tool arguments and results.

**Estimate, not a reading:** the session used less than 1 percentage point of the weekly allowance. That is less than about 0.09 points per message and less than about 0.11 points per tool call, as an upper bound. The page shows whole percent only. The figure covers all of Grok Bot's work in the window, not only the tool calls. A longer session is needed for a calibrated rate (`usage --calibrate`).

## Consequences

- Hub: "Connect your Grok Bot" (Mac and phone) and "Track usage" guides; the website shows the native route as working, tunnel optional.
- Gateway `0.1.0-alpha.11` carries the hardening, usage tracking and OAuth sign-in. Its release waits for the owner.
- An account-free quick tunnel gets a new hostname on every start, so the server must be added again. A tunnel account with a fixed hostname suits daily use.
- A sign-in lasts until its refresh token expires (30 days) or `oauth revoke`. Anyone who can approve on the Mac controls access.
- Not yet tested: button events through this route, reconnect after a gateway restart with a live sign-in, Team Bots and Linux hosts.
