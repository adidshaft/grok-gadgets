# Credits per gadget-day, second run — 23 to 24 October 2026

Phase 15 ([#402](https://github.com/adidshaft/grok-gadgets/issues/402), [ADR 016](../decisions/016-pay-for-a-relay.md)), finished in Phase 16 ([#422](https://github.com/adidshaft/grok-gadgets/issues/422)). Times are UTC. Each item says Pass, Fail or Not tested, and its tier. This record measures credits only. It has no prices, and no money moved.

The second run was planned to 30 October so that commands from B's Grok Bot would meter too. The kit got no commands, so the owner ended it on 24 October. The [first run](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/credits-pricing-2026-10-23.md) (20 to 23 October) is a separate record.

Tiers:

- **Owner:** the owner's relay and kit, the relay's own files, and what the owner approved.

Accounts on the relay:

- **A:** the operator account. It is exempt from credits.
- **B:** a non-operator account, as in the first run.

## Summary

| Item | Result | Tier |
| --- | --- | --- |
| Backup of the relay before the run and before the kit's return | Pass | Owner |
| Kit assigned to B for the run | Pass (23 October 10:14:55) | Owner |
| Gadget-days charged to B, one per UTC day | Pass (24 October; the 23 October day was charged before the run) | Owner |
| Relay upgrade to `0.1.0a21` and a host reboot during the run | Pass: the kit came back, and metering went on with no double charge | Owner |
| Receipts verify; the report matches the request log | Pass | Owner (relay files) |
| Credits per gadget-day | **1.0** (gadget-days only) | Owner |
| Commands from B's Grok Bot in daily use | Not tested: 0 commands from any caller during the run | — |
| Seven days | Not tested: the owner ended the run after one full day | — |
| Kit returned to A | Pass (24 October 14:56) | Owner |

## Steps and log lines

Device IDs are shortened to `kit`; account IDs to their first four characters.

1. **Start, 23 October 10:14:55.** A backup was taken first; its SHA-256 matched on both sides. The kit was assigned to B with the owner's yes.
2. **Gadget-day.**

   ```text
   16  2026-10-24T00:00:49  gadget_day  -1  balance  56  kit
   ```

3. **Upgrade and reboot, 24 October.** The relay moved to gateway `0.1.0a21` at 08:07 and the host rebooted at 08:22 ([relay backup record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/relay-backup-2026-10-24.md)). The kit reconnected each time. No second gadget-day was charged for 24 October.
4. **Commands.** The request log shows 0 `gadgets_command` calls after 23 October 10:14:55 from any caller.
5. **Report and receipts, 24 October 14:56.**

   ```text
   acct_3pd3…  spent 1 (commands 0, gadget-days 1, refunds 0)  granted 0  balance 56
   Reconciled: 0 charged commands match the request log.
   OK    acct_3pd3…: 5 receipts, closing 57
   ```

   The receipts close at 57 because the 24 October gadget-day is not yet in a daily receipt.
6. **Kit returned, 24 October 14:56:50.** The owner approved it after a fresh backup. `accounts list` shows A with 1 gadget and B with 0 gadgets.

## Result

Both runs give the same number: one gadget online all day uses **1 credit per gadget-day** with the default weights. Neither run had a command, so the number is the floor of what a gadget owner uses, not a typical day. The [20 October record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/credits-2026-10-20.md) showed that commands meter at 1 credit each. What a typical day costs stays open until a person uses a gadget daily on a relay with credits.

## Not tested

- Commands in normal daily use.
- Seven full days, and a month boundary (B's allowance first applies on 1 November).
- A second gadget, a second relay or another person's use pattern.

## State after the run

The kit belongs to A again. B keeps a balance of 56 and an allowance of 60. Nothing else on the relay changed.
