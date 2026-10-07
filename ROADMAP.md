# Roadmap

The software is an experimental alpha. Public source repositories and the static website are active. [GitHub Issues](https://github.com/adidshaft/grok-gadgets/issues) track public work.

**Local `serve` is implemented** with bearer authentication at `127.0.0.1:8766/mcp`. It is loopback-only. The remote MCP endpoint and a verified Grok Bot invocation are not complete. A tunnel adds reachability, not authentication.

Grok Bot normally runs on its cloud computer. This does not expose your private LAN. Its separate **Execution on Local Computer** capability can run an approved Mac command when enabled. With network reachability and SSH configured, that command can reach a Pi. This is a possible manual experiment, not shipped or accepted Grok Gadgets support. USB alone does not create the route. See the [three-path hosting FAQ](docs/getting-started/hosting.md).

- **M5 — Actual Grok: blocked.** Obtain supported invocation and reload evidence for the exact kit, and complete the authenticated remote route. Independently retrieved logs and transcript observation are required; a Bot narrative is not proof.
- **M8 — Physical and independent verification: blocked.** Set up a real Pi or device, observe its peripheral operation, and obtain independent reproduction.

[HARD-GROK-REMOTE-001](https://github.com/adidshaft/grok-gadgets/issues/4) tracks secure remote access. Do not point Grok Bot at this alpha yet.

| Milestone | What closes it |
|---|---|
| Honest local alpha | Website, checks, and docs that say what Grok Bot can and cannot do |
| Local HTTP gateway (`serve`) | Implemented and software-tested on loopback; not Grok-verified |
| Bounded Grok experiment | Operator-owned HTTP logs plus transcript observation; Grok Bot Remote HTTPS still unverified |
| First physical C124 build | Observed LED/button and USB recovery on real hardware |
| Remote connection and provisioning | Tunnel or relay, pairing, and separately approved activation |
| Real Linux and Home Assistant | Selected real service/peripheral/home paths verified |

[Ready contribution queue](docs/contributing/ready-issues.md) · [contribution process](CONTRIBUTING.md). No invented completion percentage.
