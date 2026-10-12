# Project status

Updated 12 October 2026. This is the one place that says what works. Other pages link here
instead of repeating caveats.

**The Grok Bot connection is in progress. You can test the gateway and existing SDK examples locally.**

| Part | Works today (software, checked in CI every night) | Not verified yet |
| --- | --- | --- |
| Gateway and simulated light | Six MCP tools for Grok Bot over stdio or authenticated HTTP on `127.0.0.1`; `rehearse` first success; simulator kit; opt-in TLS listener for Wi-Fi devices on one private address | Native Grok Bot tool calls (approved `rehearse` commands work); Windows and Intel Mac installs |
| Linux SDK | `grok-linux-agent dev ./my_gadget.py` with the decorator API, against the gateway's `main` | Real peripherals, systemd, Raspberry Pi hardware |
| ESP32 SDK | Host tests, three firmware examples compile, simulated USB link to the gateway. The ESP32-S3 + OLED kit passed physical tests on the owner's board over USB ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-2026-10-12.md)) and over Wi-Fi from a USB charger ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md)) | Another person's reproduction; other boards and routers; setup without a USB cable ([#72](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/72)) |
| Home Assistant probe | Read-only discovery against fixtures | A real Home Assistant home |
| Browser playground | Local JavaScript model of the light | — (it never calls Grok) |

## What "verified" means here

- **Software:** tests, builds and local MCP calls. A device acknowledgement is the device's
  report, not proof of a physical effect.
- **Grok Bot:** its normal cloud computer cannot reach your private LAN through its internet connection alone. If you enable **Execution on Local Computer** and approve a command, it can run on your Mac. That command can use SSH to a Pi if the Mac can reach the Pi on the home network and SSH is set up. This is a possible manual experiment, not verified product support or packaged MCP. USB alone does not create the route. See the [three connection paths](../getting-started/hosting.md).
- **Remote MCP:** local `serve` is implemented at `127.0.0.1:8766/mcp` with bearer-token authentication. An authenticated remote MCP endpoint with TLS and approved Grok Bot invocation remain incomplete (`HARD-GROK-REMOTE-001`). A tunnel does not add authentication. Button events do not wake the Bot.
- **Hardware:** needs a person to observe the board. On 12 October 2026 the owner flashed the ESP32-S3 + OLED kit. They observed text, clear, the RGB light, the BOOT button, replug and gateway restart ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-2026-10-12.md)).
  The same day the kit ran over Wi-Fi from a USB charger. The owner observed boot, text, clear, BOOT, Wi-Fi loss and recovery, gateway restart, revocation, wrong-CA rejection and power cycle ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md)).

**M5 — Actual Grok: partly done.** Grok Bot runs `rehearse` on the owner's Mac through local execution. It showed text on the real OLED, over USB and over Wi-Fi. Native Grok Bot tool calls need the remote route ([#4](https://github.com/adidshaft/grok-gadgets/issues/4)).

**M8 — Physical and independent verification: partly done.** The owner's ESP32-S3 + OLED kit passed. An independent reproduction and a real Raspberry Pi setup are still needed.

Tested component versions are in the [compatibility manifest](../../compatibility/tested-components.json).
How the parts connect and who runs what: [hosting FAQ](../getting-started/hosting.md).
Dated evidence for maintainers starts at the [verification record](local-status.md).
