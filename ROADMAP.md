# Roadmap

Grok Gadgets is an experimental alpha for Grok Bot. Builders use its SDKs to make gadgets.
The goal is simple setup for the people who use those gadgets.

## Today, next, later

- **Today:** a person joins a factory-provisioned gadget to home Wi-Fi from a phone, with no cable and no app. They claim it with the code on its screen; their Grok Bot then sees only their gadgets, by the names they give them. Share, remove and hand-over are explicit. The builder's relay sends signed firmware updates with no cable, and a bad image reverts by itself. Builders get a "Before you distribute" note and a licence checklist. A builder sets up a relay with one command, prepares gadgets in batches and checks them in one report ([Ship a gadget](docs/getting-started/ship-a-gadget.md)). One small relay host carried 1,000 simulated gadgets with long-poll, and phones on iPhone and Android sign in with the code on the gadget's screen.
- **Next:** a tester repeats the kit ([#185](https://github.com/adidshaft/grok-gadgets/issues/185)) and a builder outside the project follows the guide ([#269](https://github.com/adidshaft/grok-gadgets/issues/269)). Both calls were posted on 24 October. The climate sensor, switch and servo examples run on hardware.
- **Credits:** a relay can meter credits per account: commands and online gadget-days use them, and the operator grants them. Signed receipts and a report check the use. Two live runs measured 1 credit per gadget-day; neither had a command. There are no payments ([Credits on your relay](docs/getting-started/credits-on-your-relay.md)).
- **Later:** builders run their own relays. A listing of independent operator relays waits for two outside operators ([ADR 015](docs/decisions/015-shared-relay.md)). A button press does not wake Grok Bot.
- **Paying for a relay:** [ADR 016](docs/decisions/016-pay-for-a-relay.md) is only a proposal. Nothing is sold, and there are no payments. Selling waits for an outside builder and for legal review.

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
| 13: ready for others | Complete on the owner's setup | [Ready-for-others record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ready-for-others-2026-10-18.md): a 512 MB relay carried 1,000 simulated gadgets with long-poll; sign-in by client metadata document (scripted client); the new sign-in page; Android claim and text; 39 hours of sign-in with no fresh sign-in; the kit on a released image by signed update. Tester and builder calls are drafted |
| 14: shared relay decision | Decided; Stage 0 complete on the owner's setup | [ADR 015](docs/decisions/015-shared-relay.md): builder-only relays now, an operator network later, no project-run relay now ([#270](https://github.com/adidshaft/grok-gadgets/issues/270)). [Credits record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/credits-2026-10-20.md): per-account credits, the out-of-credits message in Grok Bot, signed receipts and a reconciled report; one kit, one relay, no payments |
| 15: Stage 1 preparation | Complete on the owner's setup; ADR 016 stays proposed | [ADR 016](docs/decisions/016-pay-for-a-relay.md) proposed: customers would pay a builder by card, never with a wallet; the gateway stays payment-free. [First credits run](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/credits-pricing-2026-10-23.md): 1.0 credit per gadget-day over four metered UTC days, no commands; the owner ended it on 23 October. A [second run](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/credits-pricing-2026-10-24.md) (23 to 24 October) again had no commands, and the owner ended it ([#402](https://github.com/adidshaft/grok-gadgets/issues/402)). No payments |
| 16: hygiene and reach | Complete on the owner's setup | [Relay backup record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/relay-backup-2026-10-24.md): nightly backups on the owner's relay and a restore that matched; an encrypted offline copy of the signing keys; the relay host updated and rebooted; the tester and builder calls posted ([milestone](https://github.com/adidshaft/grok-gadgets/milestone/25)). No payments |

[ADR 009](docs/decisions/009-relay-route.md) plans Phases 9–13. Stage 1 (Phase 9) is accepted and released. [ADR 010](docs/decisions/010-phone-setup.md) (Phase 10, phone setup) and [ADR 011](docs/decisions/011-accounts-and-claim-codes.md) (Phase 11, accounts and claim codes) are accepted.
[ADR 012](docs/decisions/012-signed-updates.md) (Phase 12b, signed updates) and [ADR 013](docs/decisions/013-builder-kit.md) (Phase 12a, builder kit) are accepted.
[ADR 014](docs/decisions/014-ready-for-others.md) (Phase 13, ready for others) is accepted. [ADR 015](docs/decisions/015-shared-relay.md) (Phase 14, shared relay) is accepted. [ADR 016](docs/decisions/016-pay-for-a-relay.md) (Phase 15, paying for a relay) is proposed. ADR numbers differ from phase numbers: Phase 13 was renumbered on 18 October 2026, and the shared-relay decision moved to Phase 14.

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
