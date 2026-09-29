# HUB-ESP-001 — Reusable C124 USB firmware and compilation

Owner: grok-gadgets

Stage: done · M4

Labels: feature, esp32, P1

Intended behaviour: Reusable C124 USB firmware and compilation

Acceptance:

- Documented commands reproduce observed behaviour
- Evidence identifies actual verification level

Dependencies: HUB-GW-001

Commits: 585adda, 74085a9

Evidence:

- 3 CTest and canonical frame tests
- Firmware compiled RAM54628 flash276113; binary276480 bytes
- Actual consumer PTY overflow/restart/revocation tests; independent review regression rerun passed

Blocker: None
