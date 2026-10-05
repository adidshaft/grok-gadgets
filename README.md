# Grok Gadgets

![Grok Gadgets — Open source. Real world.](docs/visuals/project-banner.png)

[![Experimental alpha](docs/visuals/badge-stage.svg)](docs/public/support-matrix.md) [![Apache-2.0 license](docs/visuals/badge-license.svg)](LICENSE) [![View CI checks](docs/visuals/badge-checks.svg)](https://github.com/adidshaft/grok-gadgets/actions) [![Contributions welcome](docs/visuals/badge-contribute.svg)](CONTRIBUTING.md)

**[Try the simulator](https://grok-gadgets.pages.dev/#playground)** · [Documentation](https://grok-gadgets.pages.dev/docs.html) · [Roadmap](ROADMAP.md) · [Issues](https://github.com/adidshaft/grok-gadgets/issues) · [Community](https://www.reddit.com/r/GrokGadgets/)

Connect gadgets to Grok with open-source tools and separate software development kits (SDKs). Start with a virtual light. Then build with Linux or ESP32, or explore Home Assistant.

Documentation follows our [ASD-STE100-inspired writing guide](docs/contributing/writing-guide.md). Formal compliance is not claimed.

**Experimental alpha.** Browser simulation and the local Model Context Protocol (MCP) connection pass software tests. C124 firmware compiles. Actual Grok execution, mobile use and physical operation still need verification.

## Choose your starting point

| Your next step | Start here |
| --- | --- |
| Try without hardware | [Browser and simulator kit](docs/getting-started/simulator-kit.md) |
| Develop a connection | [Gateway](https://github.com/adidshaft/grok-gadgets-gateway) |
| Build a Linux application | [Linux SDK](https://github.com/adidshaft/grok-gadgets-linux-sdk) |
| Build an ESP32 gadget | [ESP32 SDK](https://github.com/adidshaft/grok-gadgets-esp32-sdk) |
| Explore an existing home | [Home Assistant diagnostics](https://github.com/adidshaft/grok-gadgets-home-assistant) |
| Help improve the alpha | [Ready issues](docs/contributing/ready-issues.md) and [contribution guide](CONTRIBUTING.md) |

The [public website](https://grok-gadgets.pages.dev/) is live. Its source lives here. Package releases and firmware downloads have separate release gates.

The ESP32 library is reusable; C124 is the first board example. Other boards need their own hardware handlers, build configuration and verification. See the [repository and device map](docs/architecture/overview.md).

## How the parts connect

![Browser simulation exports settings for the local MCP simulator. SDK and native Grok paths have separate verification requirements.](docs/visuals/project-overview.svg)

## Try the website locally

Install Python 3.13, uv, Node.js 22+ and Git. Run these commands from the hub directory:

```sh
uv venv .venv --python 3.13
uv pip install --python .venv/bin/python -r website/requirements.txt
.venv/bin/python website/build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory website/dist
```

Open `http://127.0.0.1:4173/index.html#playground`. Change the virtual light. Export your settings as `my-light.json`. The browser does not call Grok or control hardware.

To run the local MCP demonstration, follow the [simulator kit guide](docs/getting-started/simulator-kit.md). That guide also explains download verification and rebuild checks.

Browser and local simulation need no hardware or Grok account. Kit installation needs Python 3.11+ and downloads dependencies with hash checks.

An actual Grok experiment needs a supported MCP connection in the Bot's environment. A cloud Bot cannot run a file that exists only on your Mac. Remote HTTPS/OAuth access to local gadgets is not implemented.

## What is verified

| Evidence | What it establishes |
| --- | --- |
| Gateway and configurable kit | Source and extracted-package MCP software acceptance |
| Linux SDK | Software tests on macOS and Linux container; peripherals/systemd unverified |
| ESP32 SDK | Host logic, simulated USB/PTY and C124 compilation; no flashing or physical observation |
| Home Assistant | Fixture diagnostics and read-only client; no real home or Grok acceptance |
| Website | Static build/link tests, browser interaction and responsive checks |

## Contribute

![Choose an issue, make a focused branch, run checks, then open a pull request for review.](docs/visuals/contribution.svg)

| Get involved | Link |
| --- | --- |
| Find a small task | [Ready issues](docs/contributing/ready-issues.md) |
| Propose a change | [Contribution guide](CONTRIBUTING.md) |
| Review activity | [Pull requests](https://github.com/adidshaft/grok-gadgets/pulls) · [Contributors](https://github.com/adidshaft/grok-gadgets/graphs/contributors) |
| Report a private concern | [Security](SECURITY.md) · [Code of conduct](CODE_OF_CONDUCT.md) |

Run standalone hub checks with `python3 scripts/check.py`, `node --test website/test_simulator.cjs`, and `.venv/bin/python -m unittest discover -s website`. With all four pinned siblings installed, `.venv/bin/python scripts/check-all.py` runs the fourteen integration groups. See [verification matrix](docs/public/support-matrix.md), [architecture](docs/architecture/overview.md), [roadmap](ROADMAP.md), [support](SUPPORT.md), [security](SECURITY.md), [governance](GOVERNANCE.md) and [community](community/README.md).

Original code and vectors: [Apache-2.0](LICENSE), with [NOTICE](NOTICE) and [third-party notices](THIRD_PARTY_NOTICES.md). Independent community project, unaffiliated with xAI, M5Stack or Home Assistant. The owner has retained the current project and repository names.

## History note

Pre-publication commit dates were reconstructed across 29 September–5 October 2026 at the owner’s request. Verification records retain their actual execution dates. See the [history and privacy record](docs/verification/publication-sanitization.md).
