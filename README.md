# Grok Gadgets

![Grok Gadgets — Open source. Real world.](docs/visuals/project-banner.png)

[![Experimental alpha](docs/visuals/badge-stage.svg)](docs/public/support-matrix.md) [![Apache-2.0 license](docs/visuals/badge-license.svg)](LICENSE) [![View CI checks](docs/visuals/badge-checks.svg)](https://github.com/adidshaft/grok-gadgets/actions) [![Contributions welcome](docs/visuals/badge-contribute.svg)](CONTRIBUTING.md)

![Grok Gadgets shown on a small OLED display mounted on a breadboard.](docs/visuals/esp32-s3-oled-display.jpg)

<p align="center"><sub>Display lettering enhanced for readability.</sub></p>

**[Website](https://grokgadgets.org/)** · [Documentation](https://grokgadgets.org/docs.html) · [Roadmap](ROADMAP.md) · [Issues](https://github.com/adidshaft/grok-gadgets/issues) · **[Join r/GrokGadgets](https://www.reddit.com/r/GrokGadgets/)**

**Give your Grok Bot hands in the physical world. Build a gadget, set it up from a phone, then just ask. Open source.**

Alpha · one owner-tested kit · phone setup with no cable · Grok Bot calls through a gateway on an always-on server.
See [project status](docs/public/support-matrix.md). Independent project, not affiliated with SpaceXSI.

## Choose a start

| Your task | Start here |
| --- | --- |
| Set up a gadget you received | [Phone setup](docs/getting-started/phone-setup.md) |
| Claim a prepared gadget | [Claim your gadget in Grok Bot](docs/getting-started/claim-your-gadget.md), after phone setup. |
| Run a relay and prepare gadgets for others | [Ship a gadget](docs/getting-started/ship-a-gadget.md). Start with your own relay and a tested application. |
| Build a gadget | [Factory provisioning](docs/getting-started/factory-provision.md), [tested OLED kit](docs/getting-started/repeat-the-kit.md), [ESP32 SDK](https://github.com/adidshaft/grok-gadgets-esp32-sdk) or [Linux SDK](https://github.com/adidshaft/grok-gadgets-linux-sdk) |
| Try without hardware | [Five-minute simulator guide](docs/getting-started/first-success.md) or [browser playground](https://grokgadgets.org/playground) |

Received gadgets need a printed label and the builder’s running relay. The project hosts no relay.

[All documentation](docs/index.md) separates guides, reference, project status and test records.
Home Assistant users can start with the [read-only probe](https://github.com/adidshaft/grok-gadgets-home-assistant).

## How the parts connect

New here? Read [How it works](docs/getting-started/how-it-works.md): one page for builders, end users and the curious.

```mermaid
flowchart LR
    B["Grok Bot"] -->|"HTTPS and OAuth"| T["Owner-run tunnel"]
    T --> G["Gateway on an always-on server"]
    D["Wi-Fi gadget"] -->|"Outbound TLS"| G
```

See the [relay setup guide](docs/getting-started/mac-free-route.md) and the [phone setup guide](docs/getting-started/phone-setup.md).
The gateway can also run on a Mac that stays awake, using the [local kit route](docs/getting-started/repeat-the-kit.md).

The owner's relay and phone setup checks passed; see [project status](docs/public/support-matrix.md) for evidence and limits.
Report an independent kit test in [#185](https://github.com/adidshaft/grok-gadgets/issues/185).
Outside builders can follow [Ship a gadget](docs/getting-started/ship-a-gadget.md) and report in [#269](https://github.com/adidshaft/grok-gadgets/issues/269).

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

## Support the project

Grok Gadgets is open source. If you’d like to support its development, you can send a
voluntary contribution to one of these addresses:

- **Ethereum (ETH):** `0xD571210016e5AB4206D27f24bE128916E1C91047`
- **Solana (SOL):** `D2jV1NkjuHHmvkuZ48Woc29v5NDeKLmHeLkUcN4fDg68`
- **Bitcoin (BTC):** `bc1qal92xr892akwxgqrnkjhld7ar04hlld06uqyq5`
- **ZEC (Shielded):** `u10hkzg65lgz6eq3arsylenag78jracfpguc3m4p6ptz8fkjlgxy6668yrjdgj2p704wp2f2wykrqv88tg9zu7fjuc9tk5s6vazvzmw5cvt5qkyzr32wqymesmcymja9zxpcwc6vcswa88yae023yj7jhypvn6n592t6z7nxqu4s59sdf9`

## License and affiliation

Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). Grok Gadgets is an independent
open-source project. It is **not affiliated with, endorsed by or sponsored by SpaceXSI**, nor
with M5Stack or Home Assistant. The Grok mark shown on the website is not
covered by this project's license. Public history used reconstructed commit dates; see
[publication sanitization](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/publication-sanitization.md).
