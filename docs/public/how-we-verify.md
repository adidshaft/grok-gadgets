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

After one Mac restart and login, the board showed **Gateway...** for about 90 seconds, then **Online**. The service started without a terminal and the log recorded `lan_hello`. This is one owner setup, not an independent run. The [13 October daily record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md) adds a post-fix restart observation.
The gateway listened 66 seconds after boot and the board returned Online at 72 seconds.
The login timestamp has minute precision. These times do not establish an exact improvement after login.

## Native calls and one-day checks

On 13 October, Grok Bot called all six tools from the owner's Mac and iPhone apps through Remote HTTPS and OAuth.
The [native record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/grok-remote-https-2026-10-13.md) pairs gateway logs with the owner's observations.
The [daily record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md) covers cellular access, gateway restart, Mac sleep and restart, log rotation and sign-in limits.
During sleep, the route failed and queued nothing.

This is one day on one setup. Another day, a calibrated usage rate and another person's run remain open.
Whole-percent usage readings did not resolve the usage change. They do not prove zero cost per call.

[Project status](support-matrix.md) lists releases and gates. [Troubleshooting](../getting-started/troubleshooting.md) helps locate a failed connection.
