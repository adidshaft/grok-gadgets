# Hosting and remote access

There are three separate paths. The website serves documentation and a browser simulator. It does not run your gateway. The owner's Grok Bot used an approved local command to reach the gateway; native MCP calls remain unverified. The Wi-Fi kit can use the gateway's optional per-user service, which starts after Mac login or under a Linux user session.

## 1. Grok Bot on its cloud computer

Grok Bot normally works on its cloud computer. Its internet connection does not give it access to your private home network. A path on your Mac is not a path on that cloud computer. The address `127.0.0.1` refers to the computer where the command runs.

## 2. Local execution on a Mac, then SSH to a Pi

Grok Bot has a separate **Execution on Local Computer** capability. If you enable it and approve a command, Grok Bot can run that command on your Mac.

A command on the Mac can connect to your Raspberry Pi through SSH. For this, the Mac must reach the Pi over the home network, and you must set up SSH. Both computers must be available. The SSH user must have permission to do the requested work.

The Mac-to-Pi SSH path is a possible manual experiment. It has not been tested as Grok Gadgets support. USB alone does not create this route.

On 12 October 2026 the owner's Grok Bot ran two approved `grok-gadgets-gateway rehearse` commands on the owner's Mac. The gateway request log recorded the matching calls against a simulated light. Later, the same local-command route showed text on the owner's physical OLED over USB and Wi-Fi. Grok Bot did not add the gateway as an MCP server. The approved command is a working local route, not a native tool connection. See the [local-command issue](https://github.com/adidshaft/grok-gadgets/issues/31) and [Wi-Fi kit record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md).

For Wi-Fi, the board can draw power from a USB charger. The gateway must still run on the Mac. Its optional per-user service can start the private LAN TLS listener at login. Provisioning with the Mac's `.local` name lets the gateway re-resolve and rebind after an address change. The owner's board recovered after two address changes without a new certificate or provisioning. One restart/login run took about 90 seconds to return Online; faster recovery needs a retest. Follow the [kit guide](repeat-the-kit.md) and [always-on guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/always-on.md).

## 3. Grok Gadgets remote MCP

The gateway's local `serve` mode is implemented. It provides Streamable HTTP MCP at `http://127.0.0.1:8766/mcp`, with a bearer token read from a file. It listens on loopback only.

A packaged public route and native Grok Bot MCP calls have not passed acceptance. A tunnel can make a service reachable; it does not add authentication. Do not expose the device port at `127.0.0.1:8765` or publish the gateway as an accepted public MCP service.

**Wi-Fi devices use a separate listener.** `serve --lan-listen <private address>` carries device traffic over private LAN TLS ([ADR 005](https://github.com/adidshaft/grok-gadgets/blob/dev/docs/decisions/005-wifi-device-route.md)). It is not a Grok Bot MCP endpoint. Never forward its port or put it behind a tunnel.

## Connection diagram

```text
Default:      Grok Bot → cloud computer → internet
                                          ✕ private home LAN

Possible:     Grok Bot → enabled local execution + command approval
                       → Mac → configured SSH over home LAN → Pi
                       Manual experiment; not product verification

Product goal: Grok Bot → authenticated remote MCP endpoint with TLS
                       → local gateway → device
                       Remote endpoint and Bot invocation incomplete
```

## Build stage

| Gate | Current stage | Evidence needed |
| --- | --- | --- |
| Local gateway `serve` | Implemented on loopback | Local software evidence does not prove a Grok Bot connection. |
| M5 — Actual Grok | Partly done | Approved local `rehearse` commands work. Native tool calls need the authenticated remote route. |
| M8 — Physical and independent verification | Partly done | The owner's ESP32-S3/OLED kit passed USB and Wi-Fi tests. Independent reproduction and a real Pi setup remain open. |

[HARD-GROK-REMOTE-001](https://github.com/adidshaft/grok-gadgets/issues/4) tracks secure remote access. The existing loopback listener is separate from that unfinished work. See the [roadmap](../../ROADMAP.md) and gateway [remote access guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/remote-access.md).

## Simple FAQ

**Can the Mac app reach my Pi?** An approved local command can use SSH if the Mac can reach the Pi and SSH is configured. We have not verified this route as Grok Gadgets support.

**Does internet access let the cloud Bot reach my Pi?** No. A private home network is not exposed by the Bot's internet connection.

**Does USB make the Mac a bridge?** No. A cable does not configure local execution, network access, SSH, or MCP.

**Does enabling local execution install Grok Gadgets MCP?** No. Local command execution and MCP configuration are separate. In the 12 October test, Grok Bot declined both MCP server types for the gateway on the Mac.

**Who runs the MCP server?** The gateway operator runs it. SpaceXSI runs Grok Bot. A Home Assistant operator runs Home Assistant's own MCP server.

**What can I use now?** Build the [tested ESP32-S3/OLED kit](repeat-the-kit.md), or use the [browser playground](https://grokgadgets.org/playground) and [simulator kit](simulator-kit.md) without hardware. The owner's Grok Bot used the approved local-command route to show text on that kit. Native MCP support and another person's reproduction remain open.

**Does a button wake Grok Bot?** No. Events wait in the gateway until a client calls `gadgets_read_events`.

**Are Command MCP and local execution the same?** No. A Command MCP process on the cloud computer uses that computer's paths and network. Local execution runs an approved command on your Mac. Neither establishes packaged Grok Gadgets remote MCP support.

## Platform sources

The official [computer and apps guide](https://docs.x.ai/grok-bot/computer-and-apps) separates the cloud computer from approved local command execution. The [approval guide](https://docs.x.ai/grok-bot/approvals-security-and-privacy) describes permissions. These platform capabilities are not evidence of a verified Grok Gadgets connection. The Mac-to-Pi route above is a conditional networking inference, not a recorded product test.
