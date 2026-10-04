# HUB-KIT-001 — Provide an inspectable configurable Grok simulator kit

Owner: grok-gadgets

Stage: done · M9

Labels: feature, gateway, P1

Intended behaviour: Provide an inspectable configurable Grok simulator kit

Acceptance:

- Download kit contains exact source, wheel, locked hashed dependencies, license and provenance
- Extracted kit installs and configured MCP runs without hardware
- Website export loads in gateway; cloud setup instructions distinguish Bot-reported route and native receipt gate
- Build automatically refreshes changed committed gateway or kit inputs, runs acceptance before publishing, and fails on stale/corrupt/uncommitted source

Dependencies: HUB-GW-001

Commits: d2bda94, fa062a1, 7ac61fd, f4ad5f9

Evidence:

- docs/verification/simulator-playground.md
- docs/verification/download-build-policy.md

Blocker: None
