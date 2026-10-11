# LAUNCH-FIRMWARE-DIST-001 — Prepare the required third-party redistribution material before firmware binary uploads

> Hardware plan update — 9 October 2026: the [ordered ESP32-S3/OLED kit](../../docs/getting-started/experiment-kit.md) replaces C124 as the first physical experiment. C124 build commands and results below describe the retained reference example, not verification of the ordered kit. Controller, interface and pins remain provisional until inspection.

Owner: grok-gadgets

Stage: blocked · PUBLIC-ALPHA

Labels: maintenance, esp32, P1, blocked

Intended behaviour: Keep experimental source/build instructions eligible while BIN/ELF/bootloader/partition release assets remain excluded

Acceptance:

- Inventory exact linked dependency licenses and corresponding sources for the compiled C124 build
- Supply and review required relinking/source/notice material before selecting firmware binary release assets
- Record explicit redistribution disposition and reproduce from reviewed sources

Dependencies: HUB-ESP-001

Commits: Pending

Evidence:

- publication/history-and-assets-review.md

Blocker: Corresponding-source/relinking redistribution package has not been assembled or cleared; source-only publication package excludes binaries.
