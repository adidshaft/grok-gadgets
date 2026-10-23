# Credits per gadget-day on the owner's relay — 20 to 23 October 2026

Phase 15 ([#402](https://github.com/adidshaft/grok-gadgets/issues/402), [ADR 016](../decisions/016-pay-for-a-relay.md)). Times are UTC. Each item says Pass, Fail or Not tested, and its tier. This record measures credits only. It has no prices, and no money moved.

Tiers:

- **Owner:** the owner's relay and kit, the relay's own files, and what the owner approved.
- **Software:** tests on the gateway code; no person, phone or gadget.

Accounts on the relay:

- **A:** the operator account. It is exempt from credits.
- **B:** a non-operator account (the Phase 13 Android sign-in), as in the [20 October record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/credits-2026-10-20.md).

## Summary

| Item | Result | Tier |
| --- | --- | --- |
| Backup of the relay before the change | Pass | Owner |
| Kit assigned to B, so gadget-days meter for a non-operator owner | Pass | Owner |
| Grant and monthly allowance for B | Pass | Owner |
| Gadget-days on the live relay, one per UTC day the kit was online | Pass (4 of 4 days) | Owner |
| A gadget-day never stops the gadget | Pass (no refusal; the balance only fell) | Owner |
| Receipts verify after the change | Pass | Owner (relay files) |
| Report matches the request log | Pass (no charged commands to match) | Owner (relay files) |
| Credits per gadget-day | **1.0** (gadget-days only) | Owner |
| Credits used by commands in normal daily use | Not tested: the kit received no commands during the run | — |
| B shares the kit back to A | Not tested: not needed, because nobody used the kit | — |
| Seven full days | Not tested: the owner ended the run after three full days and one partial day | — |
| Kit returned to A | Pass | Owner |

## Setup

- **Relay:** the owner's relay, named `devices.example.net` here, on gateway `0.1.0a20` with `--credits`. The same relay as the 20 October record.
- **Kit:** the ESP32-S3/OLED kit on `0.2.0-alpha.19`.
- **Meter:** 1 credit per accepted command and 1 per gadget-day, the ADR 015 defaults.

## Steps and log lines

Device IDs are shortened to `kit`; account IDs to their first four characters.

1. **Backup, 20 October.** The owner approved the change. An archive of the relay's configuration was copied off the relay; its SHA-256 matched on both sides. It is kept privately.
2. **Assign, grant and allowance, 20 October 14:40–14:42.** The owner approved each change.

   ```text
   B ledger  11  2026-10-20T14:41:00  grant        +60  balance  61  operator
   credits list  acct_3pd3…  balance 61  allowance 60
   accounts list acct_3pd3…  -  1 gadget
   ```

3. **Gadget-days.** The relay charged B once for each UTC day the kit was online:

   ```text
   12  2026-10-20T14:41:51  gadget_day  -1  balance  60  kit
   13  2026-10-21T00:00:27  gadget_day  -1  balance  59  kit
   14  2026-10-22T00:00:09  gadget_day  -1  balance  58  kit
   15  2026-10-23T00:00:01  gadget_day  -1  balance  57  kit
   ```

   Daily reports are on [#402](https://github.com/adidshaft/grok-gadgets/issues/402).
4. **Commands.** The request log shows 0 `gadgets_command` calls to the kit after 20 October 14:40 from any caller. The 8 commands earlier on 20 October belong to the 20 October acceptance.
5. **Report and receipts, 23 October 07:15.**

   ```text
   acct_3pd3…  spent 4 (commands 0, gadget-days 4, refunds 0)  granted 60  balance 57
   Reconciled: 0 charged commands match the request log.
   OK    acct_3pd3…: 4 receipts, closing 58
   ```

   The receipts close at 58 because the 23 October gadget-day is not yet in a daily receipt.
6. **Kit returned, 23 October 07:15:35.** The owner approved it. `accounts list` shows A with 1 gadget and B with 0 gadgets.

## Result

On this relay one gadget, online all day, uses **1 credit per gadget-day**, with the default weights. In this run nobody sent a command, so the number has no command part. It is the floor of what a gadget owner uses, not a typical day.

What a typical day costs in credits stays open. A future run needs a person who uses the gadget each day. The [20 October record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/credits-2026-10-20.md) showed that commands meter at 1 credit each.

## Not tested

- Commands in normal daily use, for the reason above.
- A full seven days. The owner ended the run on 23 October.
- A month boundary. B's allowance of 60 first applies on 1 November.
- A second gadget, a second relay or another person's use pattern.

## State after the run

The kit belongs to A again. B keeps a balance of 57 and an allowance of 60. Nothing else on the relay changed.
