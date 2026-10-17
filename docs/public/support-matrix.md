# Project status

Updated 17 October 2026. This is the one place that says what works. Other pages link here
instead of repeating caveats.

**Alpha · one owner-tested kit · phone setup · claim by code · Grok Bot calls through an always-on gateway.**

On 13 October 2026 the owner's Grok Bot called the six tools itself from the Mac and the iPhone. It used an owner-run tunnel with sign-in ([ADR 007](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/007-grok-bot-remote-https.md)). [Connect your Grok Bot](../getting-started/connect-grok-bot.md).

## Current releases

| Component | Release | Package |
| --- | --- | --- |
| Hub | `v0.1.16-alpha.2` | [GitHub release](https://github.com/adidshaft/grok-gadgets/releases/tag/v0.1.16-alpha.2) |
| Gateway | `v0.1.0-alpha.15` | [PyPI `0.1.0a15`](https://pypi.org/project/grok-gadgets-gateway/) |
| ESP32 SDK | `v0.2.0-alpha.16` | [GitHub release](https://github.com/adidshaft/grok-gadgets-esp32-sdk/releases/tag/v0.2.0-alpha.16) |
| Linux SDK | `v0.1.0-alpha.7` | [PyPI `0.1.0a7`](https://pypi.org/project/grok-gadgets-linux-sdk/) |
| Home Assistant | `v0.1.0-alpha.5` | [PyPI `0.1.0a5`](https://pypi.org/project/grok-gadgets-home-assistant/) |

## Today, next, later

**Today:** the kit connects to a gateway on an always-on Linux server.
The earlier Mac-hosted route passed Phase 8 for one day. During Mac sleep, that route failed and queued nothing.
See the [daily record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md).

**Phase 9:** the gateway can run on an always-on Linux server, so the Mac can sleep.
On 13 October 2026 the owner's iPhone, on cellular, showed text on the kit while the Mac slept ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/mac-free-route-2026-10-13.md)).

**Phase 10:** a factory-provisioned gadget joins home Wi-Fi from a phone alone, through its setup hotspot.
On 14 October 2026 the owner joined the kit from an iPhone and an Android phone. The owner kept the Mac closed during iPhone setup. The kit went Online through the relay, and Grok Bot on the iPhone showed text on it ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/phone-setup-2026-10-14.md), [guide](../getting-started/phone-setup.md)).

Android Grok Bot calls remain untested. The owner's relay runs gateway `0.1.0a15` on device port 8443.
New relays use port 8444 by default.

**Phase 11:** each person claims a gadget with the code on its screen, and their Grok Bot sees only their gadgets.
On 17 October 2026 two people tested this on the owner's relay and kit, each with Grok Bot on their own iPhone. Claim, isolation, share and revoke, wrong and expired codes, a flood and a hand-over after a reset all passed ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/claim-2026-10-17.md), [guide](../getting-started/claim-your-gadget.md)).

**Next:** Phase 12 adds a kit for builders.

**Later:** Phase 12b adds updates over the air.
Phase 13 is only a decision on a shared relay. The project hosts no service.
See the [roadmap](../../ROADMAP.md) for acceptance gates.

**Help test:** another day, measured usage and [an independent kit report](https://github.com/adidshaft/grok-gadgets/issues/185) remain open.
A button event does not wake Grok Bot.

| Part | What works today | Not verified yet |
| --- | --- | --- |
| Gateway and simulated light | Six MCP tools over stdio or authenticated HTTP on `127.0.0.1`; `rehearse` first success; approved Grok Bot local commands; native Grok Bot calls from Mac and iPhone through an owner-run tunnel with OAuth sign-in, tested for one day behind a fixed hostname (gateway `0.1.0a12`); sign-in flood limits, log rotation and route status; usage summary and hook; simulator kit; private LAN TLS for Wi-Fi devices; optional per-user launchd/systemd service; an always-on Linux relay with iPhone calls while the Mac sleeps; accounts with claim codes, shares, names and hand-over, tested by two people (gateway `0.1.0a15`) | Android Grok Bot calls; a second day and a calibrated usage rate; Team Bots; Windows and Intel Mac installs |
| Linux SDK | PyPI `0.1.0a7` and `grok-linux-agent dev ./my_gadget.py` with the decorator API | Real peripherals, systemd on a physical Linux host, Raspberry Pi hardware |
| ESP32 SDK | Host tests, four firmware builds compile, simulated USB link to the gateway. The ESP32-S3 + OLED kit passed physical tests on the owner's board over USB ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-2026-10-12.md)) and over Wi-Fi from a USB charger ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md)); phone setup passed on iPhone and Android ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/phone-setup-2026-10-14.md)); claim codes passed with two accounts ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/claim-2026-10-17.md)) | Another person's reproduction; other boards and routers; Android Grok Bot calls |
| Home Assistant probe | Read-only discovery against fixtures | A real Home Assistant home |
| Browser playground | Local JavaScript model of the light | — (it never calls Grok Bot) |

## What "verified" means here

- **Software:** tests, builds and local MCP calls. A device acknowledgement is the device's
  report, not proof of a physical effect.
- **Grok Bot:** its cloud computer cannot reach your private LAN on its own. The owner's setup has two working routes. Approved local commands ran on the Mac (12 October). Native tool calls came from the desktop and phone apps through an owner-run HTTPS tunnel with sign-in (13 October). The gateway log recorded nine calls with the `grok-bot` sign-in, and the owner saw the text on the OLED ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/grok-remote-https-2026-10-13.md)). Mac-to-Pi SSH remains a conditional, untested route. See the [connection paths](../getting-started/hosting.md).
- **Remote MCP:** `serve` listens on `127.0.0.1:8766/mcp`. With `--allowed-host` and `--oauth`, an owner-run tunnel gives Grok Bot an HTTPS endpoint, and the owner approves each sign-in on the gateway host. The project runs no public endpoint. A tunnel does not add authentication; the sign-in does. Button events do not wake the Bot.
- **Hardware:** needs a person to observe the board. On 12 October 2026 the owner flashed the ESP32-S3 + OLED kit. They observed text, clear, the RGB light, the BOOT button, replug and gateway restart ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-2026-10-12.md)).
  The same day the kit ran over Wi-Fi from a USB charger. The owner observed boot, text, clear, BOOT, Wi-Fi loss and recovery, gateway restart, revocation, wrong-CA rejection and power cycle ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md)).

Tested component versions are in the [compatibility manifest](../../compatibility/tested-components.json).
See [how we verify](how-we-verify.md) for the local command log and physical observations.
How the parts connect and who runs what: [hosting FAQ](../getting-started/hosting.md).
Dated evidence for maintainers starts at the [verification record](local-status.md).
