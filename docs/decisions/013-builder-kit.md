# ADR 013 — Builder kit: one afternoon from an empty host to shipped gadgets

**Date:** 18 October 2026

**Status:** Proposed. The owner decides the questions in [Owner decisions](#owner-decisions) before code starts.

**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)

**Issues:** hub [HUB-BUILD-001 #269](https://github.com/adidshaft/grok-gadgets/issues/269), [HUB-BUILD-002 #292](https://github.com/adidshaft/grok-gadgets/issues/292); gateway [GW-BUILD-001 #162](https://github.com/adidshaft/grok-gadgets-gateway/issues/162), [GW-BUILD-002 #164](https://github.com/adidshaft/grok-gadgets-gateway/issues/164), [GW-BUILD-003 #165](https://github.com/adidshaft/grok-gadgets-gateway/issues/165), [GW-OAUTH-REFRESH-001 #211](https://github.com/adidshaft/grok-gadgets-gateway/issues/211); ESP32 [ESP-BUILD-001 #118](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/118), [#127](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/127), [#128](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/128), [#129](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/129); Linux [LIN-REMOTE-001 #76](https://github.com/adidshaft/grok-gadgets-linux-sdk/issues/76), [#13](https://github.com/adidshaft/grok-gadgets-linux-sdk/issues/13)

## Context

Phases 9 to 12b built every piece a builder needs. A relay runs on a small Linux host ([ADR 009](009-relay-route.md)). A person joins a gadget to home Wi-Fi with a phone ([ADR 010](010-phone-setup.md)). They claim it with the code on its screen ([ADR 011](011-accounts-and-claim-codes.md)). The builder sends signed updates ([ADR 012](012-signed-updates.md)).

All of it ran on the owner's setup, one piece at a time, with the owner's commands. A new builder today reads six guides and types about forty commands. Some steps exist only in records, for example the tunnel and the firewall.

Phase 12a goal: a builder deploys a relay and ships gadgets in one afternoon, from the docs alone.

Facts this design depends on:

- **Device IDs come from the board.** The ESP32 SDK makes the ID from the chip's MAC address (`oledkit-84c7…`). A builder cannot choose it. A Linux gadget chooses its own ID.
- **Labels hold secrets.** A setup label carries the hotspot passphrase and the setup code ([ADR 010](010-phone-setup.md)). Anyone with the label and the gadget can set it up again after a reset.
- **The request log already holds what a builder needs.** It has `device_hello`, `mcp_tool_call` with device and outcome, `update_*`, and `claim_*` lines. It also holds things a report must not show: command arguments, caller addresses and account IDs.
- **The Linux agent connects to loopback only** (`agent.py`). The relay listener already accepts any TLS client with a token.
- **Cloudflare proxies port 8443.** A proxied device name breaks every CA pin. New relays use port 8444 ([ADR 009](009-relay-route.md)).
- **Grok Bot's access token lasts 1 hour.** On 17 October 2026 the owner's sign-in stopped after that hour. The relay logged no refresh (gateway #211). Every end user meets this. The relay now logs refresh results; the fix follows the owner's watch of one expiry.

## Decision

### 1. `relay init` (gateway #165)

`grok-gadgets-gateway relay init --mcp-host gadgets.example.net --device-host devices.example.net --mode compose|systemd --out DIR` writes the files for a new relay. It writes no secret and runs nothing on a remote host.

| File | For |
| --- | --- |
| `cloud-init.yaml` | A fresh Ubuntu host: a `grokgadgets` user, the firewall (SSH and TCP 8444 only), `uv`, the pinned gateway release, linger, and the service or Docker. |
| `compose.yaml`, `.env` (compose mode) | The gateway and the tunnel containers, as in `examples/docker/`, with the hosts filled in. |
| `grok-gadgets-gateway.service` (systemd mode) | The user service with `--oauth --accounts --device-listen 0.0.0.0:8444`. |
| `cloudflared/config.yml` | The tunnel route `gadgets.example.net` → `http://127.0.0.1:8766`, with a placeholder for the credentials file. |
| `NEXT-STEPS.md` | The commands left for the builder, in order: copy the tunnel credentials, `init`, `device-cert`, start, `relay-check`. |

The tunnel credentials stay out of every generated file, because a cloud provider keeps user data readable to anyone with the account. The builder copies them to the host with `scp`.

**Preflight.** `relay-check` grows from one check to all of them. Each line says Pass or Fail and what to do:

1. `devices.example.net` is DNS only: no proxy address.
2. TCP 8444 is open from outside.
3. The device port answers TLS with the relay's CA (the SHA-256 fingerprint matches `--ca`).
4. The device port refuses plain HTTP.
5. `https://gadgets.example.net/mcp` answers 401, and its protected-resource metadata answers 200.

### 2. Batches (gateway #162)

`grok-gadgets-gateway enroll --batch IDS --out DIR` prepares many gadgets at once.

- `IDS` is a CSV with a `device_id` column. For ESP32 boards, the builder reads each ID from the board. `factory-provision --read-id PORT` prints it. For Linux gadgets, `--count N --prefix lamp-` makes the IDs.
- For each device: a token, written once to `DIR/tokens/ID.token` (mode 0600). The relay keeps only its hash. Tokens never reach the terminal or a log.
- For each device: a label with a passphrase and a setup code. The label store keeps it, and `DIR/labels/` gets a text, QR PNG and printable SVG copy. Plus one `labels.pdf` page for printing all labels at once.
- `DIR/batch.csv`: device ID, hotspot name, label files, `provisioned` (yes or no). No secrets.
- `factory-provision PORT --batch DIR` reads the board's ID, finds its row, sends that token and label, and marks the row after the board confirms. It then deletes the token file.
- The batch directory holds secrets until `factory-provision` has used every row. The guide says so, and tells the builder to keep it off shared drives and chats.

### 3. `builder report` (gateway #164)

`grok-gadgets-gateway builder report [--since DATE] [--json]` reads the request log and `firmware/status.json` on the relay host. It shows, for each gadget:

| Column | From |
| --- | --- |
| Device, name (if the operator account named it) | `device_hello`, accounts |
| Online now, last seen | `device_hello`, `device_disconnected` |
| Calls a day (7 days) | `mcp_tool_call` with `device_id` |
| Errors | `mcp_tool_call` outcomes other than `ok`, by code |
| Firmware version, last update result | `update_*` lines, `firmware/status.json` |
| Claimed | accounts |

It never shows a token, command arguments, reported state, caller addresses, account IDs or codes. It is a CLI, not an HTTP page: a new HTTP route would need its own sign-in and threat review.

### 4. Linux gadgets on a relay (Linux #76)

`grok-linux-agent run app.py --gateway devices.example.net:8444 --ca relay-ca.pem --token-file lamp-01.token` connects with TLS. It pins the relay's CA and checks the name. It uses the same hello, polling, backoff and limits as the ESP32 Wi-Fi link (ADR 005). Loopback stays the default. Protocol 0.1.0 stays the same. Linux #13 adds a simulated background sensor that sends events, as the climate example does.

### 5. Capability vocabulary and template (hub #292)

A short list of names that Grok Bot reads the same way on every gadget. Each has a JSON schema and a description pattern. Builders may use other names; these are the recommended ones.

| Name | Kind | Arguments or data |
| --- | --- | --- |
| `display.text`, `display.clear` | command | `{text: 1–32 printable}`, `{}` |
| `rgb.set` | command | `{r, g, b: 0–255, on}` (canonical) |
| `switch.set` | command | `{on: boolean}`; state `switch.on`; off at boot and on link loss |
| `servo.move` | command | `{angle: 0–180}`; the ACK comes after the move ends |
| `climate` | state | `temperature_c`, `humidity_pct` |
| `threshold.crossed` | event | `{reading, value, above}` |
| `button` | event | `{pressed}` (canonical) |

A project template in each SDK has the relay transport, the update hooks and a host test wired in.

### 6. Examples (ESP32 #127, #128, #129)

| Example | Teaches | Hardware |
| --- | --- | --- |
| Climate sensor | State, events, "tell me when it gets hot" | I2C AHT20, SHT31 or BME280 on the OLED bus |
| Switch | Actuation, safe-off at boot and on link loss, idempotent retries | 3.3 V opto-isolated relay module, **low-voltage loads only** |
| Servo | A command that takes time, `gadgets_command_status`, range checks | SG90 servo |

Each example has a host model that simulates its part, host tests and a CI compile environment. The guide marks each example **Not tested on hardware** until someone runs it with the part. Mains wiring is out of scope, and the switch guide says so first.

### 7. "Ship a gadget" guide (ESP32 #118, hub #269)

One guide, in this order:

1. Template, capabilities, `rehearse`.
2. `relay init`, batch and labels, `factory-provision`.
3. Phone setup, claim.
4. Sign and ship an update, hand-over.
5. [Before you distribute](../getting-started/before-you-distribute.md). Each step links to the guide that has the detail.

### 8. Proof in three tiers

| Tier | Who | Where | Gate |
| --- | --- | --- | --- |
| Clean room | The project's maintainer, from the guide alone | A fresh VM or container, a simulated gadget | Every gap fixed in the docs |
| Dry run | The owner, from the guide alone | A fresh host for a few hours, a batch of 3 | Recorded in `docs/verification/builder-kit-2026-10-DD.md` |
| Outside builder | Someone else | Their own host and parts | Stays open (#269), as #185 does |

Each item in the record names its tier.

## Threat model

| # | Threat | Control |
| --- | --- | --- |
| B1 | Tunnel credentials or tokens in cloud user data | `relay init` writes no secret; credentials go by `scp` |
| B2 | A batch directory leaks | Tokens and labels mode 0600 in a 0700 directory; token files deleted after provisioning; the guide warns |
| B3 | A label reaches the wrong box | Label files are named by device ID; `factory-provision --batch` checks the board's ID first |
| B4 | A proxied device name | `relay-check` fails it; `factory-provision` runs the check |
| B5 | The report leaks personal data | Counts only; no arguments, state, addresses, accounts or codes; CLI on the host only |
| B6 | Linux agent trusts the wrong server | Pinned CA and name check; no system trust store |
| B7 | Relay switch on mains | Low-voltage only; the guide and the example say so before any wiring |
| B8 | Sign-in stops after an hour for every end user | #211: log, watch one expiry, then a fix with the owner's yes |

## Owner decisions

Recommendations first.

1. **Host for the dry run:** a fresh droplet for a few hours, with two DNS names and a second tunnel. We destroy it after (well under US$1 at hourly billing). Or a local VM, which cannot test real DNS or a public port. Recommendation: the droplet.
2. **Gadget for the dry run:** re-provision the kit to the fresh relay and back (two USB sessions; the claim is redone both times). Or use only a Linux agent in a container. Recommendation: the kit plus two Linux agents, to make the batch of 3. Only the kit shows phone setup, the OLED and a signed update.
3. **Example parts:** buy a temperature sensor, a relay module and a servo (about US$10–20). Or ship the examples with host models only, marked Not tested on hardware. Recommendation: host models now. Mark hardware Pass only after the parts arrive.
4. **Report:** a CLI on the relay host, not a web page. Recommendation: yes.

## Not in scope

- Long-poll (gateway #182), the load test (#181), Client ID Metadata Documents (#176), a new sign-in page (#207) and plugin research (hub #336).
- Hardware identity (ESP32 #126) and the Home Assistant bridge (HA #62).
- A shared relay, secure boot, Android, a kit binary as a release asset, and mains switching.
- Words that encourage selling gadgets.
