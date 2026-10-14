# Roadmap

Grok Gadgets is an experimental alpha for Grok Bot. Builders use its SDKs to make gadgets.
The goal is simple setup for the people who use those gadgets.

## Today, next, later

- **Today:** Grok Bot on Mac and iPhone controls the owner's Wi-Fi kit through a gateway on an always-on Linux server. The Mac can sleep.
- **Next:** Phase 10, joining a gadget to Wi-Fi from a phone with no cable.
- **Later:** claim codes and tools for builders who ship gadgets.

The project runs no relay service. There are no promised dates.

## Phase plan

| Phase | State | Evidence or remaining gate |
| --- | --- | --- |
| 1–6: local tools, kit and service | Owner-tested work complete | [Independent kit report](https://github.com/adidshaft/grok-gadgets/issues/185) remains open |
| 7: native Grok Bot connection | Complete on the owner's setup | [Mac and iPhone calls](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/grok-remote-https-2026-10-13.md) |
| 8: daily route checks | Complete on one setup for one day | [Recorded checks](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md); another day and a calibrated usage rate remain |
| 9: Mac-free route | Complete on the owner's setup | [Relay record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/mac-free-route-2026-10-13.md): iPhone on cellular controlled the kit while the Mac slept; one kit, one server |
| 10: setup without a cable | Next | iPhone joins a factory-provisioned kit to Wi-Fi; wrong password and reset checks |
| 11: claim your gadget | Planned | Two accounts prove device isolation, sharing, removal and transfer |
| 12: builder kit | Planned | A second builder follows the deployment and shipping guides |
| 13: shared relay | Owner decision only | Cost, operations, abuse controls, privacy and terms; no service promised |

[ADR 009](docs/decisions/009-relay-route.md) plans Phases 9–13. Stage 1 (Phase 9) is accepted and released; the later stages are design only.

## What the current result means

Native calls use Remote HTTPS and OAuth sign-in through an owner-run tunnel.
The owner approves sign-in on the gateway's host. The gateway and tunnel must remain available.
With the gateway on the Mac, the route failed while the Mac slept and queued nothing.
With the gateway on an always-on server, the route worked while the Mac slept.
After a server reboot, the kit was back Online in 24 seconds.
After a restart, the gateway listened at 66 seconds and the board returned Online at 72 seconds.
These times describe one run, not a recovery guarantee.

The remaining checks include another day, measured usage and another person's setup.
Real Linux services, peripherals and Home Assistant homes need separate evidence.
A device button does not wake Grok Bot.

## Help test or build

- Use the [documentation index](docs/index.md) to choose a guide.
- Repeat the [tested kit](docs/getting-started/repeat-the-kit.md) and report results in [#185](https://github.com/adidshaft/grok-gadgets/issues/185).
- Pick a [ready issue](docs/contributing/ready-issues.md) and follow the [contribution guide](CONTRIBUTING.md).
- Check [current releases and support](docs/public/support-matrix.md) before you install.
