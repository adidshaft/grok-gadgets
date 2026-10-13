# How we verify Grok Gadgets

Each claim has a different check. A successful command reply is a software result; it does not, by itself, show what happened on a board.

## Software and local commands

The gateway's `rehearse` command calls its six MCP tools against a simulated light and checks the returned state. In the [12 October local Grok Bot run](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/grok-local-execution-2026-10-12.md), native command approval and an independently retrieved gateway log matched in time. The public record includes these redacted log fields:

```text
tool: gadgets_command
capability: rgb.set
status: executed
simulated: true
```

That run verifies an approved local command on the owner's Mac. It does not verify native Grok Bot MCP tool discovery or a physical light.

## The owner's physical kit

The owner separately observed text and clear on the 1.3-inch OLED, the onboard RGB light, BOOT press and release, and recovery after unplugging the board. The [USB record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-2026-10-12.md) pairs command replies with those observations. The [Wi-Fi record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md) records the board running from a USB charger, its Online display, recovery, token revocation and wrong-certificate rejection.

The [repeatable kit guide](../getting-started/repeat-the-kit.md) is ready for another person's run. [Share a result in tester issue #185](https://github.com/adidshaft/grok-gadgets/issues/185), including failures and skipped steps.

## The always-on Wi-Fi run

On 12–13 October, the owner saw **Online** on the OLED after setting up the gateway as a per-user Mac service. The [gateway record](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/verification/always-on-2026-10-13.md) pairs that observation with `lan_connected` and `lan_hello` log events. On two Mac address changes, the log recorded `lan_rebound`, followed by `lan_hello`; the board returned Online without a new certificate or provisioning.

After one Mac restart and login, the board showed **Gateway...** for about 90 seconds, then **Online**. The service started without a terminal and the log recorded `lan_hello`. This is one owner setup, not an independent run. A later service change aims to reduce the delay; its post-restart effect remains untested in [gateway issue #115](https://github.com/adidshaft/grok-gadgets-gateway/issues/115).

## Connection still to verify

The gateway can serve authenticated MCP on loopback. A remote HTTPS endpoint and native Grok Bot tool calls on Mac and phone need a separate owner-approved test. [Project status](support-matrix.md) tracks that gate and the current component versions.
