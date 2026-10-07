# Local software and service status

Grok Gadgets is an alpha for your existing Grok Bot. The public site provides docs and a browser simulator. The local gateway provides stdio MCP and authenticated HTTP MCP through `serve`. No Grok Bot connection or physical hardware operation is verified. See the [tested component versions](../../compatibility/tested-components.json) for the current local software evidence.

| Component | Local evidence | Still pending |
| --- | --- | --- |
| Gateway and simulator | Local rehearsal command, authenticated loopback and simulation tests | Supported remote route and actual Grok Bot execution evidence |
| Linux SDK | Installed-wheel acceptance on macOS and an isolated Linux container | Physical peripherals and systemd lifecycle |
| ESP32 SDK / AtomS3 Lite C124 | Host consumer tests and ESP32-S3 compilation | Physical USB, LED/button and flashing |
| Home Assistant | Fixtures and local MCP transport checks | Actual home installation and Grok Bot |
| Website and community | Public static site, fixtures and offline recognition | Release uploads, a hosted gateway and automatic recognition |

## Run locally

From the hub, run:

```sh
python3 scripts/dev.py setup
python3 scripts/dev.py site
```

Open `http://127.0.0.1:4173`. You do not need the sibling repositories to build the website.

Run the gateway's assertion-backed simulator demo:

```sh
cd ../grok-gadgets-gateway
uv sync --locked
uv run python -m grok_gadgets_gateway.demo
```

These operations prove software behavior. They do not prove physical effects or that Grok Bot has called the tools.

## Remaining gates

The [hosting FAQ](../getting-started/hosting.md) describes three separate paths:

- **Cloud computer:** Grok Bot normally runs commands on its cloud computer. Its internet connection does not give it access to your private home network.
- **Manual Mac → SSH → Pi experiment:** With **Execution on Local Computer** enabled and your approval for a command, Grok Bot can run that command on your Mac. The command can reach a Pi if the Mac can reach the Pi on the home network and SSH is set up. USB alone does not create this route. This possible experiment is not verified Grok Gadgets support or a packaged MCP integration.
- **Packaged remote MCP:** The local `serve` command is implemented at `127.0.0.1:8766/mcp` with bearer-token authentication. The authenticated remote MCP endpoint with TLS and an approved, verified Grok Bot invocation are not complete. A tunnel adds reachability, not authentication. Do not connect Grok Bot to the alpha as a ready-to-use remote service.

**M5 — Actual Grok is blocked.** It needs supported invocation and reload evidence for the exact kit, plus a supported remote route. **M8 — Physical and independent verification is blocked.** It needs a real Pi/device setup, observed peripheral behavior and independent reproduction. Mobile clients and actual Home Assistant devices need separate evidence.

The public website does not run the gateway or a tunnel. Future service deployment, release uploads and live recognition require their own approval. Firmware binary redistribution needs dependency/license review. These local instructions do not activate an account or device.
