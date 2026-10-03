# HARD-SIM-EXPORT-001 — Browser export overwrites the hash-protected simulator default

Owner: grok-gadgets

Stage: in progress · MH

Labels: bug, website, gateway, P1

Intended behaviour: Export my-light.json and use it as a separate custom config without weakening bundled integrity

Acceptance:

- Reproduce old simulator-config.json hash collision
- Align download, copy, fallback and setup with distinct my-light.json
- Regression exports browser contract into extracted kit and verifies immutable defaults
- Actual browser file installs and exercises local MCP discovery, commands, state, offline rejection and reconnect
- Affected and cross-repository acceptance passes; current kit/site/release provenance verified
- Bounded independent review resolved and stages/journal/evidence updated

Dependencies: HUB-DEMO-001, HUB-KIT-001

Commits: Pending

Evidence:

- docs/verification/simulator-export-onboarding.md

Blocker: None
