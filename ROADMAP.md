# Roadmap

The software is an experimental alpha. Public source repositories and the static website are active. [GitHub Issues](https://github.com/adidshaft/grok-gadgets/issues) track public work.

**Local `serve` is implemented** with bearer authentication at `127.0.0.1:8766/mcp`. It is loopback-only. Grok Bot runs approved `rehearse` commands on the owner's Mac ([ADR 004](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/004-grok-bot-route.md)). The remote MCP endpoint and native Grok Bot tool calls are not complete. A tunnel adds reachability, not authentication.

Grok Bot normally runs on its cloud computer. This does not expose your private LAN. Its separate **Execution on Local Computer** capability can run an approved Mac command when enabled. With network reachability and SSH configured, that command can reach a Pi. This is a possible manual experiment, not shipped or accepted Grok Gadgets support. USB alone does not create the route. See the [three-path hosting FAQ](docs/getting-started/hosting.md).

- **M5 — Actual Grok: partly done.** On 12 October 2026 Grok Bot ran approved `rehearse` commands, recorded in the gateway request log, against the simulated light and the real OLED. Native Grok Bot tool calls need the authenticated remote route. A Bot narrative is not proof.
- **M8 — Physical and independent verification: partly done.** The owner's ESP32-S3 + SH1106 OLED kit passed USB and Wi-Fi acceptance on 12 October 2026 ([USB record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-2026-10-12.md), [Wi-Fi record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md)). Still needed: another person's reproduction and a real Raspberry Pi setup.

[HARD-GROK-REMOTE-001](https://github.com/adidshaft/grok-gadgets/issues/4) tracks secure remote access. Do not add this alpha to Grok Bot as a remote MCP server yet.

| Milestone | What closes it |
|---|---|
| Honest local alpha | Website, checks, and docs that say what Grok Bot can and cannot do |
| Local HTTP gateway (`serve`) | Implemented and software-tested on loopback; not Grok-verified |
| Bounded Grok experiment | Done for approved local `rehearse` commands (gateway request log plus owner observation); native tool calls still unverified |
| First physical ESP32-S3/OLED experiment | Passed on the owner's kit over USB and Wi-Fi; closes when another person repeats it |
| Remote connection and provisioning | Tunnel or relay, pairing, and separately approved activation |
| Real Linux and Home Assistant | Selected real service/peripheral/home paths verified |

[Ready contribution queue](docs/contributing/ready-issues.md) · [contribution process](CONTRIBUTING.md). No invented completion percentage.

The [kit page](docs/getting-started/experiment-kit.md) lists the parts that arrived, the tested wiring (SH1106 at `0x3c` on GPIO8/GPIO9) and the staged checks.
