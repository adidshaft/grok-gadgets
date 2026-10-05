# Grok Gadgets

![Grok Gadgets — Open source. Real world.](docs/visuals/project-banner.png)

[![Experimental alpha](docs/visuals/badge-stage.svg)](docs/public/support-matrix.md) [![Apache-2.0 license](docs/visuals/badge-license.svg)](LICENSE) [![View CI checks](docs/visuals/badge-checks.svg)](https://github.com/adidshaft/grok-gadgets/actions) [![Contributions welcome](docs/visuals/badge-contribute.svg)](CONTRIBUTING.md)

**[Try the simulator](https://grok-gadgets.pages.dev/#playground)** · [Documentation](https://grok-gadgets.pages.dev/docs.html) · [Roadmap](ROADMAP.md) · [Issues](https://github.com/adidshaft/grok-gadgets/issues) · [Community](https://www.reddit.com/r/GrokGadgets/)

Open-source tools so you can connect gadgets to [Grok Bot](https://docs.x.ai/grok-bot). Start with a virtual light in the browser. Then build on Linux or ESP32, or explore Home Assistant.

## What works with Grok Bot today

| You can do this now | You cannot do this yet |
| --- | --- |
| Try the [browser light](https://grok-gadgets.pages.dev/#playground). It does not call Grok. | Ask Grok Bot to control a board on your Mac, a Pi, or your home network. |
| Run the [local simulator kit](docs/getting-started/simulator-kit.md) on your computer. | Use a cloud Bot against a file that only exists on your Mac. Command MCP runs on Grok's cloud computer. |
| Build the Linux agent or compile C124 firmware. | Treat compile success as a flashed, working board. |
| Read the [hosting FAQ](docs/getting-started/hosting.md). | Point Grok Bot at `127.0.0.1`. Remote HTTPS MCP is not verified with Grok Bot. |

**Experimental alpha.** Software tests pass. `grok_verified` and `hardware_verified` stay false until native Grok receipts and physical observation exist.

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
python3 scripts/dev.py site
```

Or the long form: `uv venv .venv --python 3.13`, install `website/requirements.txt`, `website/build.py`, then `python3 -m http.server 4173 --bind 127.0.0.1 --directory website/dist`. Open `http://127.0.0.1:4173/index.html#playground`.

Hub checks: `python3 scripts/dev.py check` (same as CI). With pinned sibling clones, `scripts/check-all.py` runs the fourteen integration groups.

## Contribute

![Choose an issue, make a focused branch, run checks, then open a pull request for review.](docs/visuals/contribution.svg)

[Ready issues](docs/contributing/ready-issues.md) · [contribution guide](CONTRIBUTING.md) · [support](SUPPORT.md) · [security](SECURITY.md) · [community](community/README.md)

Apache-2.0. Independent project, not affiliated with xAI, M5Stack or Home Assistant.

Public history used reconstructed commit dates; see [publication sanitization](docs/verification/publication-sanitization.md).
