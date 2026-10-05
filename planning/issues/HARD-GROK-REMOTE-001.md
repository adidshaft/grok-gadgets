# HARD-GROK-REMOTE-001 — Implement authenticated cloud-to-local HTTPS MCP transport

Owner: grok-gadgets

Stage: blocked · M5

Labels: feature, gateway, P1, help wanted

Intended behaviour: Existing Grok Bot reaches explicitly authorized local devices through a reviewed HTTPS MCP service

Acceptance:

- Approved hosting, route and trust design; no raw device protocol exposure
- TLS, supported OAuth or scoped credentials, per-user/per-device authorization and tenant isolation
- User consent, secure secret storage, credential rotation and revocation
- Missing/invalid/expired/revoked credential and cross-user/cross-device access rejection regressions
- Bounded commands/connections/queues/timeouts; redacted diagnostics; shutdown/reconnect tests
- Actual Grok desktop/mobile experiment after separate activation approval

Dependencies: HUB-GROK-001

Commits: Pending

Evidence:

- docs/verification/real-grok-test-plan.md
- docs/getting-started/hosting.md

Blocker: Remote HTTPS MCP/OAuth service is unimplemented. Design, implementation and security tests are required before separately approved service activation. Documentation does not close this gate.
