# Roadmap

The software is an experimental alpha. Public source repositories, the static website and three PyPI packages are active. [GitHub Issues](https://github.com/adidshaft/grok-gadgets/issues) track public work. [Project status](docs/public/support-matrix.md) lists current releases and evidence.

## Phases

| Phase | State | Next evidence |
| --- | --- | --- |
| 1–6: local tools, physical kit and optional always-on service | Owner-tested work done | Independent kit run in [#185](https://github.com/adidshaft/grok-gadgets/issues/185); post-login recovery retest |
| 7: native Grok Bot connection | Done on the owner's setup (13 October 2026) | Another person's native connection |
| 8: daily native route | Done on the owner's setup (13 October 2026, [record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/daily-route-2026-10-13.md)) | Not done: a second separate day of use and a calibrated usage rate |
| 9: setup without a cable | Later | Hotspot or BLE-assisted initial setup and short-code pairing; daily use stays on Wi-Fi |
| 10: optional hosted relay | Decision pending | Owner decision on service operation and scope |

**Grok Bot calls the tools natively.** On 13 October 2026 the owner's Grok Bot called the six tools from the Mac and the iPhone apps through `serve --oauth` behind an owner-run tunnel; the gateway request log recorded each call ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/grok-remote-https-2026-10-13.md), [ADR 007](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/007-grok-bot-remote-https.md)). `serve` still listens on `127.0.0.1:8766/mcp` only. A tunnel adds reachability; the owner-approved sign-in adds authentication.

Grok Bot normally runs on its cloud computer. This does not expose your private LAN. Its separate **Execution on Local Computer** capability ran two approved `rehearse` commands on the owner's Mac. Gateway logs matched those commands. A physical ESP32-S3/OLED kit also passed USB and Wi-Fi acceptance. The gateway still runs on the Mac for the wireless setup. See the [hosting FAQ](docs/getting-started/hosting.md) and [physical records](docs/getting-started/experiment-kit.md).

- **M5 — Actual Grok: done on the owner's setup.** Approved local commands and native tool calls from the Mac and phone apps both reached the gateway and showed text on the physical kit. Another person's reproduction is still open.
- **M8 — Physical and independent verification: partly done.** The owner's delivered kit passed USB and Wi-Fi acceptance. Another person must reproduce the setup.

Phase 8 ([HUB-DAILY-001](https://github.com/adidshaft/grok-gadgets/issues/251)) left the remote route on behind a fixed hostname with gateway `0.1.0a12`. Calls worked from the Mac and from the phone on cellular. The route came back after a gateway restart, Mac sleep and a Mac restart. The Mac must stay on and awake.

| Milestone | What closes it |
|---|---|
| Honest local alpha | Website, checks, and docs that say what Grok Bot can and cannot do |
| Local HTTP gateway (`serve`) | Implemented and software-tested on loopback; the approved local Grok Bot commands used `rehearse`, not this HTTP endpoint |
| Bounded Grok experiment | Owner-approved local command and matching gateway log; native Grok Bot calls through the remote route on 13 October 2026 |
| First physical ESP32-S3/OLED experiment | Owner observed text, clear, RGB, BOOT, USB recovery and Wi-Fi recovery; independent reproduction remains open |
| Remote connection and provisioning | Owner-run tunnel with sign-in works; daily use (Phase 8), setup without a cable and any relay remain |
| Real Linux and Home Assistant | Selected real service/peripheral/home paths verified |

[Ready contribution queue](docs/contributing/ready-issues.md) · [contribution process](CONTRIBUTING.md). No invented completion percentage.

The [tested kit guide](docs/getting-started/experiment-kit.md) lists the delivered parts and wiring. Follow the [repeatable setup](docs/getting-started/repeat-the-kit.md) to try the same kit.
