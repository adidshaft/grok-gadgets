# Hosting and remote access

The website serves documentation and a simulator. It does not run your gateway.
The gateway operator runs the connection service. SpaceXSI runs Grok Bot.

## The verified route

Grok Bot on Mac and iPhone calls the six gadget tools through an owner-run HTTPS tunnel with OAuth sign-in.
The operator approves sign-in on the Mac. The gateway and tunnel run there; the board connects over private LAN TLS.

```text
Grok Bot on Mac or iPhone
    → HTTPS tunnel → gateway on the Mac → private LAN TLS → Wi-Fi gadget
```

The owner's setup passed [one day of checks](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md).
The phone also worked on cellular. This does not remove the gateway's Mac dependency.
During Mac sleep, the route failed and queued nothing.
After restart, the gateway listened at 66 seconds; the board returned Online at 72 seconds.
Another day, measured usage and an independent report remain open.

Start with [Connect your Grok Bot](connect-grok-bot.md).
The personal app adds the server from chat with a URL, then uses OAuth sign-in.
Do not assume that its setup form accepts bearer headers.

## Keep the listeners separate

| Listener | Purpose | Exposure |
| --- | --- | --- |
| `127.0.0.1:8766/mcp` | Grok Bot tools | Owner-run HTTPS tunnel; allowed host and OAuth required for the verified route |
| `127.0.0.1:8765` | Local device traffic | Loopback only; never expose it through the tunnel |
| Private LAN TLS listener | Wi-Fi device traffic | Private network only; never port-forward the current listener |

A tunnel supplies reachability. OAuth supplies sign-in authorization.
See the gateway [remote access guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/remote-access.md) for configuration and controls.

## Next: a gateway away from the Mac

[ADR 009](../decisions/009-relay-route.md) proposes a relay: the existing gateway on an always-on Linux host.
The gadget would connect out to that host over TLS. Grok Bot would keep the HTTPS and OAuth route.
The owner must choose the host, device hostname and tunnel move before implementation.
The project runs no relay service. Phone-only setup and claim codes belong to later phases.

## Advanced local commands

The owner's approved `grok-gadgets-gateway rehearse` commands also reached the simulator and the physical OLED kit.
This route runs a command on the Mac. It is separate from native tool calls.
See the [local-command record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/grok-local-execution-2026-10-12.md).

An approved Mac command could use SSH to reach a configured Raspberry Pi on the same network.
That extension remains unverified. Both hosts and the SSH permissions must be available.
A USB cable does not create an SSH or remote MCP connection.

Grok Bot's cloud computer cannot reach your private network without a configured route.
`127.0.0.1` always refers to the computer where the connection runs.
A device button does not wake Grok Bot; its events wait for a tool read.

## Next step

[Connect Grok Bot](connect-grok-bot.md) · [Fix a connection](troubleshooting.md) · [Current support](../public/support-matrix.md) · [All documentation](../index.md)
