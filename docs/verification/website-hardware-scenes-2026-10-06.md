# Practical hardware scenes — 6 October 2026

HUB-WEB-008 / #108 responds to the owner's rejection of the abstract Signal orbit and generic peripheral labels.

## Changes

Connections centers the supplied Grok Bot mark among C124/ESP32, Raspberry Pi/Linux and Home Assistant illustrations. SDK routes identify the gateway; Home Assistant identifies its own MCP server. Selection reveals a short capability description, proposed connection path and documentation link. All Bot routes remain conceptual and pending verification.

Workbench adds an exploded C124 concept with a gateway, USB bridge and retracting USB plug. LED controls animate a command and device report. Button events travel to the gateway and stop there; they do not wake Grok Bot. Unplugging clears travelling packets, retains events already received by the gateway, and makes fresh commands unavailable. An interrupted dispatched LED command remains unconfirmed. Reconnecting waits for a fresh action.

Three max-effort agent subagents handled the two modules and independent architecture/link review. Review corrections preserved retained events and interrupted-command uncertainty. The parent integrated and visually checked the result.

## Browser evidence

In-app Chromium checks covered 1440×900, 1280×600, 667×375 and 320×568. The inspected pages matched viewport dimensions. Both new scenes were inspected on the smallest phone and landscape size. The four-scene selector fits the phone width; its numeric prefixes are hidden there. The Bot mark preserves its aspect ratio.

- Selecting Home Assistant changed the readout to its own MCP route and guide.
- Paused Workbench button interaction reported “Button → gateway · no Bot wake.”
- After unplugging, a fresh LED action reported “USB offline · commands unavailable.” Phase stayed at 0.247 while paused; packets stayed at zero.
- Reconnect reported “USB restored · send a new command.” After resuming animation, phase advanced to 10.875 while packet count stayed at zero and transmitting stayed false: no replay.
- LED animation completed with “Execution reported · physical check pending.”
- No browser JavaScript errors were reported.

Interrupted-command timing and retained-event persistence were independently reviewed in source. They were not established by physical hardware testing. Reduced-motion and lifecycle gates were preserved; no operating-system preference changes were performed.

Screenshots and source-review receipts are local ignored artifacts. These diagrams make no network or hardware calls and are not evidence of native Grok Bot operation or a tested physical board.

## Checks

`python3 scripts/check.py` passed: simulator, script, community and website tests; generated website and ZIP build; public URL prefix; lint and formatting. Module syntax checks passed. The link review covered 66 pages, 4,049 local references, 332 fragment links and 18 JavaScript destinations with no missing targets or duplicate IDs.
