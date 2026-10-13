# Project verification status

Grok Gadgets is an alpha for your existing Grok Bot. The public site provides docs and a browser simulator. The local gateway provides stdio MCP and authenticated HTTP MCP through `serve`. Grok Bot ran approved `rehearse` commands on the owner's Mac. The gateway log matched them. On 12 October 2026 the same route showed text on a real ESP32-S3 + OLED kit over [USB](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-2026-10-12.md) and [Wi-Fi](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md). On 13 October 2026 Grok Bot also called the tools natively from the Mac and phone apps through an owner-run tunnel with sign-in ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/grok-remote-https-2026-10-13.md)). See the [tested component versions](../../compatibility/tested-components.json).

| Component | Local evidence | Still pending |
| --- | --- | --- |
| Gateway and simulator | Local rehearsal command, authenticated loopback and simulation tests; Grok Bot ran approved `rehearse` commands, recorded in the gateway request log; optional per-user service and private LAN name route passed on the owner's kit | Supported remote route and native Grok Bot tool calls; faster post-login recovery retest |
| Linux SDK | Released PyPI wheel and installed-wheel acceptance on macOS and an isolated Linux container | Physical peripherals and systemd lifecycle on a real Linux host |
| ESP32 SDK / retained reference examples | Host consumer tests, ESP32-S3 compilation, and USB/Wi-Fi physical acceptance of the owner's ESP32-S3 + OLED kit | Independent reproduction, other boards, disconnect during a command |
| Home Assistant | Fixtures and local MCP transport checks | Actual home installation and Grok Bot |
| Website and community | Public static site, fixtures and offline recognition | A hosted gateway and automatic recognition |

## Run locally

From the hub, run:

```sh
python3 scripts/dev.py setup
python3 scripts/dev.py site
```

Open `http://127.0.0.1:4173`. You do not need the sibling repositories to build the website.

Run the gateway's assertion-backed simulator demo:

```sh
cd ../grok-gadgets-gateway
uv sync --locked
uv run python -m grok_gadgets_gateway.demo
```

These operations prove software behavior. They do not prove physical effects or that Grok Bot has called the tools.

## Remaining gates

The [hosting FAQ](../getting-started/hosting.md) describes three separate paths:

- **Cloud computer:** Grok Bot normally runs commands on its cloud computer. Its internet connection does not give it access to your private home network.
- **Local Mac route:** Approved commands reached the owner's gateway and OLED kit. A Mac-to-Pi SSH extension remains untested; it needs a reachable Pi and configured SSH. USB alone does not create that SSH route. Local commands are not packaged native MCP integration.
- **Remote MCP with sign-in:** `serve` listens on `127.0.0.1:8766/mcp`. With `--allowed-host` and `--oauth` behind a tunnel that you run, Grok Bot calls the six tools natively from the Mac and phone apps. The owner's setup did this on 13 October 2026 ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/grok-remote-https-2026-10-13.md)). A tunnel adds reachability; the sign-in that you approve on the Mac adds authentication. Daily use is Phase 8 ([#251](https://github.com/adidshaft/grok-gadgets/issues/251)).

**M5 — Actual Grok is done on the owner's setup.** Approved local `rehearse` commands work, and Grok Bot calls the tools natively through the remote route ([ADR 007](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/007-grok-bot-remote-https.md)). **M8 — Physical and independent verification is partly done.** The owner's ESP32-S3 + OLED kit passed. It still needs independent reproduction and a real Pi setup. Mobile clients and actual Home Assistant devices need separate evidence.

The public website does not run the gateway or a tunnel. All five repositories have published GitHub releases. The gateway, Linux SDK and Home Assistant packages are on PyPI ([gateway](https://pypi.org/project/grok-gadgets-gateway/), [Linux SDK](https://pypi.org/project/grok-gadgets-linux-sdk/), [Home Assistant](https://pypi.org/project/grok-gadgets-home-assistant/)). Future service deployment and live recognition require their own approval. Firmware binary redistribution needs dependency/license review. These local instructions do not activate an account or device.
