# Hosting and remote access

Grok Bot runs in Grok's cloud. The gateway runs on a computer you operate. The project website serves docs and a browser simulator. It does not run anyone's gateway.

## What exists today

| Path | Status |
| --- | --- |
| Browser playground | Works. Does not call Grok. |
| Local stdio MCP | Works with a local MCP client. |
| `serve` at `http://127.0.0.1:8766/mcp` | Implemented. File bearer token. Loopback only. Not used with Grok Bot. |
| Your HTTPS in front of `serve` | You supply TLS. This project does not. Unverified with Grok Bot. |
| Device port `127.0.0.1:8765` | Loopback only. Never publish it. |
| OAuth / per-person scopes | Not shipped. |

A cloud Bot cannot open `127.0.0.1`. A tunnel only moves packets. Keep the bearer token in the client config, not in the URL.

## What you can do now

1. Try the [browser light](https://grokgadgets.org/#playground).
2. Run the [simulator kit](simulator-kit.md) or `grok-gadgets-gateway serve --simulator`.
3. Build a Linux or ESP32 gadget against a gateway on the same computer.

Do not point Grok Bot at this alpha yet. [HARD-GROK-REMOTE-001](https://github.com/adidshaft/grok-gadgets/issues/4) tracks a later experiment. Gateway details: [remote access](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/remote-access.md).

## Common questions

**Who hosts the MCP server?** Whoever runs the gateway. Grok/xAI hosts Grok Bot. Home Assistant operators use Home Assistant's own MCP server.

**Does a gadget button wake Grok?** No. Grok Bot starts work when someone asks, or on a schedule. Events wait in the gateway until the Bot calls `gadgets_read_events`.

**Do local tests prove the cloud route?** No. Keep these separate: local MCP tests, a Grok Bot session, remote security (TLS, identity, scopes), and a physical board.

**Command MCP vs Remote HTTPS.** Command MCP runs on Grok's cloud computer, so a path on your Mac is the wrong path. Remote HTTPS is the documented route for a server with secrets. Local `serve` is the thing you would put behind HTTPS. Neither Bot path is verified here.

Official Grok Bot docs: [Team Bots](https://docs.x.ai/grok-bot/team-bots), [computer and apps](https://docs.x.ai/grok-bot/computer-and-apps). Those pages describe the platform. They do not mean Grok Gadgets supports those routes yet.
