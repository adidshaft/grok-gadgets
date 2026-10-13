# Documentation

Choose the task you want to complete. Current setup needs an operator, a Mac gateway and a configured gadget.
Phone-only setup is planned, not available today.

## Use a configured gadget

1. Ask the operator to confirm the gadget and gateway are ready.
2. [Connect your Grok Bot](getting-started/connect-grok-bot.md) and complete OAuth sign-in.
3. Ask Grok Bot to list gadgets, show text or read the button events.
4. If a step fails, use the [troubleshooting lookup](getting-started/troubleshooting.md).

The owner verified Mac and iPhone calls. See [current support](public/support-matrix.md) before you choose another platform.

## Build a gadget

| Starting point | Guide |
| --- | --- |
| No hardware | [First success with the simulator](getting-started/first-success.md) |
| The tested ESP32-S3 and OLED | [Parts and wiring](getting-started/experiment-kit.md), then [repeat the setup](getting-started/repeat-the-kit.md) |
| A Linux application | [Linux SDK](https://github.com/adidshaft/grok-gadgets-linux-sdk#quickstart) |

Use the [ESP32 SDK](https://github.com/adidshaft/grok-gadgets-esp32-sdk) for board examples and reusable firmware code.
Use the [gateway](https://github.com/adidshaft/grok-gadgets-gateway) for device routing and Grok Bot tools.
Home Assistant operators can use the [read-only probe](https://github.com/adidshaft/grok-gadgets-home-assistant).

## Reference

- [Glossary](reference/glossary.md): shared terms.
- [Repository and device map](architecture/overview.md): component responsibilities.
- [Hosting](getting-started/hosting.md): the current connection and its limits.
- [Gateway protocol](https://github.com/adidshaft/grok-gadgets-gateway/tree/main/docs): tool and transport references.

## Status and roadmap

[Project status](public/support-matrix.md) lists releases and support.
The [roadmap](../ROADMAP.md) separates completed work, planned phases and owner decisions.

## Verification and contribution

[How we verify](public/how-we-verify.md) explains the evidence levels.
The [daily record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md) contains the latest owner observations and logs.
Report a repeat test in [#185](https://github.com/adidshaft/grok-gadgets/issues/185).
For code or documentation work, read [Contributing](../CONTRIBUTING.md).
