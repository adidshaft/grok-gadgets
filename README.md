# Grok Gadgets

![Grok Gadgets — Open source. Real world.](docs/visuals/project-banner.png)

[![Experimental alpha](docs/visuals/badge-stage.svg)](docs/public/support-matrix.md) [![Apache-2.0 license](docs/visuals/badge-license.svg)](LICENSE) [![View CI checks](docs/visuals/badge-checks.svg)](https://github.com/adidshaft/grok-gadgets/actions) [![Contributions welcome](docs/visuals/badge-contribute.svg)](CONTRIBUTING.md)

**[Try the simulator](https://grok-gadgets.pages.dev/#playground)** · [Documentation](https://grok-gadgets.pages.dev/docs.html) · [Roadmap](ROADMAP.md) · [Issues](https://github.com/adidshaft/grok-gadgets/issues) · [Community](https://www.reddit.com/r/GrokGadgets/)

**Let your Grok Bot control lights, buttons and sensors you build. Open source.**

Status: works with local MCP clients today · Grok Bot connection in progress
([project status](docs/public/support-matrix.md)).

Pick a path:

- **No hardware:** run the gateway's simulated light and call it from MCP Inspector in
  [five minutes](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/first-success.md).
- **Raspberry Pi / Linux:** one install, ten lines of Python, one command with the
  [Linux SDK](https://github.com/adidshaft/grok-gadgets-linux-sdk#quickstart).
- **ESP32:** an Arduino sketch with the [ESP32 SDK](https://github.com/adidshaft/grok-gadgets-esp32-sdk#quickstart).

Already use Home Assistant? Check what it offers with the
[read-only probe](https://github.com/adidshaft/grok-gadgets-home-assistant).

## Start here

| If you want to… | Open |
| --- | --- |
| Try it without hardware | [Browser playground](https://grok-gadgets.pages.dev/#playground) then the [simulator kit](docs/getting-started/simulator-kit.md) |
| Understand why the cloud Bot cannot see your desk | [Hosting FAQ](docs/getting-started/hosting.md) |
| Run the local gateway | [Gateway](https://github.com/adidshaft/grok-gadgets-gateway) |
| Write a Linux gadget | [Linux SDK](https://github.com/adidshaft/grok-gadgets-linux-sdk) |
| Flash an ESP32 (C124 is the first example) | [ESP32 SDK](https://github.com/adidshaft/grok-gadgets-esp32-sdk) |
| Probe Home Assistant (read-only) | [Home Assistant](https://github.com/adidshaft/grok-gadgets-home-assistant) |
| Fix something small | [Ready issues](docs/contributing/ready-issues.md) |

The [website](https://grok-gadgets.pages.dev/) is live. Package and firmware downloads are a separate release step.

## How the parts connect

![Browser simulation exports settings for the local MCP simulator. SDK and native Grok paths have separate verification requirements.](docs/visuals/project-overview.svg)

Grok Bot runs in the cloud. The gateway and gadgets run on a computer you operate. A tunnel only moves packets; it does not log anyone in. Do not expose the local device port.

## Build the website locally

Python 3.13, uv, Node.js 22+ and Git:

```sh
python3 scripts/dev.py setup
python3 scripts/dev.py check
python3 scripts/dev.py site
```

Open `http://127.0.0.1:4173/index.html#playground`. Sibling integration is `scripts/check-all.py` when the four other repos sit next to this one.

## Contribute

![Choose an issue, make a focused branch, run checks, then open a pull request for review.](docs/visuals/contribution.svg)

[Ready issues](docs/contributing/ready-issues.md) · [contribution guide](CONTRIBUTING.md) · [support](SUPPORT.md) · [security](SECURITY.md) · [community](community/README.md)

Apache-2.0. Independent project, not affiliated with xAI, M5Stack or Home Assistant.

Public history used reconstructed commit dates; see [publication sanitization](docs/verification/publication-sanitization.md).
