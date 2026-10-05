# Local software and service status

Grok Gadgets is an alpha for your existing Grok Bot. The public site provides docs and a browser simulator. The local gateway provides stdio MCP and authenticated HTTP MCP through `serve`. No Grok Bot connection or physical hardware operation is verified. See the [tested component versions](../../compatibility/tested-components.json) for the current local software evidence.

| Component | Local evidence | Still pending |
| --- | --- | --- |
| Gateway and simulator | Official MCP client, authenticated loopback and simulation tests | Supported remote route and actual Grok Bot execution evidence |
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

These operations prove software behavior. They do not prove physical effects or that Grok has called the tools.

## Remaining gates

The Grok Bot needs a supported authenticated route to the gateway for local gadgets. Local HTTP MCP is implemented with a bearer token. Public TLS, OAuth and a hosted service are not supplied. An operator route to Grok Bot remains unverified. A tunnel supplies reachability, not authorization. A cloud command cannot execute a private path on a user's computer. See the [hosting FAQ](../getting-started/hosting.md) for operator responsibilities and future hosting choices.

Local software acceptance, native Grok invocation, remote security and physical verification are separate checks. Mobile clients, actual Home Assistant devices and independent human reproduction need their own evidence.

The public website does not run the gateway or a tunnel. Future service deployment, release uploads and live recognition require their own approval. Firmware binary redistribution needs dependency/license review. These local instructions do not activate an account or device.
