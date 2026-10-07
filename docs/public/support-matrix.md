# Project status

Updated 6 October 2026. This is the one place that says what works. Other pages link here
instead of repeating caveats.

**The Grok Bot connection is in progress. You can test every part locally today.**

| Part | Works today (software, checked in CI every night) | Not verified yet |
| --- | --- | --- |
| Gateway and simulated light | Six MCP tools for Grok Bot over stdio or authenticated HTTP on `127.0.0.1`; `rehearse` first success; simulator kit | Grok Bot use; Windows and Intel Mac installs |
| Linux SDK | `grok-linux-agent dev ./my_gadget.py` with the decorator API, against the gateway's `main` | Real peripherals, systemd, Raspberry Pi hardware |
| ESP32 SDK | Host tests, both firmware examples compile, simulated USB link to the gateway | Flashing, a physical C124 board, its LED and button |
| Home Assistant probe | Read-only discovery against fixtures | A real Home Assistant home |
| Browser playground | Local JavaScript model of the light | — (it never calls Grok) |

## What "verified" means here

- **Software:** tests, builds and local MCP calls. A device acknowledgement is the device's
  report, not proof of a physical effect.
- **Grok Bot:** a cloud Bot cannot open `127.0.0.1` on your computer. A supported remote route
  is later work (tracked as `HARD-GROK-REMOTE-001`). Button events do not wake the Bot.
- **Hardware:** needs a person to observe the board. Nobody has flashed a board for this project yet.

Tested component versions are in the [compatibility manifest](../../compatibility/tested-components.json).
How the parts connect and who runs what: [hosting FAQ](../getting-started/hosting.md).
Dated evidence for maintainers starts at the [verification record](local-status.md).
