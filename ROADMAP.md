# Roadmap

Grok Gadgets is an experimental alpha for Grok Bot. Builders use its SDKs to make gadgets.
The goal is simple setup for the people who use those gadgets.

## Today, next, later

- **Today:** a person joins a factory-provisioned gadget to home Wi-Fi from a phone, with no cable and no app. They claim it with the code on its screen; their Grok Bot then sees only their gadgets, by the names they give them. Share, remove and hand-over are explicit. The builder's relay sends signed firmware updates with no cable, and a bad image reverts by itself. Builders get a "Before you distribute" note and a licence checklist. A builder sets up a relay with one command, prepares gadgets in batches and checks them in one report ([Ship a gadget](docs/getting-started/ship-a-gadget.md)).
- **Next:** a builder outside the project follows that guide ([#269](https://github.com/adidshaft/grok-gadgets/issues/269)). The climate sensor, switch and servo examples run on hardware.
- **Phase 13, Ready for others (in progress):** one small relay is measured: 1,000 simulated gadgets with long-poll. Sign-in accepts client metadata documents, and the sign-in page is shorter. Still open: an Android check, three days of sign-in, and calls for testers and builders ([#363](https://github.com/adidshaft/grok-gadgets/issues/363)).
- **Later:** Phase 14, only a decision on a shared relay. A button press does not wake Grok Bot.

The project runs no relay service. There are no promised dates.

## Phase plan

| Phase | State | Evidence or remaining gate |
| --- | --- | --- |
| 1–6: local tools, kit and service | Owner-tested work complete | [Independent kit report](https://github.com/adidshaft/grok-gadgets/issues/185) remains open |
| 7: native Grok Bot connection | Complete on the owner's setup | [Mac and iPhone calls](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/grok-remote-https-2026-10-13.md) |
| 8: daily route checks | Complete on one setup for one day | [Recorded checks](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md); another day and a calibrated usage rate remain |
| 9: Mac-free route | Complete on the owner's setup | [Relay record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/mac-free-route-2026-10-13.md): iPhone on cellular controlled the kit while the Mac slept; one kit, one server |
| 10: setup without a cable | Complete on the owner's setup | [Phone setup record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/phone-setup-2026-10-14.md): iPhone and Android joined the factory-provisioned kit to Wi-Fi with the computer closed; wrong code, wrong password, window expiry and reset checks; one kit |
| 11: claim your gadget | Complete on the owner's setup | [Claim record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/claim-2026-10-17.md): two people with their own Grok Bot proved claim by code, isolation of list, state, commands and events, share and revoke, wrong and expired codes, a flood, and a transfer after a reset; one kit, one relay |
| 12b: update and ship safely | Complete on the owner's setup | [Update record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ota-2026-10-17.md): signed updates over the relay with no cable, wrong key and changed byte refused, automatic revert, power cut recovered; one kit, one relay. [Before you distribute](docs/getting-started/before-you-distribute.md) and the [licence checklist](docs/getting-started/firmware-licences.md) |
| 12a: builder kit | Complete on the owner's setup | [Builder kit record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/builder-kit-2026-10-17.md): a clean-room run, and the owner's dry run on a fresh host with a batch of three, phone setup, claim, Grok Bot text and a signed update. A second builder ([#269](https://github.com/adidshaft/grok-gadgets/issues/269)) and the new examples on hardware remain |
| 13: ready for others | In progress | Measured relay capacity, sign-in by client metadata document, a new sign-in page, Android, tester and builder calls ([#363](https://github.com/adidshaft/grok-gadgets/issues/363)) |
| 14: shared relay | Owner decision only | Cost, operations, abuse controls, privacy and terms; no service promised ([#270](https://github.com/adidshaft/grok-gadgets/issues/270)) |

[ADR 009](docs/decisions/009-relay-route.md) plans Phases 9–13. Stage 1 (Phase 9) is accepted and released. [ADR 010](docs/decisions/010-phone-setup.md) (Phase 10, phone setup), [ADR 011](docs/decisions/011-accounts-and-claim-codes.md) (Phase 11, accounts and claim codes) [ADR 012](docs/decisions/012-signed-updates.md) (Phase 12b, signed updates) and [ADR 013](docs/decisions/013-builder-kit.md) (Phase 12a, builder kit) are accepted; the later stages are design only. ADR numbers differ from phase numbers: Phase 13 was renumbered on 18 October 2026, and the shared-relay decision moved to Phase 14.

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
