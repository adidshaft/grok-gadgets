# Ordered kit update — 9 October 2026

This record starts with the 9 October order. The delivered parts and USB
inspection are documented in the 12 October section below.

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

## Physical inspection 12 October 2026

This record covers visual identification and read-only USB enumeration. It does
not claim firmware execution, display operation or Grok Bot control. The owner
provided photographs of the delivered board and one display; the photos are not
published in this repository.

| Check | Observation | Result |
| --- | --- | --- |
| Board identity | PCB marked `YD-ESP32-23`, `2022-V1.3`; module can marked `ESP32-S3-N16R8`. Two USB-C ports are labelled `COM` and `USB`. Pads labelled `3V3`, `GND`, `8`, `9` are visible. | Pass: visual markings |
| Display identity | Electrifier 1.3-inch 128×64 display PCB marked `RG1.30 IIC V2.2`; four pads labelled `VCC`, `GND`, `SCK`, `SDA`. | Pass: visual markings; controller and address unknown |
| Connectors | Neither board has fitted pin headers. The owner has loose headers but no soldering tool. Breadboard and jumper wiring were not connected. | Blocked: secure headers needed |
| Mac USB | On macOS 27.0 arm64, `ioreg -p IOUSB -w 0` listed `Espressif Device` after connecting the board's `USB` port. USB VID `0x303A`, PID `0x4001`. `ls /dev/cu.*` included `/dev/cu.usbmodem1234561`. | Pass: USB enumeration only |
| Firmware/display | No serial commands, flashing, I²C scan, OLED text/clear or recovery checks were run. | Not tested |
| Grok Bot | No supported invocation receipt or independently retrieved execution result. | Not tested |

An earlier board in the same task did not appear in Mac USB listings. Its cause
was not diagnosed; that observation does not show the earlier board is defective.
The new board's USB observation does not establish its flash/PSRAM configuration,
firmware behavior or display wiring. No firmware or source checksum exists for a
board-specific kit build yet.

The [planned connection table and diagram](../getting-started/experiment-kit.md#stage-2-prepare-and-connect-the-inspected-kit)
use the printed labels: display `VCC` to board `3V3`, `GND` to `GND`, `SCK` to
GPIO9 and `SDA` to GPIO8. This is a plan, not a tested circuit. Ordinary loose
header pins resting in the holes or breadboard are not a reliable connection.
Disconnect USB before fitting headers or changing wires. The display controller,
I²C address, driver, board build profile and physical acceptance remain open.

Evidence is tracked in [ESP32 issue #4](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/4#issuecomment-6119182081)
and [hub issue #15](https://github.com/adidshaft/grok-gadgets/issues/15#issuecomment-6119183970).
