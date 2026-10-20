# Credits on your relay

Credits give each account on your relay a fair share. Each command and each day a gadget is online uses credits. You grant them. The gateway refuses a command when an account has none left, and tells Grok Bot why.

Credits measure use on your relay. They are not money. The project sells nothing, and the gateway contains no payment code. Credits are off unless you turn them on.

## What you need

- A relay in accounts mode: `serve --oauth --accounts` ([Claim your gadget](claim-your-gadget.md)).
- Gateway `0.1.0a20` or later.
- A backup of the relay's `oauth/` folder and `~/.config/grok-gadgets/`.

## How credits are used

| Action | Credits |
| --- | --- |
| A command that the relay accepts (`gadgets_command`) | 1 |
| Each UTC day that a gadget the account owns is online | 1 |
| List, state, events, command status, diagnostics | 0 |
| Claim, share, name, remove | 0 |
| A command the relay refuses, a repeated command ID, or a command the gadget never received | 0 (refunded) |

The operator account never uses credits. A gadget-day never stops a gadget; it can take a balance below zero. Change the weights with `credits settings`.

## Turn credits on

1. Back up the relay:

   ```sh
   tar czf relay-backup.tgz ~/.config/grok-gadgets
   ```

   Expected result: one archive with `oauth/` and the device credentials. Keep it off the relay.

2. Add `--credits` to the service:

   ```sh
   grok-gadgets-gateway service uninstall
   grok-gadgets-gateway service install --allowed-host gadgets.example.net \
     --oauth --accounts --credits --device-listen 0.0.0.0:8444
   ```

   Use the flags your service already had, plus `--credits`. Expected result: `service status` shows the relay running. The request log has a `credits_opened` line.

3. List the accounts:

   ```sh
   grok-gadgets-gateway credits list
   ```

   Expected result: the operator account says `exempt`; every other account has `balance 0`.

## Grant credits

```sh
grok-gadgets-gateway credits grant acct_EXAMPLE 50
```

The running relay applies the change within a second. A negative number takes credits back. To give every account a monthly amount, set an allowance:

```sh
grok-gadgets-gateway credits allowance 100
grok-gadgets-gateway credits allowance 20 --account acct_EXAMPLE
```

On the first use each UTC month, a balance below the allowance rises to it. The default allowance is 0.

## What a person sees

`gadgets_list_devices` shows the person's own balance, for example `"credits": {"balance": 12}`. No account sees another account's balance.

At zero, a command does not run. Grok Bot gets this text, with no price and no link:

> Your credits on this relay are used up; ask its operator.

The gadget stays online. The list and every read keep working. After you grant credits, the next command works.

## See use, and check it

```sh
grok-gadgets-gateway credits ledger acct_EXAMPLE
grok-gadgets-gateway credits report --since 2026-10-01
```

`report` shows credits granted and spent per account. It also matches every charged command with its request-log record. "Reconciled" means both agree. A rotated-away log shows as commands with no record.

## Receipts

After midnight UTC, the relay writes one receipt per account in `oauth/receipts/`. A receipt holds counts, credits in and out, and the opening and closing balance. Each one carries the hash of the one before it. A key on the relay signs it: `~/.config/grok-gadgets/credits-receipt-key.pem`.

```sh
grok-gadgets-gateway credits close
grok-gadgets-gateway credits verify
```

`close` writes receipts now. `verify` checks each signature, the chain and the ledger. A changed, missing or reordered receipt fails. You can give a person a copy of their receipts and the public key in `oauth/credits-receipt-key.pub`. They check it with `credits verify --receipts FILE --public-key FILE --no-ledger`.

Receipts hold the account ID and counts. They never hold names, tokens, command arguments, addresses or codes.

## Turn credits off

Install the service again without `--credits`. Every command works again. The ledger and receipts stay in `oauth/` for later.

## If you charge for your relay

The project does not handle money. If you charge your customers and grant credits to match, you are the seller. Prepaid credits can fall under rules for stored value, refunds and consumer rights. Ask your own lawyer before you sell them. Never put a price or a payment link in a tool result.

Design and limits: [ADR 015](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/015-shared-relay.md). Gateway reference: [relay host](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/relay-host.md).

[Documentation](../index.md) · [Track usage](track-usage.md)
