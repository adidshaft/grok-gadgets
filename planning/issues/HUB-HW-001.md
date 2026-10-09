# HUB-HW-001 — First ESP32-S3/OLED physical experiment

Owner: grok-gadgets

Stage: blocked · M8

Labels: feature, esp32, P1, needs hardware

Intended behaviour: Use the ordered AYWHP ESP32-S3 DevKitC-style ESP32-S3-WROOM-1-N16R8 USB-C board, ApTechDeals 840-point breadboard/jumpers and Robocraze 0.96-inch 128×64 four-pin OLED advertised as SPI/I²C.

Acceptance:

- Follow [kit, setup and acceptance](../../docs/getting-started/experiment-kit.md).
- Keep simulator-first checks separate from physical evidence; the separate OLED Python rehearsal does not implement a display driver or gateway integration.
- Inspect controller, interface, pin order, voltage and board configuration after delivery.
- Observe displayed text/clear, USB disconnect/reconnect and restart recovery.
- Use optional external LED/button and resistor only if onboard parts are unsuitable; these are not confirmed purchases.
- Record existing Grok Bot invocation and physical observations as separate checks.

Dependencies: HUB-ESP-001

Commits: Pending

Evidence: Hardware order confirmed 9 October 2026; no physical verification.

Blocker: Kit delivery, inspection, reviewed wiring and OLED implementation.
