# Grok Gadgets

![Grok Gadgets — Open source. Real world.](docs/visuals/project-banner.png)

[![Experimental alpha](docs/visuals/badge-stage.svg)](docs/public/support-matrix.md) [![Apache-2.0 license](docs/visuals/badge-license.svg)](LICENSE) [![View CI checks](docs/visuals/badge-checks.svg)](https://github.com/adidshaft/grok-gadgets/actions) [![Contributions welcome](docs/visuals/badge-contribute.svg)](CONTRIBUTING.md)

**[Website](https://grokgadgets.org/)** · [Documentation](https://grokgadgets.org/docs.html) · [Roadmap](ROADMAP.md) · [Issues](https://github.com/adidshaft/grok-gadgets/issues) · **[Join r/GrokGadgets](https://www.reddit.com/r/GrokGadgets/)**

**Let your Grok Bot control lights, buttons and sensors you build. Open source.**

Status: works with local MCP clients today · Grok Bot connection in progress
([project status](docs/public/support-matrix.md)).
Independent project, not affiliated with SpaceXAI or xAI.

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
| See it work in five minutes, no hardware | [Gateway first success](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/first-success.md) |
| Play with a virtual light in your browser | [Browser playground](https://grokgadgets.org/#playground), then the [simulator kit](docs/getting-started/simulator-kit.md) |
| Build a Raspberry Pi or Linux gadget | [Linux SDK](https://github.com/adidshaft/grok-gadgets-linux-sdk) |
| Build an ESP32 gadget | [ESP32 SDK](https://github.com/adidshaft/grok-gadgets-esp32-sdk) |
| Run the local MCP gateway | [Gateway](https://github.com/adidshaft/grok-gadgets-gateway) |
| Check what Home Assistant offers (read-only) | [Home Assistant probe](https://github.com/adidshaft/grok-gadgets-home-assistant) |
| Understand why a cloud Bot cannot see your desk yet | [Hosting FAQ](docs/getting-started/hosting.md) |

## How the parts connect

![Browser simulation exports settings for the local MCP simulator. SDK and native Grok paths have separate verification requirements.](docs/visuals/project-overview.svg)

Grok Bot runs in the cloud. The gateway and your gadgets run on a computer you operate. Each
repository installs on its own; the SDKs talk to the gateway, and the gateway never depends
on an SDK. A tunnel only moves packets; it does not log anyone in. Never expose the device port.

## Community

Join [r/GrokGadgets](https://www.reddit.com/r/GrokGadgets/) to show what you built, ask
questions and share ideas. Follow the [community guidelines](community/guidelines.md) and the
[Code of Conduct](CODE_OF_CONDUCT.md); keep tokens and household details out of posts.
Bugs and proposals go to [GitHub Issues](https://github.com/adidshaft/grok-gadgets/issues).

## Contribute

![Choose an issue, make a focused branch, run checks, then open a pull request for review.](docs/visuals/contribution.svg)

Every repository has its own starter issues: see [ready issues](docs/contributing/ready-issues.md).
Branch from `dev` and open your PR into `dev`; `main` only holds tagged stable releases ([branches and releases](CONTRIBUTING.md#branches-and-releases)).
Then read the [contribution guide](CONTRIBUTING.md). Help: [support](SUPPORT.md). Security:
[security policy](SECURITY.md).

To build this website locally (Python 3.13, uv, Node.js 22+ and Git):

```sh
python3 scripts/dev.py setup
python3 scripts/dev.py check
python3 scripts/dev.py site
```

Open `http://127.0.0.1:4173/index.html`. With the four other repositories beside this one,
`scripts/check-all.py` runs the cross-repository integration.

## License and affiliation

Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). Grok Gadgets is an independent
open-source project. It is **not affiliated with, endorsed by or sponsored by SpaceXAI or
xAI**, which make Grok and Grok Bot, nor with M5Stack or Home Assistant. Grok and SpaceXAI
marks shown on the website follow their [brand guidelines](https://x.ai/legal/brand-guidelines)
and are not covered by this project's license. Public history used reconstructed commit
dates; see [publication sanitization](docs/verification/publication-sanitization.md).
