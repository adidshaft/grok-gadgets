# HARD-GROK-REMOTE-001 — Implement authenticated cloud-to-local HTTPS MCP transport

Owner: grok-gadgets

Stage: blocked · M5

Labels: feature, gateway, P1, help wanted

Intended behaviour: Existing Grok Bot reaches explicitly authorized local devices through a reviewed HTTPS MCP service

Acceptance:

- Approved route and access design; no raw device protocol exposure
- TLS, scoped authorization or OAuth, device/tenant isolation and credential revocation
- Missing/invalid/expired/revoked credential and cross-device access rejection regressions
- Bounded commands/connections/timeouts; redacted diagnostics; shutdown/reconnect tests
- Actual Grok desktop/mobile experiment after separate activation approval

Dependencies: HUB-GROK-001

Commits: Pending

Evidence:

- docs/verification/real-grok-test-plan.md

Blocker: Remote HTTPS/OAuth transport is unimplemented; separate design and service activation approval required
