# HUB-GROK-001 — Actual existing Grok Bot tool execution

Owner: grok-gadgets

Stage: blocked · M5

Labels: feature, gateway, P1

Intended behaviour: Actual existing Grok Bot tool execution

Acceptance:

- Existing signed-in Grok Bot invokes gateway MCP simulator tools
- Discovery, green/off state, invalid commands, button events and offline/reconnect acceptance
- Evidence is operator-owned server logs plus transcript observation, correlated by command ID. Native stdio tool-I/O export is Enterprise-only and excludes stdio servers; do not wait on it.
- No physical verification claim

Dependencies: HUB-GW-001

Commits: 1ac4496

Evidence:

- docs/verification/real-grok-experiment.md
- docs/verification/grok-launch-evidence.md

Blocker: No Grok Bot session has used local `serve`. Native tool-I/O export cannot close this gate on a personal plan. Operator HTTP logs plus transcript observation are the evidence trail once an experiment is approved.
