# Project status

Updated 18 October 2026. This is the one place that says what works. Other pages link here
instead of repeating caveats.

**Alpha · one owner-tested kit · phone setup · claim by code · signed updates · Grok Bot through an always-on gateway.**

On 13 October 2026 the owner's Grok Bot called the six tools itself from the Mac and the iPhone. It used an owner-run tunnel with sign-in ([ADR 007](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/007-grok-bot-remote-https.md)). [Connect your Grok Bot](../getting-started/connect-grok-bot.md).

## Current releases

| Component | Release | Package |
| --- | --- | --- |
| Hub | `v0.1.18-alpha.1` | [GitHub release](https://github.com/adidshaft/grok-gadgets/releases/tag/v0.1.18-alpha.1) |
| Gateway | `v0.1.0-alpha.17` | [PyPI `0.1.0a17`](https://pypi.org/project/grok-gadgets-gateway/) |
| ESP32 SDK | `v0.2.0-alpha.18` | [GitHub release](https://github.com/adidshaft/grok-gadgets-esp32-sdk/releases/tag/v0.2.0-alpha.18) |
| Linux SDK | `v0.1.0-alpha.9` | [PyPI `0.1.0a9`](https://pypi.org/project/grok-gadgets-linux-sdk/) |
| Home Assistant | `v0.1.0-alpha.5` | [PyPI `0.1.0a5`](https://pypi.org/project/grok-gadgets-home-assistant/) |

## Today, next, later

**Today:** the kit connects to a gateway on an always-on Linux server.
The earlier Mac-hosted route passed Phase 8 for one day. During Mac sleep, that route failed and queued nothing.
See the [daily record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md).

**Phase 9:** the gateway can run on an always-on Linux server, so the Mac can sleep.
On 13 October 2026 the owner's iPhone, on cellular, showed text on the kit while the Mac slept ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/mac-free-route-2026-10-13.md)).

**Phase 10:** a factory-provisioned gadget joins home Wi-Fi from a phone alone, through its setup hotspot.
On 14 October 2026 the owner joined the kit from an iPhone and an Android phone. The owner kept the Mac closed during iPhone setup. The kit went Online through the relay, and Grok Bot on the iPhone showed text on it ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/phone-setup-2026-10-14.md), [guide](../getting-started/phone-setup.md)).

Android Grok Bot calls remain untested. The owner's relay runs gateway `0.1.0a17` on device port 8443.
New relays use port 8444 by default.

**Phase 11:** each relay account claims gadgets with their screen codes.
Grok Bot sees gadgets the account owns or another account explicitly shares.
On 17 October 2026 two people tested this on the owner's relay and kit, each with Grok Bot on their own iPhone. Claim, isolation, share and revoke, wrong and expired codes, a flood and a hand-over after a reset all passed ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/claim-2026-10-17.md), [guide](../getting-started/claim-your-gadget.md)).

A reset keeps account ownership. A transfer stays pending until the owner removes the gadget or the 7-day period ends without refusal.
The automatic 7-day transfer has software-clock tests only; no physical relay has completed that wait yet.

**Phase 12b:** the relay sends signed firmware updates to a gadget with no cable.
The gadget refuses an image signed with another key or changed on the way. An image that does not come Online within 5 minutes reverts by itself.
On 17 October 2026 the owner's kit passed each of these checks and recovered from a power cut during a download. Grok Bot then showed text on the updated kit ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ota-2026-10-17.md), [guide](../getting-started/sign-and-ship-an-update.md)).
Builders also get [Before you distribute a gadget](../getting-started/before-you-distribute.md) and a [firmware licence checklist](../getting-started/firmware-licences.md). Both are not legal advice.

**Phase 12a:** a builder sets up a relay with one command, prepares gadgets in batches and checks them in one report.
A clean-room run and the owner's dry run on a fresh host followed [Ship a gadget](../getting-started/ship-a-gadget.md) on 17 October 2026 ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/builder-kit-2026-10-17.md)).
The climate sensor, switch and servo examples compile and pass host tests. Nobody has run them with the parts yet.

**Next:** a builder outside the project follows the guide ([#269](https://github.com/adidshaft/grok-gadgets/issues/269)).

**Phase 13 (in progress):** we measure what one small relay carries and add a clearer sign-in page and an Android check ([#363](https://github.com/adidshaft/grok-gadgets/issues/363)). Sign-in also gets ready for the protocol's registration change. We have no measured numbers yet.

**Relay size:** a relay holds 64 gadgets by default. That is a set limit, not a measurement. Gateway `dev` adds `serve --max-devices`; measured sizes come with the Phase 13 load test.

**Platforms:** Grok Bot on Android: Not tested (phone setup from Android passed, a Grok Bot call from Android did not happen yet). Windows: Not tested; run the gateway and a relay on macOS or Linux.

**Later:** Phase 14 is only a decision on a shared relay. The project hosts no service.
See the [roadmap](../../ROADMAP.md) for acceptance gates.

**Help test:** another day, measured usage and [an independent kit report](https://github.com/adidshaft/grok-gadgets/issues/185) remain open.
A button event does not wake Grok Bot.

| Part | What works today | Not verified yet |
| --- | --- | --- |
| Gateway and simulated light | Six MCP tools over stdio or authenticated HTTP on `127.0.0.1`; `rehearse` first success; approved Grok Bot local commands; native Grok Bot calls from Mac and iPhone through an owner-run tunnel with OAuth sign-in, tested for one day behind a fixed hostname (gateway `0.1.0a12`); sign-in flood limits, log rotation and route status; usage summary and hook; simulator kit; private LAN TLS for Wi-Fi devices; optional per-user launchd/systemd service; an always-on Linux relay with iPhone calls while the Mac sleeps; accounts with claim codes, shares, names and hand-over, tested by two people (gateway `0.1.0a15`); signed firmware updates to a gadget, tested on the owner's kit (gateway `0.1.0a16`); `relay init`, batches and `builder report`, tested in a builder's dry run on a fresh host (gateway `0.1.0a17`) | Android Grok Bot calls; a second day and a calibrated usage rate; Team Bots; Windows and Intel Mac installs |
| Linux SDK | PyPI `0.1.0a9`, `grok-linux-agent dev ./my_gadget.py` with the decorator API, and a relay over TLS (`--gateway`, `--ca`, `--device-id`): two simulated batch gadgets were Online on a fresh relay | Real peripherals, systemd on a physical Linux host, Raspberry Pi hardware |
| ESP32 SDK | Host tests, nine firmware builds compile (the climate sensor, switch and servo examples are not tested on hardware), simulated USB link to the gateway. The ESP32-S3 + OLED kit passed physical tests on the owner's board over USB ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-2026-10-12.md)) and over Wi-Fi from a USB charger ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md)); phone setup passed on iPhone and Android ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/phone-setup-2026-10-14.md)); claim codes passed with two accounts ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/claim-2026-10-17.md)); signed updates with automatic revert passed on the kit ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ota-2026-10-17.md)) | Another person's reproduction; other boards and routers; Android Grok Bot calls |
| Home Assistant probe | Read-only discovery against fixtures | A real Home Assistant home |
| Browser playground | Local JavaScript model of the light | — (it never calls Grok Bot) |

## What "verified" means here

- **Software:** tests, builds and local MCP calls. A device acknowledgement is the device's
  report, not proof of a physical effect.
- **Grok Bot:** its cloud computer cannot reach your private LAN on its own. The owner's setup has two working routes. Approved local commands ran on the Mac (12 October). Native tool calls came from the desktop and phone apps through an owner-run HTTPS tunnel with sign-in (13 October). The gateway log recorded nine calls with the `grok-bot` sign-in, and the owner saw the text on the OLED ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/grok-remote-https-2026-10-13.md)). Mac-to-Pi SSH remains a conditional, untested route. See the [connection paths](../getting-started/hosting.md).
- **Remote MCP:** `serve` listens on `127.0.0.1:8766/mcp`. With `--allowed-host` and `--oauth`, an operator-run tunnel gives Grok Bot an HTTPS endpoint. Accounts mode accepts a gadget claim code at sign-in. Legacy operator approval happens on the gateway host. The project runs no public endpoint. A tunnel does not add authentication; the sign-in does. Button events do not wake the Bot.
- **Hardware:** needs a person to observe the board. On 12 October 2026 the owner flashed the ESP32-S3 + OLED kit. They observed text, clear, the RGB light, the BOOT button, replug and gateway restart ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-2026-10-12.md)).
  The same day the kit ran over Wi-Fi from a USB charger. The owner observed boot, text, clear, BOOT, Wi-Fi loss and recovery, gateway restart, revocation, wrong-CA rejection and power cycle ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md)).

Tested component versions are in the [compatibility manifest](../../compatibility/tested-components.json).
See [how we verify](how-we-verify.md) for the local command log and physical observations.
How the parts connect and who runs what: [hosting FAQ](../getting-started/hosting.md).
Dated evidence for maintainers starts at the [verification record](local-status.md).
