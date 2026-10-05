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

Blocker: Local `serve` (loopback Streamable HTTP + bearer) is implemented on the gateway `simplify-and-fix` branch (`a9be0db`). A public tunnel, hosted service, or Grok Bot experiment still needs owner approval. Native stdio tool-I/O export cannot close this gate.
