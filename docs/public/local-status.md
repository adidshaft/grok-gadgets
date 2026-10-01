# Local release status

Grok Gadgets is an unpublished local alpha exclusively for the existing Grok Bot. The audit correction cycle is in progress; the earlier alpha completion claim is historical.

| Component | Local evidence | Still pending |
| --- | --- | --- |
| Gateway and simulator | Official MCP client, authenticated loopback and simulation tests | Actual Grok Bot connectivity |
| Linux SDK | Installed-wheel software acceptance | Physical peripherals and systemd lifecycle |
| ESP32 SDK / AtomS3 Lite C124 | Host consumer tests and ESP32-S3 compilation | Physical USB, LED/button and flashing |
| Home Assistant | Fixtures and local MCP transport checks | Actual home installation and Grok |
| Website and community | Static site, fixtures and offline recognition | Publication and community activation |

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

The Grok Bot needs a supported authenticated route to the self-hosted gateway. The current loopback-only device listener and local stdio test process are not a hosted HTTPS/OAuth service. A cloud command cannot execute a private path on a user's computer. Real Grok, mobile clients, C124 hardware, actual Home Assistant devices and independent human reproduction remain separate checks.

Public repositories, release uploads, hosted CI, deployment, Reddit changes and live recognition require separate approval. Firmware binary redistribution needs dependency/license review. No account or device action is implied by these local instructions.
