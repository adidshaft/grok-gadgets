# ADR 015 — Shared relay: who runs and pays for relays, and Stage 0 credits

**Date:** 20 October 2026

**Status:** Accepted on 20 October 2026 after the Stage 0 acceptance on the owner's relay ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/credits-2026-10-20.md)). The owner took the five decisions below on the same day.

**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)

**Phase:** 14, "Shared relay decision" ([#270](https://github.com/adidshaft/grok-gadgets/issues/270)). ADR numbers differ from phase numbers.

**Issues:** hub [HUB-ADR-015 #388](https://github.com/adidshaft/grok-gadgets/issues/388), [HUB-CREDITS-001 #389](https://github.com/adidshaft/grok-gadgets/issues/389), [HUB-BIZ-001 #390](https://github.com/adidshaft/grok-gadgets/issues/390); gateway [GW-CREDITS-001 #244](https://github.com/adidshaft/grok-gadgets-gateway/issues/244), [GW-CREDITS-002 #245](https://github.com/adidshaft/grok-gadgets-gateway/issues/245), [GW-CREDITS-003 #246](https://github.com/adidshaft/grok-gadgets-gateway/issues/246), [GW-CREDITS-004 #247](https://github.com/adidshaft/grok-gadgets-gateway/issues/247)

## Context

Today every relay belongs to one person. The owner runs one relay for the owner's kit. A builder runs one relay for the gadgets they ship ([ADR 013](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/013-builder-kit.md)). The project hosts no relay.

People outside the project can now arrive. Phase 13 made the builder guide, the sign-in page and the capacity numbers ready for them ([ADR 014](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/014-ready-for-others.md)). Someone must run each relay and pay for it. Issue #270 asks whether that should be the project.

Facts this decision depends on (gateway `0.1.0a19`):

- **Capacity.** One 512 MB, 1-vCPU host carried 1,000 simulated gadgets with long-poll for 15 minutes. CPU was 67 % and memory 137 MB; p95 command latency was 406 ms. At a 100 ms poll the same host failed near 400 gadgets. No physical fleet was measured.
- **Host cost.** That host class costs US$4 a month; 1 GiB costs US$6 ([DigitalOcean pricing](https://www.digitalocean.com/pricing/droplets), read 14 October 2026). The tunnel costs nothing on the Cloudflare Zero Trust free plan ([ADR 008](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/008-daily-native-route.md)). A domain the operator already owns is assumed.
- **Accounts.** A relay in accounts mode keeps a relay-minted account per person ([ADR 011](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/011-accounts-and-claim-codes.md)). Each account sees only its own gadgets. The operator account is separate.
- **Existing limits.** Each sign-in may make 60 tool calls and 10 commands a minute (`RateLimiter`). Sign-in floods have budgets ([ADR 008](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/008-daily-native-route.md)). Wrong claim codes have limits (ADR 011 §5). `remote off` stops every remote call.
- **The usage hook cannot block a call.** `--usage-hook` puts one line on a bounded queue and drops lines when the queue is full. So a quota cannot live in the hook. It must sit in the call path, in `mcp_server` beside the rate limiter.
- **Grok Bot payments.** We could not read the SpaceXSI terms on payments inside Grok Bot (HTTP 403 on 18 October 2026). Tool results therefore carry no price and no link.
- **Crypto.** A review on 18 October 2026 found no use for tokens, wallets, on-chain records or per-call payments. It suggested one builder-side idea: a quota per account, with no payment code in the project.

## Options

| | A. Project-run relay | B. Operator network | C. Builder-only relays |
| --- | --- | --- | --- |
| Who runs it | The project owner | Independent operators listed by the project | Each builder, for their own gadgets |
| Who pays | The owner, or donations | Each operator | Each builder |
| Host cost | US$4–6 a month per 1,000 long-poll gadgets, plus the owner's time | Same, per operator | Same, per builder |
| Abuse handling | The owner answers every report | Each operator; the project sets a baseline | Each builder |
| Privacy role (GDPR) | The owner becomes the controller for strangers' account IDs, device IDs and request logs | Each operator is the controller; the project lists them | Each builder is the controller |
| Terms | The project needs terms, a privacy notice and an abuse contact | A listing baseline; each operator has their own terms | Each builder's own |
| Single point of failure | Yes | No | No |
| Ready now | No: no entity, no terms, no on-call | No: no outside operator yet | Yes: the guide and kit exist |

**Cost per gadget.** One US$4 host carried 1,000 simulated gadgets. That is about US$0.004 per gadget a month for the host alone. Owner time, abuse handling, backups and legal review cost far more than the host. A project-run relay is therefore a staffing decision, not a hosting one.

**Abuse.** A relay carries short commands to the caller's own gadgets. The main risks are floods, a stolen sign-in and one heavy user starving others. Rate limits, sign-in budgets and `remote off` cover the first two. A per-account balance covers the third. It also gives an operator a plain record of who used what.

**Privacy.** The relay stores account IDs, device IDs, gadget names, request logs and sign-in records. Request logs rotate at 5 MiB and keep 5 files. Whoever runs the relay decides why and how long it keeps them, so they act as the GDPR controller. Under option A that is the owner as a private person. They would then need a privacy notice, a lawful basis, retention rules, a way to answer access requests, and a processing agreement with the host.

## Decision

**C now, B later, A not now.** Builders run their own relays. The project ships the tools to run one fairly: Stage 0 credits. An operator network and a project-run relay each wait for their gate. No stage adds payments to the project.

### Stages and gates

| Stage | What | Gate to start | Counsel checkpoint |
| --- | --- | --- | --- |
| 0 | Credits on a builder's own relay: per-account balance, metering, signed receipts, a report, an admin CLI. No money. | This ADR; the owner's relay as the proof | None needed: no money moves |
| 1 | A builder may charge their own customers outside the project and grant credits to match. The project ships no payment code. | An outside builder asks for it (#269), and the Stage 0 record | Before any project text mentions selling credits: prepaid value and e-money rules, refunds and withdrawal rights, consumer terms |
| 2 | A listing of independent operator relays that meet a baseline: abuse contact, privacy notice, terms, a released gateway | Two outside operators run a released gateway for 30 days | Before the listing: liability for listed operators, GDPR roles; before operators are paid by anyone through the project: money transmission and sanctions screening |
| 3 | A project-run relay | A legal entity, 12 months of hosting funded, an abuse contact with a response time, terms and a privacy notice reviewed by counsel | Before launch: controller duties, processing agreement with the host, terms; any token, securities or crypto-asset rule (for example MiCA) if a token were ever proposed |

Tokens, wallets, chains, x402, pre-sales and a marketplace are out of scope at every stage. A credit or token name never contains "Grok".

### Stage 0 design: Gadget Credits

All of this is off unless the operator opts in. A relay without `--credits` behaves exactly as today.

1. **Opt-in.** `serve --oauth --accounts --credits` and `service install ... --credits`. Credits need accounts mode. Local `stdio` and operator mode are never gated.
2. **Store.** `oauth/credits.json` sits beside `accounts.json` and holds the settings and any per-account allowance. `oauth/credits-ledger.jsonl` is the append-only ledger of grants, debits and refunds. A balance is the sum of its account's entries. One lock guards both. An account without entries has a balance of 0.
3. **Meter.** One credit for each remote `gadgets_command` that the gateway accepts. One credit for each gadget-day: a UTC day in which a gadget owned by the account was online. Weights are relay settings. Reads cost nothing: list, state, events, command status, diagnostics, claim, share, name and remove.
4. **Operator exempt.** The operator account is never debited.
5. **Debit at the gate.** The gate runs in `gadgets_command` after the rate limit and the access check, before the gateway queues the command. It debits first, then runs the command. It refunds in three cases: the gateway refuses the command, the call repeats an earlier command, or the device never received it (`not_delivered`). A gadget-day debit never refuses anything; it may take the balance below zero.
6. **Out of credits.** When the balance is below the command weight, the command does not run. The tool result is `ok: false` with code `out_of_credits` and the text "Your credits on this relay are used up; ask its operator." It never names a price or a link. Gadgets stay online. Local behaviour, reads and the list keep working.
7. **Balance in the list.** With credits on, `gadgets_list_devices` adds the caller's own balance. No account ever sees another account's balance.
8. **Monthly allowance.** On the first metered event of a UTC month, a balance below the allowance is raised to it. A ledger entry records the change. The default allowance is a relay setting.
9. **Receipts.** After each UTC midnight, and on `credits close`, the relay writes one receipt for each account with activity. A receipt holds the account ID, the day, calls, gadget-days, debits, grants, refunds and the closing balance. It also holds a sequence number and the SHA-256 hash of the previous receipt. An Ed25519 receipt key signs it. The key lives in the relay's configuration directory, never in a repository. Each account has its own receipt file.
10. **Verify.** `credits verify` checks every signature, the hash chain and the sequence. A changed, removed, reordered or missing receipt fails.
11. **Reconcile.** Each command debit carries the `request_id` of its `mcp_tool_call` record. `credits report` matches the ledger against those records. Lost usage-hook lines never change a balance, because balances come only from the gate.
12. **CLI.** `credits grant ACCOUNT N`, `credits list`, `credits ledger ACCOUNT`, `credits receipts ACCOUNT`, `credits verify`, `credits report`. Changes are queued for `serve`, as `accounts assign` is. `report` is the operator's view of credits used per account and period, in credits only.
13. **Privacy.** Receipts and reports carry account IDs and counts. They never carry names, tokens, arguments, addresses or codes.

### Threat model

| # | Threat | Control |
| --- | --- | --- |
| C1 | A bug on the call path refuses the owner's own calls | Off by default; operator exempt; stdio and operator-mode tests; `remote off` unchanged |
| C2 | Double spend under concurrent calls | One lock; the debit happens before the action; a concurrency test |
| C3 | Lost debits | Debit first, refund on a known failure; reconciliation against `mcp_tool_call` records |
| C4 | One account learns another's balance | Balance only in the caller's own list result; isolation test |
| C5 | Receipts edited after the fact | Signed, hash-chained receipts; `verify` fails on any change or gap |
| C6 | Receipt key leaks | Key outside the repository, mode 0600; a new key starts a new chain, recorded in the ledger |
| C7 | Credits read as a pre-sale or investment | No price, link, token or "earn" wording in public text; the website says "no payments" |
| C8 | A refused tool result breaks Grok Bot's flow | A normal `ok: false` result with plain text, as `rate_limited` is today |

## Proof

Record `docs/verification/credits-2026-10-DD.md`. Each item says Pass, Fail or Not tested, the tier, and the log lines.

| Item | Tier |
| --- | --- |
| Backup of the live relay's `oauth/` before the change | Owner |
| Relay on the candidate gateway with `--credits` | Owner |
| Grant account B 5 credits; B's commands show text on the kit | Owner |
| B runs out; Grok Bot shows the out-of-credits message (screenshot) | Owner |
| B's list still works at zero | Owner |
| Operator account A unaffected | Owner |
| Top up B; commands work again | Owner |
| Restart keeps balances | Owner |
| Receipts verify; a tampered copy fails | Software, on the relay's files |
| Report matches the request log | Software, on the relay's files |
| Bypass and cross-account tests | Software |

## Results (20 October 2026)

The owner's relay ran the candidate gateway `0.1.0a20` with `--credits`. Account B got 5 credits; five commands showed text on the kit, and the sixth did not run. B's Grok Bot showed the out-of-credits text. B's list still worked, and the operator account was not charged. A top-up and a restart kept the balance. Receipts verified, and a changed copy failed. The report matched the request log. Gadget-days ran in software only, because the kit belongs to the exempt operator. See the [record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/credits-2026-10-20.md).

## Owner decisions

Taken on 20 October 2026. The model is C now and B later. The meter takes one credit per accepted command and one per gadget-day. The default allowance is 0. The business draft stays in the private review folder. The acceptance runs on the owner's relay after a backup.


1. **Relay model.** C now, B later, A not now (recommended). Or A, or B now.
2. **Meter weights.** One credit per accepted command and one per gadget-day (recommended). Or commands only.
3. **Default allowance.** 0 a month, so the operator grants every credit (recommended for the test). Or a number such as 100.
4. **Business draft.** Kept only in the private review folder (recommended). Or in the hub as a draft. It holds no prices for publication either way.
5. **Credits on the live relay.** Turn on `--credits` on the owner's relay for the acceptance, after a backup (recommended). Or test on a fresh host only.

## Not in scope

Real payments, stablecoins, tokens, pre-sales, wallets, x402, a marketplace and a project-run relay. Changes to the ESP32, Linux or Home Assistant code. Replies on #185 or #269, posts and selling wording.
