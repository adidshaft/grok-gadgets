# Local software and service status

Grok Gadgets is an alpha for the existing Grok Bot. The source repositories and static website are public. Package releases and a hosted gadget service have separate gates. Recorded local software checks and agent source review passed. A dedicated Grok Bot computer has a tested simulator kit and browser-exported configuration installed. Direct terminal observation confirms the configuration checksum and installed package version. This does not prove native Grok tool invocation. Inspectable native invocation evidence and physical verification remain pending.

| Component | Local evidence | Still pending |
| --- | --- | --- |
| Gateway and simulator | Official MCP client, authenticated loopback and simulation tests | Native invocation receipts and scoped connector reload |
| Linux SDK | Installed-wheel acceptance on macOS and an isolated Linux container | Physical peripherals and systemd lifecycle |
| ESP32 SDK / AtomS3 Lite C124 | Host consumer tests and ESP32-S3 compilation | Physical USB, LED/button and flashing |
| Home Assistant | Fixtures and local MCP transport checks | Actual home installation and Grok |
| Website and community | Public static site, fixtures and offline recognition | Release uploads, a hosted gateway and automatic recognition |

## Run locally

Choose a workspace containing the five sibling repositories. From the hub, create the pinned website environment before building:

```sh
uv venv .venv --python 3.13
uv pip install --python .venv/bin/python -r website/requirements.txt
.venv/bin/python website/build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory website/dist
```

Run the gateway's assertion-backed simulator demo:

```sh
cd ../grok-gadgets-gateway
uv sync --locked
uv run python -m grok_gadgets_gateway.demo
```

These operations prove software behavior. They do not prove physical effects or that Grok has called the tools.

## Remaining gates

The Grok Bot needs a supported authenticated route to the gateway for local gadgets. The current loopback device listener and stdio process are not a hosted HTTPS/OAuth MCP service. That remote service is unimplemented. A tunnel cannot supply the missing MCP transport or authorization. A cloud command cannot execute a private path on a user's computer. See the [hosting FAQ](../getting-started/hosting.md) for operator responsibilities and future hosting choices.

Local software acceptance, native Grok invocation, remote security and physical verification are separate checks. Mobile clients, actual Home Assistant devices and independent human reproduction need their own evidence.

The public website does not run the gateway or a tunnel. Future service deployment, release uploads and live recognition require their own approval. Firmware binary redistribution needs dependency/license review. These local instructions do not activate an account or device.
