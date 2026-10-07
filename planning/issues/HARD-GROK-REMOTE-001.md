# HARD-GROK-REMOTE-001 — Authenticated remote MCP for local gadgets

Owner: grok-gadgets

Stage: in progress · M5

Labels: feature, gateway, P1, help wanted

Intended behaviour: Grok Bot reaches gadgets the operator explicitly authorized, through HTTPS MCP the operator runs.

Acceptance:

- Local `serve` mode: Streamable HTTP MCP on loopback with a rotatable bearer, no raw device protocol exposure
- Tests: missing/wrong token rejected; test controls impossible over HTTP; Host/Origin checks
- Redacted request logs that can stand in for native stdio receipts
- TLS, OAuth or scoped credentials, and a public hostname only after separate activation approval
- Actual Grok desktop/mobile experiment after that approval

Dependencies: none (does not wait on HUB-GROK-001)

Blocker: Local `serve` is implemented with bearer authentication on loopback. Secure remote access is not complete. It needs an approved route, TLS, suitable credentials or OAuth, and independently verified Grok Bot invocation evidence. A tunnel provides reachability, not authentication. Do not point Grok Bot at this alpha yet.

The separate Execution on Local Computer capability can run a Mac command when enabled and approved. If the Mac can reach a Pi over the home network and SSH is configured, that command can reach the Pi. This is a possible manual experiment, not shipped or accepted Grok Gadgets support. USB alone does not create this route.

M5 remains blocked on supported exact-kit invocation/reload evidence and the remote route. M8 remains blocked on a real Pi/device setup, peripheral observation and independent reproduction. See [hosting FAQ](../../docs/getting-started/hosting.md).

Documentation does not activate an account, tunnel or remote service. Those actions need separate approval.
