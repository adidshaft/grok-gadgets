# Relay backup and restore on the owner's relay — 24 October 2026

Phase 16 ([#418](https://github.com/adidshaft/grok-gadgets/issues/418)). Times are UTC. Each item says Pass, Fail or Not tested, and its tier. The owner approved each change on the relay host. No money moved.

Tiers:

- **Software:** tests on the gateway code; no person, phone or gadget.
- **Owner (relay files):** the owner's relay host, its files and logs, and a copy on the owner's Mac.

## Summary

| Item | Result | Tier |
| --- | --- | --- |
| `backup` tests: modes, members, restore round trip, checksum mismatch, pruning, refusals | Pass (gateway `0.1.0a21`, 603 tests on Python 3.11 to 3.14) | Software |
| Restore of a synthetic relay with accounts, credits and a signed update | Pass: three commands and the file tree matched | Software |
| Copy of the config directory before the change, SHA-256 checked on both sides | Pass (08:05) | Owner (relay files) |
| Relay upgraded from `0.1.0a20` to `0.1.0a21` from PyPI; service restarted with the same flags | Pass (08:07:39) | Owner (relay files) |
| Kit back online after the restart | Pass: `device_hello` in the request log within seconds | Owner (relay files) |
| Receipts still verify after the upgrade | Pass | Owner (relay files) |
| Route from outside: metadata 200, unauthenticated MCP 401 | Pass | Owner (relay files) |
| Nightly systemd user timer installed; first run through systemd | Pass: 37 files, mode 0600, folder 0700; next run 03:30; linger on | Owner (relay files) |
| Off-host pull to the Mac, SHA-256 checked there | Pass (`shasum -c` OK) | Owner (relay files) |
| Restore into an empty `XDG_CONFIG_HOME` on the Mac: `credits verify`, `accounts list`, `firmware list` | Pass: identical to the relay's output at the time of the backup (3 accounts, 2 receipt chains, 7 stored updates) | Owner (relay files) |
| Restored copy started on other loopback ports, no tunnel | Pass: metadata 200, unauthenticated MCP 401; stopped after the check | Owner (relay files) |
| A person saw the kit's screen after the upgrade | Not tested | — |
| A scheduled nightly run | Not tested yet: the first one is due 25 October 03:30 | — |

## Notes

- The restore ran with a separate install of `0.1.0a21`, not the owner's Mac service. The temporary config folder was deleted after the check.
- The archive holds live tokens, sign-ins and the receipt key. It stays owner-only on the relay and on the owner's computer. The OTA builder key is not in it.
- The guide is [Back up and restore](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/relay-host.md#back-up-and-restore) in the gateway's relay host guide.
