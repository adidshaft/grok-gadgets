# Roadmap

The software is an experimental alpha. Public source repositories and the static website are active. [GitHub Issues](https://github.com/adidshaft/grok-gadgets/issues) track public work.

**Local `serve` is implemented** with bearer authentication at `127.0.0.1:8766/mcp`. It is loopback-only. Grok Bot ran approved gateway commands on the owner's Mac. Native MCP calls and the remote MCP route remain unverified. A tunnel adds reachability, not authentication.

Grok Bot normally runs on its cloud computer. This does not expose your private LAN. Its separate **Execution on Local Computer** capability ran two approved `rehearse` commands on the owner's Mac. Gateway logs matched those commands. A physical ESP32-S3/OLED kit also passed USB and Wi-Fi acceptance. The gateway still runs on the Mac for the wireless setup. See the [hosting FAQ](docs/getting-started/hosting.md) and [physical records](docs/getting-started/experiment-kit.md).

- **M5 — Actual Grok: partly done.** Approved local commands reached the gateway, including a display command to the physical kit. Native MCP tool calls and the remote route remain open.
- **M8 — Physical and independent verification: partly done.** The owner's delivered kit passed USB and Wi-Fi acceptance. Another person must reproduce the setup.

[HARD-GROK-REMOTE-001](https://github.com/adidshaft/grok-gadgets/issues/4) tracks secure remote access. Do not expose the gateway as a public MCP service yet.

| Milestone | What closes it |
|---|---|
| Honest local alpha | Website, checks, and docs that say what Grok Bot can and cannot do |
| Local HTTP gateway (`serve`) | Implemented and software-tested on loopback; the approved local Grok Bot commands used `rehearse`, not this HTTP endpoint |
| Bounded Grok experiment | Owner-approved local command and matching gateway log; native MCP still unverified |
| First physical ESP32-S3/OLED experiment | Owner observed text, clear, RGB, BOOT, USB recovery and Wi-Fi recovery; independent reproduction remains open |
| Remote connection and provisioning | Tunnel or relay, pairing, and separately approved activation |
| Real Linux and Home Assistant | Selected real service/peripheral/home paths verified |

[Ready contribution queue](docs/contributing/ready-issues.md) · [contribution process](CONTRIBUTING.md). No invented completion percentage.

The [tested kit guide](docs/getting-started/experiment-kit.md) lists the delivered parts and wiring. Follow the [repeatable setup](docs/getting-started/repeat-the-kit.md) to try the same kit.
