# Builder kit — 17 and 18 October 2026

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

## Owner dry run on a fresh host (tier: fresh host and hardware)

Pending the owner's approval.
