# Project status

Updated 7 October 2026. This is the one place that says what works. Other pages link here
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
- **Grok Bot:** its normal cloud computer cannot reach your private LAN through its internet connection alone. If you enable **Execution on Local Computer** and approve a command, it can run on your Mac. That command can use SSH to a Pi if the Mac can reach the Pi on the home network and SSH is set up. This is a possible manual experiment, not verified product support or packaged MCP. USB alone does not create the route. See the [three connection paths](../getting-started/hosting.md).
- **Remote MCP:** local `serve` is implemented at `127.0.0.1:8766/mcp` with bearer-token authentication. An authenticated remote MCP endpoint with TLS and approved Grok Bot invocation remain incomplete (`HARD-GROK-REMOTE-001`). A tunnel does not add authentication. Button events do not wake the Bot.
- **Hardware:** needs a person to observe the board. No board was flashed for this project.

**M5 — Actual Grok: blocked.** Supported exact-kit invocation/reload evidence and the remote route are still needed.

**M8 — Physical and independent verification: blocked.** A real Pi/device setup, peripheral observation and independent reproduction are still needed.

Tested component versions are in the [compatibility manifest](../../compatibility/tested-components.json).
How the parts connect and who runs what: [hosting FAQ](../getting-started/hosting.md).
Dated evidence for maintainers starts at the [verification record](local-status.md).
