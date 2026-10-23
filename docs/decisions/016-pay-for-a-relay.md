# ADR 016 — Paying for a builder's relay: Stage 1 boundaries

**Date:** 20 October 2026

**Status:** Proposed. Nothing is sold, and no money moves. This ADR sets the boundaries for ADR 015 Stage 1. Selling stays closed until every gate below is met.

**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)

**Phase:** 15, "Pay for a relay: Stage 1 preparation". ADR numbers differ from phase numbers.

**Issues:** hub [HUB-ADR-016 #401](https://github.com/adidshaft/grok-gadgets/issues/401), [HUB-CREDITS-002 #402](https://github.com/adidshaft/grok-gadgets/issues/402), [HUB-LEGAL-001 #403](https://github.com/adidshaft/grok-gadgets/issues/403); Stage 1 demand: [#269](https://github.com/adidshaft/grok-gadgets/issues/269)

## Context

[ADR 015](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/015-shared-relay.md) chose builder-only relays now and an operator network later. Stage 0 credits run on the owner's relay. In Stage 1 a builder may charge their own customers outside the project and grant credits to match. Stage 1 waits for an outside builder (#269) and for counsel before any project text mentions selling.

ADR 015 also says tokens, wallets, chains, x402, pre-sales and a marketplace are out at every stage. This ADR keeps that rule for customers. It proposes one narrow exception, for a later stage: two businesses, an operator and a builder, may settle between themselves in a stablecoin. Until counsel signs off, that path exists only on a test network, with test tokens that have no value.

Facts this proposal depends on:

- **The gateway already has a payment-neutral hook.** `credits grant ACCOUNT N` queues a change that the running relay applies within a second. Anything outside the gateway that learns of a payment can call it. No payment code needs to enter the gateway.
- **Grok Bot terms.** The SpaceXSI consumer terms and the Grok Bot terms were read on 20 October 2026 (both updated 12 October 2026; [consumer terms](https://x.ai/legal/x-subscription-terms-of-service)). They make the user responsible for Grok Bot's agentic actions and for the terms and charges of connected third-party services. They expect human review before financial transactions. They say nothing about a connected tool charging its users. The [Acceptable Use Policy](https://x.ai/legal/acceptable-use-policy) (effective 14 August 2026) forbids operating in a regulated industry without complying with its rules.
- **The SpaceXSI name and marks.** The [Brand Guidelines](https://x.ai/legal/brand-guidelines) (14 February 2025) cover SpaceXSI's marks, which include "Grok". They ask that no product or service SpaceXSI does not make uses the marks in its name. This project's name contains "Grok". Counsel must review the name before anything is sold under it.
- **Test networks.** Circle publishes test USDC on Solana Devnet and Base Sepolia and states that it has no financial value ([contract addresses](https://developers.circle.com/stablecoins/usdc-contract-addresses)). Its [faucet](https://faucet.circle.com/) needs no account. Solana has a [Memo program](https://www.solana-program.com/docs/memo) that records a short text with a transaction. A plain ERC-20 transfer on Base has no memo field.
- **Costs and liability.** ADR 015's cost basis still holds: hosting is cheap; operator time, abuse handling, the GDPR controller role and legal duties are not.

## Decision (proposed)

1. **Customers pay by card, up front, never with a wallet.** A customer pays the builder who sold the gadget. The builder uses a card processor or a merchant of record of the builder's choosing, outside the project. The builder grants credits only after payment. A customer never connects, creates or funds a wallet. No price, payment link or wallet address appears in a Grok Bot tool result, on a gadget or in the gateway.
2. **The gateway stays payment-free.** The gateway, the SDKs and the Home Assistant integration get no payment code, no wallet code and no chain client. A relay learns about money only through `credits grant`, which an operator or an outside tool runs.
3. **Operator and builder settlement: test network only.** When ADR 015 Stage 2 brings independent operators, an operator and a builder may settle in a stablecoin. Until counsel signs off, this happens only on a test network with test tokens. A transfer carries a one-time reference in its memo. The reference is not the relay account ID; the operator keeps the mapping. A watcher outside the gateway sees the transfer and queues `credits grant` on the operator's relay.
4. **Any top-up adapter is separate and later.** A watcher turns a transfer into credits. If it ever ships, it is a separate optional package, outside the five repositories' runtime code. It ships only after counsel, and never with mainnet support switched on by default.
5. **Amendment to ADR 015.** ADR 015 keeps chains out at every stage. This ADR adds one exception: operator and builder settlement as in point 3, on a test network until counsel signs off. Everything else in that clause stays: no tokens, no customer wallets, no x402, no pre-sales, no marketplace. ADR 015's stages and gates stay the same.
6. **Out at every stage.** A project token, staking, rewards, an exchange, custody of anyone's funds and payouts by the project. No credit, token, coin or settlement product has "Grok" in its name.

### Who pays whom

| From | To | How | When |
| --- | --- | --- | --- |
| Customer | Builder | Card, through the builder's processor or merchant of record | Stage 1, after counsel |
| Builder | Operator | Stablecoin on a test network (test tokens only) | Rehearsal now; real funds only after counsel and Stage 2 |
| Anyone | The project | Nothing | Never through this path |

The project never receives, holds or forwards a customer's or an operator's money.

### Gates before anything is sold

| Gate | Evidence |
| --- | --- |
| An outside builder asks for Stage 1 | A request on #269 or a linked issue |
| Counsel signs off for the jurisdictions involved | A written opinion held privately by the owner; this ADR records only the date and scope |
| The Grok Bot terms are read and still allow it | Done 20 October 2026; read again within 30 days of any launch |
| The project name is reviewed against the SpaceXSI Brand Guidelines | Counsel's answer, before any selling text |
| Stage 0 has a real number | The 7-day record with live gadget-days (#402) |

Counsel's questions cover these topics:

- Prepaid value and e-money rules once credits are sold.
- Refunds, withdrawal rights, consumer terms and tax on prepaid sales.
- Crypto-asset rules for a stablecoin, for example MiCA in the EU.
- Money transmission and sanctions screening.
- The GDPR controller role.
- App-store rules on unlocking features with cryptocurrency.

### Threat model

| # | Threat | Control |
| --- | --- | --- |
| P1 | Text reads as a payment, pre-sale or token offer | Status Proposed; no prices; the website keeps "no payments"; owner's yes before merge |
| P2 | A customer is pushed towards a wallet | Customers pay by card only; no wallet address in any tool result, gadget or guide |
| P3 | Payment code enters the gateway | Credits change only through `credits grant`; any adapter lives in a separate package |
| P4 | Real funds move before counsel | Test network only; a mainnet setting off by default in any future adapter |
| P5 | A memo links a relay account to a public ledger | One-time references; the operator keeps the mapping off chain |
| P6 | A forged or replayed transfer grants credits | The watcher checks the token mint, the receiving address, the amount and a reference used once |
| P7 | The project becomes a payment intermediary | The project never receives or forwards money; operators and builders contract directly |

## Proof

| Item | Tier | Where |
| --- | --- | --- |
| Credits per gadget-day measured live with a non-operator owner | Owner | [Record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/credits-pricing-2026-10-23.md): 1.0 per gadget-day across four metered UTC dates; ended early, no commands. [Seven-day rerun in progress](../public/support-matrix.md#phase-15-preparation-only); no results yet (#402) |
| A test-network transfer with a memo raises a balance on a local relay | Owner, on a test network | Done on 23 October 2026 on Solana Devnet with test tokens; a reused reference was refused. Results are private, not in any repository |
| Counsel pack prepared | Owner | Private; not in any repository (#403) |

## Owner decisions

Taken on 20 October 2026. The ADR stays Proposed until the gates are met.

1. **ADR 015's chain clause** gains one exception: operator and builder settlement, on a test network until counsel signs off.
2. **Test network:** Solana Devnet, with Circle's test USDC and the Memo program.
3. **Adapter:** none now. If one ever ships, it is a separate optional package, after counsel.
4. **Names:** plain words only: "credits" and "operator settlement". No new product names now. No name contains "Grok".

Options not chosen: no chains at all, Base Sepolia, never an adapter, and a product name now.

## Not in scope

Mainnet, real funds, custody, exchanges, tokens, pre-sales, payouts, staking and an operator listing. Payment code in the gateway or SDKs, and prices. Changes to the ESP32, Linux or Home Assistant code.
