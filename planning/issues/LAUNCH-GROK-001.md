# LAUNCH-GROK-001 — Obtain actual Grok simulator invocation evidence

Owner: grok-gadgets

Stage: blocked · ML

Labels: research, gateway, P1, blocked, simulator

Intended behaviour: Meet exact launch-plan stage acceptance; public activation remains separately gated

Acceptance:

- Operator-owned `serve` HTTP logs plus transcript observation, correlated by command ID, for the exact kit and website-exported configuration
- Discovery, color/off/state, invalid/unsupported input, retry, ordered simulated events, disconnect/recovery through that route
- Return to normal six tools; preserve unrelated connectors and real devices
- Do not wait on native stdio tool-I/O export (Enterprise-only; excludes stdio servers)

Dependencies: LAUNCH-001

Commits: 0dad909, 9e45d93

Evidence:

- docs/verification/grok-launch-evidence.md
- docs/verification/mcp-trace.md

Blocker: No Grok Bot session has used local `serve`. Native stdio tool-I/O export cannot close this gate on a personal plan.
