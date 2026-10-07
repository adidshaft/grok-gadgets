# Grok Gadgets

![Grok Gadgets — Open source. Real world.](docs/visuals/project-banner.png)

[![Experimental alpha](docs/visuals/badge-stage.svg)](docs/public/support-matrix.md) [![Apache-2.0 license](docs/visuals/badge-license.svg)](LICENSE) [![View CI checks](docs/visuals/badge-checks.svg)](https://github.com/adidshaft/grok-gadgets/actions) [![Contributions welcome](docs/visuals/badge-contribute.svg)](CONTRIBUTING.md)

**[Website](https://grok-gadgets.pages.dev/)** · [Documentation](https://grok-gadgets.pages.dev/docs.html) · [Roadmap](ROADMAP.md) · [Issues](https://github.com/adidshaft/grok-gadgets/issues) · **[Join r/GrokGadgets](https://www.reddit.com/r/GrokGadgets/)**

**Let your Grok Bot control lights, buttons and sensors you build. Open source.**

Status: Grok Bot connection in progress · test it locally today
([project status](docs/public/support-matrix.md)).
Independent project, not affiliated with SpaceXAI or xAI.

Pick a path:

- **No hardware:** run the gateway's simulated light and rehearse the Grok Bot calls in
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
| Play with a virtual light in your browser | [Browser playground](https://grok-gadgets.pages.dev/#playground), then the [simulator kit](docs/getting-started/simulator-kit.md) |
| Build a Raspberry Pi or Linux gadget | [Linux SDK](https://github.com/adidshaft/grok-gadgets-linux-sdk) |
| Build an ESP32 gadget | [ESP32 SDK](https://github.com/adidshaft/grok-gadgets-esp32-sdk) |
| Run the local MCP gateway | [Gateway](https://github.com/adidshaft/grok-gadgets-gateway) |
| Check what Home Assistant offers (read-only) | [Home Assistant probe](https://github.com/adidshaft/grok-gadgets-home-assistant) |
| Compare cloud, Mac-to-Pi and remote MCP paths | [Hosting FAQ](docs/getting-started/hosting.md) |

## How the parts connect

![Browser simulation exports settings for the local MCP simulator. SDK and native Grok paths have separate verification requirements.](docs/visuals/project-overview.svg)

Grok Bot normally runs on its cloud computer. This does not expose your home network.
With local execution enabled and a command approved, it can run a Mac command. If the Mac
can reach a Pi and SSH is configured, that command can reach the Pi. This is a possible
manual experiment, not verified Grok Gadgets support. USB alone does not create the route.

The gateway's local `serve` is implemented on loopback. Packaged remote MCP and a verified
Grok Bot invocation are incomplete. A tunnel adds reachability, not authentication.
See the [three-path hosting FAQ](docs/getting-started/hosting.md) before planning a connection.

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
