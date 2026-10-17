# Documentation

Choose what you want to do. A prepared gadget needs a label and an operator’s relay.
The project hosts no relay.

## Use a gadget

| Your task | Start here |
| --- | --- |
| Join your home Wi-Fi | [Set up your gadget with your phone](getting-started/phone-setup.md) |
| Connect Grok Bot and claim ownership | [Claim your gadget](getting-started/claim-your-gadget.md) |
| Give someone access | [Share a gadget](getting-started/claim-your-gadget.md#share-a-gadget) |
| Change the owner | [Hand a gadget to someone](getting-started/hand-a-gadget-to-someone.md) |
| Receive firmware updates | [Keep your gadget up to date](getting-started/keep-up-to-date.md) |
| Fix a problem | [Troubleshooting](getting-started/troubleshooting.md) |

Your relay account owns the gadget. You can give another account use or view access and revoke it later.
A reset keeps ownership. A pending transfer needs the owner’s removal or a 7-day wait without refusal.

Two people tested claims, sharing and hand-over with their own iPhones, one relay and one OLED kit.
Android Grok Bot remains untested. The 7-day timer has software tests only.
See [current support](public/support-matrix.md) for releases and limits.

## Build a gadget

| Starting point | Guide |
| --- | --- |
| No hardware | [First success with the simulator](getting-started/first-success.md) |
| The tested ESP32-S3 and OLED | [Build and repeat the kit](getting-started/repeat-the-kit.md) |
| A Linux application | [Linux SDK](https://github.com/adidshaft/grok-gadgets-linux-sdk#quickstart) |
| A gadget ready for someone else | [Factory-provision and label it](getting-started/factory-provision.md) |
| New firmware for your gadgets | [Sign and ship an update](getting-started/sign-and-ship-an-update.md) |
| A gadget to distribute | [Distribution responsibilities](getting-started/before-you-distribute.md) and [firmware licences](getting-started/firmware-licences.md) |

Use the [ESP32 SDK](https://github.com/adidshaft/grok-gadgets-esp32-sdk) for board examples and reusable firmware code.
Home Assistant operators can use the [read-only probe](https://github.com/adidshaft/grok-gadgets-home-assistant).

## Run a relay

[Hosting](getting-started/hosting.md) explains who runs the gateway and how gadgets reach it.
Follow [Run the gateway away from your Mac](getting-started/mac-free-route.md) for the relay route.
Only relay operators send firmware updates, with the CLI. Grok Bot has no update tool.

The [connection guide](getting-started/connect-grok-bot.md) covers the earlier Mac gateway route.

## Explore or contribute

- [Project status](public/support-matrix.md): releases, evidence and open gates.
- [Roadmap](../ROADMAP.md): completed work and planned phases.
- [Glossary](reference/glossary.md): shared terms.
- [Architecture](architecture/overview.md): component responsibilities.
- [How we verify](public/how-we-verify.md): evidence levels.
- [Contributing](../CONTRIBUTING.md): find an issue and prepare a change.

Report a repeat test in [#185](https://github.com/adidshaft/grok-gadgets/issues/185).
