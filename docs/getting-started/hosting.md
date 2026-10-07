# Hosting and remote access

There are three separate paths. Only local gateway software is implemented in Grok Gadgets. The website serves documentation and a browser simulator. It does not run your gateway.

## 1. Grok Bot on its cloud computer

Grok Bot normally works on its cloud computer. Its internet connection does not give it access to your private home network. A path on your Mac is not a path on that cloud computer. The address `127.0.0.1` refers to the computer where the command runs.

## 2. Local execution on a Mac, then SSH to a Pi

Grok Bot has a separate **Execution on Local Computer** capability. If you enable it and approve a command, Grok Bot can run that command on your Mac.

A command on the Mac can connect to your Raspberry Pi through SSH. For this, the Mac must reach the Pi over the home network, and you must set up SSH. Both computers must be available. The SSH user must have permission to do the requested work.

This is a possible manual experiment. It is not verified Grok Gadgets product support. It is not a ready-to-use MCP integration. Connecting a USB cable alone does not create this route.

## 3. Grok Gadgets remote MCP

The gateway's local `serve` mode is implemented. It provides Streamable HTTP MCP at `http://127.0.0.1:8766/mcp`, with a bearer token read from a file. It listens on loopback only.

A packaged, authenticated remote endpoint with TLS, suitable credentials or OAuth, and an approved, verified Grok Bot invocation is not complete. A tunnel can make a service reachable. It does not add authentication. Do not point Grok Bot at this alpha yet. Do not publish the device port at `127.0.0.1:8765`.

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
| M5 — Actual Grok | Blocked | Supported invocation and reload evidence for the exact simulator kit, plus the authenticated remote route. |
| M8 — Physical and independent verification | Blocked | A real Pi or device setup, observed peripheral operation, and independent reproduction. |

[HARD-GROK-REMOTE-001](https://github.com/adidshaft/grok-gadgets/issues/4) tracks secure remote access. The existing loopback listener is separate from that unfinished work. See the [roadmap](../../ROADMAP.md) and gateway [remote access guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/remote-access.md).

## Simple FAQ

**Can the Mac app reach my Pi?** An approved local command can use SSH if the Mac can reach the Pi and SSH is configured. We have not verified this route as Grok Gadgets support.

**Does internet access let the cloud Bot reach my Pi?** No. A private home network is not exposed by the Bot's internet connection.

**Does USB make the Mac a bridge?** No. A cable does not configure local execution, network access, SSH, or MCP.

**Does enabling local execution install Grok Gadgets MCP?** No. Local command execution and MCP configuration are separate.

**Who runs the MCP server?** The gateway operator runs it. SpaceXAI runs Grok Bot. A Home Assistant operator runs Home Assistant's own MCP server.

**What can I use now?** Use the [browser simulator](https://grokgadgets.org/#playground), the [simulator kit](simulator-kit.md), or the local gateway with `grok-gadgets-gateway rehearse`. These do not prove that Grok Bot can control a physical device.

**Does a button wake Grok Bot?** No. Events wait in the gateway until a client calls `gadgets_read_events`.

**Are Command MCP and local execution the same?** No. A Command MCP process on the cloud computer uses that computer's paths and network. Local execution runs an approved command on your Mac. Neither establishes packaged Grok Gadgets remote MCP support.

## Platform sources

The official [computer and apps guide](https://docs.x.ai/grok-bot/computer-and-apps) separates the cloud computer from approved local command execution. The [approval guide](https://docs.x.ai/grok-bot/approvals-security-and-privacy) describes permissions. These platform capabilities are not evidence of a verified Grok Gadgets connection. The Mac-to-Pi route above is a conditional networking inference, not a recorded product test.
