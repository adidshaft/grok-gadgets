# Roadmap

The software is an experimental alpha. Public source repositories and the static website are active. [GitHub Issues](https://github.com/adidshaft/grok-gadgets/issues) track public work.

**Local `serve` is implemented** on the gateway: authenticated Streamable HTTP MCP on `127.0.0.1:8766/mcp`. Grok Bot has not used it. A cloud Bot cannot open loopback. Use independently retrieved server logs and transcript observation as execution evidence. Enterprise log export is not a prerequisite. **Next product work** is a separately approved operator tunnel or Grok Bot Remote HTTPS experiment, not more website packaging. See [HARD-GROK-REMOTE-001](https://github.com/adidshaft/grok-gadgets/issues/4) and the [hosting FAQ](docs/getting-started/hosting.md).

| Milestone | What closes it |
|---|---|
| Honest local alpha | Website, checks, and docs that say what Grok Bot can and cannot do |
| Local HTTP gateway (`serve`) | Implemented and software-tested on loopback; not Grok-verified |
| Bounded Grok experiment | Operator-owned HTTP logs plus transcript observation; Grok Bot Remote HTTPS still unverified |
| First physical C124 build | Observed LED/button and USB recovery on real hardware |
| Remote connection and provisioning | Tunnel or relay, pairing, and separately approved activation |
| Real Linux and Home Assistant | Selected real service/peripheral/home paths verified |

[Ready contribution queue](docs/contributing/ready-issues.md) · [contribution process](CONTRIBUTING.md). No invented completion percentage.
