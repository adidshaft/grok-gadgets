# Project status

Updated 20 October 2026. This is the one place that says what works. Other pages link here
instead of repeating caveats.

**Alpha · one owner-tested kit · phone setup · claim by code · signed updates · Grok Bot on iPhone and Android.**

On 13 October 2026 the owner's Grok Bot called the six tools itself from the Mac and the iPhone. It used an owner-run tunnel with sign-in ([ADR 007](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/007-grok-bot-remote-https.md)). [Connect your Grok Bot](../getting-started/connect-grok-bot.md).

## Current releases

| Component | Release | Package |
| --- | --- | --- |
| Hub | `v0.1.19-alpha.2` | [GitHub release](https://github.com/adidshaft/grok-gadgets/releases/tag/v0.1.19-alpha.2) |
| Gateway | `v0.1.0-alpha.19` | [PyPI `0.1.0a19`](https://pypi.org/project/grok-gadgets-gateway/) |
| ESP32 SDK | `v0.2.0-alpha.19` | [GitHub release](https://github.com/adidshaft/grok-gadgets-esp32-sdk/releases/tag/v0.2.0-alpha.19) |
| Linux SDK | `v0.1.0-alpha.10` | [PyPI `0.1.0a10`](https://pypi.org/project/grok-gadgets-linux-sdk/) |
| Home Assistant | `v0.1.0-alpha.5` | [PyPI `0.1.0a5`](https://pypi.org/project/grok-gadgets-home-assistant/) |

## What you can do today

The owner-tested path uses one ESP32-S3/OLED kit and an always-on Linux relay.
The Mac can sleep. The project hosts no relay.

| Task | Guide | Evidence |
| --- | --- | --- |
| Join home Wi-Fi from a phone with a prepared gadget, with no data cable | [Phone setup](../getting-started/phone-setup.md) | Owner's iPhone and Android; [14 October record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/phone-setup-2026-10-14.md) |
| Claim, name and share a gadget | [Claim your gadget](../getting-started/claim-your-gadget.md) | Two people, their own iPhones, one relay and kit; [17 October record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/claim-2026-10-17.md) |
| Show text from Grok Bot while the Mac sleeps | [Mac-free route](../getting-started/mac-free-route.md) | Owner's iPhone on cellular; [13 October record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/mac-free-route-2026-10-13.md) |
| Send signed firmware updates with automatic revert | [Sign and ship an update](../getting-started/sign-and-ship-an-update.md) | Owner's kit, including a power cut during download; [17 October record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ota-2026-10-17.md) |
| Set up a relay and prepare a gadget batch | [Ship a gadget](../getting-started/ship-a-gadget.md) | Clean-room software run and owner's dry run on a fresh host; [Builder record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/builder-kit-2026-10-17.md) |

The Linux SDK provides a decorator API, a development runner and a relay client over TLS.
Two simulated Linux batch gadgets went Online on a fresh relay; see the [builder record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/builder-kit-2026-10-17.md).
The [simulator kit](../getting-started/simulator-kit.md) rehearses gateway tools without hardware.
The browser playground models a light locally; it does not call Grok Bot.

The owner's relay runs gateway `0.1.0a19` on device port 8443.
The kit runs `0.2.0-alpha.19` with long-poll. New relays use port 8444 by default.
A reset keeps account ownership. The automatic 7-day transfer has software-clock tests only.
See [Hand a gadget to someone](../getting-started/hand-a-gadget-to-someone.md) for the transfer rules.

## Phase 13: accepted on 20 October

The load test, clearer sign-in page and Android kit check passed.
[ADR 014](../decisions/014-ready-for-others.md) is accepted; [the record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ready-for-others-2026-10-18.md) gives the evidence and limits.

- **Sign-in watch:** 18 October 13:44 to 20 October 04:45 UTC, about 39 hours.
  The owner ended the planned three-day watch early.
  There were 26 refreshes, no fresh owner sign-in and no 401 after access-token expiry.
  The Android test added one sign-in for the second account.
- **Android:** the owner's Grok Bot claimed the kit by code and showed text on 18 October.
  Grok Bot uses dynamic registration. Its Client ID Metadata Document route remains untested; a scripted client passed.
- **Relay size:** a relay holds 64 gadgets by default.
  Gateway `0.1.0a18` added `serve --max-devices`, up to 2,000. This setting is a limit, not a capacity guarantee.

Each load test ran for 15 minutes on one 512 MB, 1-vCPU host with simulated gadgets:

| Gadgets | Polling | Relay CPU (mean) | Relay memory (peak) | Command latency p95 |
| --- | --- | --- | --- | --- |
| 200 | every 100 ms | 61 % | 88 MB | 304 ms |
| 1,000 | long-poll, 2.5 s wait | 67 % | 137 MB | 406 ms |

1,000 gadgets polling every 100 ms did not fit that host.
These simulated runs do not establish physical gadget capacity or long-term reliability.
Long-poll lets the relay wait for a command before answering a gadget's request.
It reduces repeated requests while the gadget is idle.

The 39-hour watch does not explain the two earlier 401 responses on gateway `0.1.0a16`.
See the [scoped sign-in limits](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ready-for-others-2026-10-18.md#sign-in-watch-tier-owner-1820-october-2026).

## What still needs a report

| Area | Remaining checks |
| --- | --- |
| Independent reproduction | Another person's kit report [#185](https://github.com/adidshaft/grok-gadgets/issues/185) and outside builder report [#269](https://github.com/adidshaft/grok-gadgets/issues/269) |
| Grok Bot and sign-in | Metadata-document route, 30-day refresh lifetime, Team Bots and a calibrated usage rate |
| Platforms | Windows and Intel Mac installs |
| Linux SDK | Long-poll on physical Linux hardware, real peripherals, systemd on a physical host and Raspberry Pi hardware |
| ESP32 SDK | Climate sensor, switch and servo examples compile and pass host tests; hardware checks remain. Other boards and routers also need reports. |
| Home Assistant | Discovery passed against fixtures; a real home remains untested. |

**Next:** independent kit and builder reports. Use the issue templates to state versions, steps and observed results.
**Later:** Phase 14 is only a decision on a shared relay.
See the [roadmap](../../ROADMAP.md) for acceptance gates.
A button event does not wake Grok Bot.

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
