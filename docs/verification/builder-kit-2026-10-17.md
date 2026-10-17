# Builder kit — 17 October 2026

Phase 12a ([#292](https://github.com/adidshaft/grok-gadgets/issues/292), [ADR 013](../decisions/013-builder-kit.md)). A builder deploys a relay and ships gadgets from [Ship a gadget](../getting-started/ship-a-gadget.md) alone. Times are UTC. Nobody outside the project has run the guide yet ([#269](https://github.com/adidshaft/grok-gadgets/issues/269)).

Tiers:

- **Simulated host**: containers on the owner's Mac; no tunnel, phone or hardware.
- **Fresh host**: a new droplet, created for the dry run and destroyed after it.
- **Hardware**: the owner's ESP32-S3 OLED kit and what the owner saw.

## Clean-room run (tier: simulated host, 17 October 2026 UTC)

The run followed [Ship a gadget](../getting-started/ship-a-gadget.md) and the files that
`relay init` wrote. Two containers stood in for the builder's computer and a fresh Ubuntu 24.04
relay host with systemd. They shared a private network, and `devices.example.net` resolved
to the host. There was no tunnel, no phone and no hardware. Candidate wheels: gateway
0.1.0a17.dev2 (dev 10b09ba), Linux SDK 0.1.0a9.dev1 and .dev2.

| Item | Result | Evidence |
| --- | --- | --- |
| `relay init` writes the three files, no secret | Pass | `Wrote 3 files to my-relay … They hold no secret.` |
| `setup-relay.sh` on a fresh host | Fail, fixed | `ERROR: Could not find a profile matching 'OpenSSH'` (no openssh-server). Gateway #220: `ufw allow 22/tcp`. Rerun: exit 0, `Relay set up for gadgets.example.net and devices.example.net:8444` |
| Relay runs as a user service with linger | Pass | `active`; listeners `127.0.0.1:8766` and `0.0.0.0:8444` |
| `relay-check … --mcp` | Pass | `Relay check passed: all 5 items.` (MCP checked on the host over loopback: no tunnel) |
| Signing key | Pass | `firmware keygen`: `Key ID: 8b9ee4e7c3ecdb13` (clean-room key, destroyed) |
| Linux batch `enroll --count 2 --no-labels` | Pass | `Enrolled 2 gadgets in batch-2` (`lamp-01`, `lamp-02`, mode 0600 tokens) |
| Linux agents with the batch tokens | Fail, fixed | `Agent stopped (unauthorized)`: the factory ID was `linux-lamp-1`. Linux #95: `--device-id`. Rerun: `Agent starting as lamp-01`, `Agent starting as lamp-02` |
| Grok Bot-style sign-in (OAuth, PKCE, `oauth approve`) | Pass (scripted client) | `gadgets_list_devices` → `[]` before assign |
| Linux gadget ownership | Gap, documented | No claim code on Linux. `accounts assign lamp-01 acct_…` → `device_claimed … via operator`; hub #354 adds the step |
| Tool calls over the relay | Pass (simulated) | `rgb.set` executed on lamp-01; `threshold.set` executed; `climate` state `temperature_c 18.1` on lamp-02 |
| `builder report` | Pass | both `online`, `claimed: yes`, calls 1 and 3 |
| `rehearse --accounts`, `rehearse --update` | Pass (simulated) | `Account rehearsal passed`; `Update rehearsal passed with a simulated gadget` |
| ESP32 build, flash, `factory-provision --batch`, phone setup, claim code, signed update on a board | Not tested | No hardware in the clean room; covered by the owner's dry run |
| Grok Bot text | Not tested | Owner's dry run |

Smaller notes: `service install` told the relay user to enable linger after the script had
done so (fixed in #220). The report's `last seen` is the connection time, not the last poll.

## Owner dry run on a fresh host (tiers: fresh host and hardware, 17 October 2026 UTC)

The owner approved each step in the session. A new 512 MB Ubuntu 24.04 droplet ran the relay from `relay init` files. They named two test
names under the owner's domain: `gadgets-dry` for Grok Bot, through a tunnel, and `devices-dry`
for gadgets, DNS-only. This record writes them as
`gadgets.example.net` and `devices.example.net`. Gateway candidate `0.1.0a17.dev3` (dev
`2eb629c`), Linux SDK candidate `0.1.0a9.dev3` (dev `8e13282`). Neither is a release. The
builder's computer was the owner's Mac. The kit is the owner's ESP32-S3 OLED kit.

| Item | Result | Evidence |
| --- | --- | --- |
| Host created, `setup-relay.sh` with the candidate | Pass | Exit 0, `Relay set up for … :8444`; firewall `22/tcp`, `8444/tcp` only; service `active`; no linger hint |
| CA copied to the computer as NEXT-STEPS says | Fail, fixed | `scp grokgadgets@HOST:…` → `Connection closed`: only root had SSH keys. Gateway #222 gives the relay user root's keys; then the copy worked |
| DNS-only device name and tunnel for the Grok Bot name | Pass | The tunnel and the record were added from the session. See the incident below |
| `relay-check … --mcp` | Fail, fixed | `metadata 403, POST 403`: the tunnel's edge refuses Python's default user agent. Gateway #222 names the check; then `Relay check passed: all 5 items.` |
| Batch: kit (`enroll --batch`, label) and 2 Linux gadgets (`enroll --count 2 --no-labels`) | Pass | `Enrolled 1 gadget in batch-1 … setup labels in labels/`; `Enrolled 2 gadgets in batch-2` |
| Linux gadgets from the batch | Pass (simulated devices) | `Agent starting as lamp-01`, `… lamp-02`; both `online` in `builder report` |
| Kit `factory-provision --batch` | Fail, fixed | `… does not match the token enrolled for oledkit-…`: the Mac's own gateway held an older enrollment. Gateway #222: a batch's token wins. Then exit 0, `provisioned: yes`. A board provisioned before also needs `--replace`, as the error says |
| Phone setup with the label | Pass (owner) | BOOT reset: console `setup: open` 20:53:43Z; `setup: online`, `wifi: connected` 20:54:58Z. A re-provisioned board keeps its Wi-Fi until a BOOT reset |
| Claim with the code on the screen | Pass (owner) | 21:03:50Z `account_created`, `device_claimed … via sign_in`, `oauth_token_issued` |
| Grok Bot text | Pass (owner) | 21:04:34Z `display.text` `executed`, `outcome ok`; the owner reported that it all worked |
| Signed update over the relay | Pass | `0.2.0-alpha.17.9`, signed with the owner's key: `update_offered` 21:04:46Z, `update_verified` 21:05:44Z, `update_applied` 21:05:47Z |
| `builder report` shows it | Pass | `oledkit-…  online … claimed: yes; firmware: 0.2.0-alpha.17.9  last update: 0.2.0-alpha.17.9 applied  calls: 1` |
| Host destroyed | Pass | Droplet destroyed, both test DNS records and the test tunnel deleted; only the main relay droplet remains |
| Kit back on the main relay | Pass | Token rotated on the main relay, `factory-provision --replace` exit 0; the main relay then sent its assigned `0.2.0-alpha.17.8` (`update_applied` 21:07:56Z); `accounts list`: operator `1 gadget` |
| Climate sensor, switch and servo examples | Not tested on hardware | Compiled in CI; host models and host tests pass. No parts yet |

### Incident: the main relay's Grok Bot name, 20:41Z to 20:59Z

The session created the test tunnel with `cloudflared` on the Mac. Its default configuration
named the main tunnel, so the session routed the test name to the main tunnel. The test host then ran
a second connector of the main tunnel that answered 404 for the main name. Grok Bot's token
refresh on the main relay failed in that window. The session removed that connector at about
20:59Z, gave the test host its own tunnel, and checked both names (8 of 8 `200`). Lesson: pass
an empty `--config` and the tunnel ID to `cloudflared` on a computer that already runs a tunnel.
The guide's dashboard route has no such step.

## Gaps found and fixed

| Gap | Where | Fix |
| --- | --- | --- |
| `ufw allow OpenSSH` fails on a minimal image | Clean room | Gateway #220 |
| The linger hint after the script set linger | Clean room | Gateway #220 |
| Batch IDs refused for a Linux gadget | Clean room | Linux #95 (`--device-id`) |
| A Linux gadget has no claim code | Clean room | Hub #354 (`accounts assign`); gateway #221 (Later) |
| The relay user had no SSH key | Fresh host | Gateway #222 |
| The edge refused the preflight's user agent | Fresh host | Gateway #222 |
| The computer's own registry refused a batch token | Fresh host | Gateway #222 |
| A re-provisioned board keeps its Wi-Fi | Fresh host | This guide: BOOT reset before hand-over |

## Not proved

- A builder outside the project: [#269](https://github.com/adidshaft/grok-gadgets/issues/269) stays open.
- The three new examples on hardware.
- A relay made from `cloud-init.yaml` alone: the candidate was not on PyPI, so the script ran
  over SSH with `GATEWAY=` the wheel.
