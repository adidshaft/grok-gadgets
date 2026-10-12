# Ordered kit update — 9 October 2026

The owner ordered the first [ESP32-S3 and OLED kit](../getting-started/experiment-kit.md).
The order replaces the AtomS3 Lite first-experiment plan. Earlier build evidence still
applies only to its recorded examples.

## Changes

- Retargeted plans, roadmap, parts, setup, physical acceptance, and public documentation.
- Added the ESP32 SDK's controller-independent OLED Python rehearsal.
- Kept the released gateway/browser RGB simulation unchanged and described its limits.
- Updated website kit diagrams, navigation, and conceptual OLED message/clear workbench.
- Updated hub issues #15 and #30, gateway #4 and #13, and ESP32 #4, #6 and #13.
- Kept physical issues open. Community issue #15 still accepts other supported hardware reports.

## Verification

- Gateway: 148 tests and Ruff passed. This task changed documentation and acceptance records only.
- ESP32: four CTest suites, four OLED model tests, formatting/lint, and 259 protocol transcript frames passed.
- Hub: all checks passed in a clean tracked-source copy, without a sibling gateway checkout or unrelated drafts.
- Browser: inspected the local workbench at desktop and 390-pixel width. Checked the message and clear controls.
- Existing ignore rules cover the OLED test's Python cache. No credentials or physical logs were added.

The shared workspace's full hub runner has two independent blockers. Its gateway
`dev` includes newer request-log work than the published simulator ZIP. Its unrelated,
untracked video drafts fail lint. This task does not rebuild the published ZIP or
change those drafts. The clean-source check validates the retained download against
its recorded integrity, not against the newer gateway `dev`.

## Remaining gates

Delivery and inspection must establish the exact board revision, memory settings,
USB route, OLED controller/interface, power requirements, address, and pin mapping.
Confirm breadboard fit, headers, cable data support, and optional LED/button parts.
Then implement the matching display driver and kit firmware, compile it, and observe
physical display, input/output, and recovery results. The Python model does not
implement a gateway OLED capability or prove a display driver works.

Actual Grok Bot invocation and independent reproduction remain separate gates.
No hardware was connected or flashed. No code was pushed or website deployed by this update.
