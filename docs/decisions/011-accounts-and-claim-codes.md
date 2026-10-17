# ADR 011 — Accounts and claim codes: a person claims a gadget and sees only their own

**Date:** 17 October 2026

**Status:** Proposed. The owner took the three decisions on 17 October 2026 (below). Acceptance follows the Phase 11 record.

**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)

**Issues:** hub [HUB-ADR-011 #267](https://github.com/adidshaft/grok-gadgets/issues/267), [HUB-CLAIM-001 #268](https://github.com/adidshaft/grok-gadgets/issues/268); gateway [GW-CLAIM-001 #159](https://github.com/adidshaft/grok-gadgets-gateway/issues/159), [GW-CLAIM-002 #160](https://github.com/adidshaft/grok-gadgets-gateway/issues/160), [GW-CLAIM-003 #161](https://github.com/adidshaft/grok-gadgets-gateway/issues/161), [GW-CLAIM-004 #180](https://github.com/adidshaft/grok-gadgets-gateway/issues/180); ESP32 [ESP-CLAIM-001 #116](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/116)

## Context

[ADR 009](009-relay-route.md) put the gateway on an always-on relay. [ADR 010](010-phone-setup.md) lets a person join a gadget to home Wi-Fi with a phone alone. The relay still has one tenant: the operator.

- Grok Bot signs in with OAuth. The operator approves each sign-in with `oauth approve CODE --name NAME` on the relay host ([ADR 008](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/008-daily-native-route.md)).
- The token's subject is that approved name, for example `grok-bot`. Nothing identifies a person.
- Every live sign-in sees every device. `gadgets_diagnostics`, `gadgets_read_events` and `gadgets_command_status` also return data across all devices.
- `credentials.json` holds device tokens in plain text. `factory-provision --enroll` and `wifi-provision` read them from there.

Phase 11 goal: a person claims a gadget with the code it shows and sees only their own gadgets. Share, unclaim and transfer are explicit actions. The owner's relay, kit and sign-in keep working.

Facts this design depends on:

- With Client ID Metadata Documents, every instance of one connector backend presents the same `client_id` URL ([MCP authorization](https://modelcontextprotocol.io/specification/latest/basic/authorization)). A `client_id` never identifies a person.
- Grok Bot connects a Remote HTTPS server with "the Bot's own credential, or each person's sign-in if the server uses OAuth" ([Team Bots](https://docs.x.ai/grok-bot/team-bots)). The Bot's own credential is shared by everyone who uses that Bot.
- RFC 8628 asks for user codes with enough entropy against guessing and a short life ([RFC 8628 §6.1](https://www.rfc-editor.org/rfc/rfc8628#section-6.1)).
- **Released firmware rejects an unknown field in a gateway reply.** `GrokSession::shaped()` in ESP32 SDK 0.2.0-alpha.15 compares the reply's field count with the expected count. An extra field resets the session. A relay that adds `claim_code` to every hello reply would put every released gadget in a reconnect loop.
- In Phase 7 and Phase 9 the Mac and iPhone apps worked through one approved sign-in. Whether one person's two apps ever create two sign-ins is not known.

## Decision

### 1. Two modes

- **Operator mode** (today, the default): one tenant. Nothing in this ADR changes it. USB, loopback, LAN and stdio routes stay as they are.
- **Accounts mode**: `serve --oauth --accounts`. Accounts mode needs OAuth. The rest of this ADR describes accounts mode.

### 2. Account identity

- An **account** is a relay-minted ID: `acct_` followed by 26 base32 characters (128 random bits).
- The relay creates an account only when a sign-in is approved with a valid **claim code** or **share code** (section 4). A sign-in never joins an existing account through a code from a gadget.
- The account ID is stored in each access and refresh record of that sign-in. A refresh copies it to the new pair. The **refresh-token family** carries the account. The `client_id` never does.
- The operator's own CLI approval stays: `oauth approve CODE --name NAME` signs in to the **operator account** (section 9).
- **The Bot's shared credential is refused.** In accounts mode the `mcp-token` file and named MCP tokens get 401 `shared_credential_refused` on `/mcp`. Only an OAuth sign-in with an account can call tools. Local `stdio` keeps the operator's full view.

### 3. Claim code

- **Format:** 8 characters from the existing 32-character alphabet (no 0, O, 1 or I), shown as `XXXX-XXXX`. 40 bits.
- **Issue:** the relay makes a code when an unclaimed gadget completes its hello, if the gadget asked for claim fields (below). One live code per gadget.
- **Life:** 10 minutes, and only while that gadget's session is live. A disconnect ends the code. A used code ends at once.
- **Fresh code:** when a code expires and the session is still live, the relay makes a new one. It sends the new code in the next poll reply. The display shows it within one poll interval (500 ms on the relay).
- **Opt-in, for compatibility:** a gadget that can show a code sends `"claim": "ready"` in its hello. Only then does the hello reply carry `claimed` (true or false) and, while unclaimed, `claim_code`. A poll reply carries the same two fields only when one of them changed. A gadget without the field gets the replies it gets today.
- **Old relay:** a relay before this change answers the new hello field with `invalid_request`. The firmware then sends its hello again without the field and does not ask again until the next boot. It shows no code and works as before.
- **Storage:** codes live in the relay's memory only, as SHA-256 hashes. They never reach a file or a log line.
- **Where a code works:** on the sign-in page (creates an account and claims the gadget) and in `gadgets_claim` (claims it for the signed-in account).

### 4. Sign-in page in accounts mode

1. The person adds the relay URL in Grok Bot, for example `https://gadgets.example.net/mcp`.
2. Grok Bot opens the relay's sign-in page. The page asks for the code on the gadget or a share code.
3. A valid claim code: the relay creates an account, claims that gadget for it and finishes the sign-in.
4. A valid share code: the relay creates an account with that share and finishes the sign-in.
5. A valid link code (section 6): the relay finishes the sign-in into that link code's account.
6. A wrong or expired code: the page says "That code did not work" and nothing else. It never says whether a gadget, an account or a code exists.

The operator's code path (`oauth approve`) stays. The page shows the operator code under the form as today.

### 5. Attempt limits

| Where | Limit | When it is hit |
| --- | --- | --- |
| One sign-in request | 5 wrong codes | The request ends; Grok Bot must start a new sign-in |
| One caller address, sign-in page | 20 wrong codes an hour | 429 for the rest of the hour |
| One account, `gadgets_claim` | 10 wrong codes an hour | `rate_limited` |
| The whole relay | 200 wrong codes an hour | Code entry closes for 10 minutes; one `claim_flood` line a minute |

With 100 gadgets waiting for a claim, 200 guesses an hour find a code with a chance of about 2 in 100 million per hour. The existing OAuth limits of ADR 008 (T1–T4) still apply.

### 6. Share, link and re-sign-in

- **Share code:** the owner calls `gadgets_share(device_id, action="create", scope)`. The relay returns an 8-character code with a 10-minute life, for one use. `scope` is `use` (list, state, events, commands) or `view` (list, state, events). The owner gives the code to the other person in person or by message.
- The other person calls `gadgets_claim(code)` from their own sign-in, or uses the code on the sign-in page. They get a **grant** on that gadget. Accounts never merge.
- The owner lists grants with `action="list"` and ends one with `action="revoke"`. A revoke takes effect at the next tool call. The grantee ends their own grant with `gadgets_remove`.
- **Link code:** `gadgets_share(action="link")` makes a 10-minute code for the caller's own account. It is for a second app or a new phone that needs its own sign-in. It never comes from a gadget.
- **Re-sign-in after the refresh token expires** (30 days without use): there is no live session to make a link code. The person uses the recovery code (decision 3) or asks the relay operator (`accounts link ACCOUNT`).
- A fresh claim code at a new sign-in always makes a new account. It never reaches the old one.

### 7. Unclaim and transfer

- **Unclaim:** the owner calls `gadgets_remove(device_id)`. The gadget has no owner and no grants. If it is connected, it shows a new claim code.
- **Transfer after a BOOT reset:** the gadget still belongs to the old owner on the relay. A local reset never changes ownership.
  1. After a BOOT reset and a phone re-join, the firmware sends `"claim": "after_setup"` in its first hello.
  2. For a claimed gadget, `after_setup` makes the relay issue a **transfer code** with the same format and limits, for 10 minutes. The gadget shows it.
  3. The new person enters it (sign-in page or `gadgets_claim`). The transfer is **pending**. The old owner keeps full use. The new person sees the gadget as `pending_transfer` only.
  4. The transfer completes when the old owner calls `gadgets_remove`, or when the grace period ends (decision 1). The old owner sees `pending_transfer` with its end time and can refuse it with `gadgets_share(action="refuse_transfer")`.
- A code replay, a reset alone or a new sign-in never moves a claimed gadget.

### 8. Tools in accounts mode

Every tool checks the caller's account. A device outside the account answers `unknown_device`, the same answer as for a device that does not exist.

| Tool | Scope |
| --- | --- |
| `gadgets_list_devices` | Owned gadgets and grants, with `role` (`owner`, `use`, `view`) and `pending_transfer` |
| `gadgets_get_state` | Owner, `use`, `view` |
| `gadgets_command` | Owner, `use` |
| `gadgets_command_status` | Commands sent by this account only |
| `gadgets_read_events` | Events of gadgets the account can see; cursors stay per relay |
| `gadgets_diagnostics` | Counts and devices of this account only |
| `gadgets_claim` (new) | Claim, share or transfer code |
| `gadgets_remove` (new) | Owner: unclaim. Grantee: drop the grant |
| `gadgets_share` (new) | Owner: `create`, `list`, `revoke`, `refuse_transfer`; anyone: `link` |

Each of the six existing tools gets a cross-account regression test.

### 9. Storage, logs and operator CLI

- `oauth/accounts.json`, written by `serve` only, mode 0600: accounts (ID, created, recovery-code hash), devices (owner, claimed at, grants, pending transfer). No tokens, no codes.
- `credentials.json` holds device tokens as SHA-256 hashes (GW-CLAIM-003). The gateway checks a hash in constant time.
- **Provisioning with hashed tokens:** `enroll` prints the token once or writes it to `--token-file`. `factory-provision` and `wifi-provision` take `--token-file`. With a local registry they can also issue a new token with `--rotate`; the registry stores its hash only after the board confirms the write. A board that fails keeps its old, still valid token.
- Audit lines, never with a token or a code: `account_created`, `device_claimed`, `device_unclaimed`, `share_created`, `share_used`, `share_revoked`, `transfer_pending`, `transfer_done`, `transfer_refused`, `claim_rejected` (with reason and caller address), `claim_flood`.
- Operator CLI, through command files that `serve` reads, as `oauth approve` does today: `accounts list`, `accounts show ID`, `accounts unclaim DEVICE`, `accounts assign DEVICE ACCOUNT`, `accounts link ACCOUNT`, `accounts revoke ACCOUNT`.
- The operator can still read and change everything on the host. Hashes limit what a stolen backup reveals. They do not protect against a compromised running relay. The privacy note of ADR 009 §5 applies to every account.

### 10. Gadgets without a display (design only)

No firmware in Phase 11. Two candidate paths for a later review:

- The setup captive page of ADR 010 shows the claim code after the gadget goes Online. The phone is on that page already.
- A factory claim code printed on the label, stored as a hash on the relay, valid only while the gadget is unclaimed, for one use, and replaced by `factory-provision --new-label`.

### 11. Migration of an existing relay

On the first start in accounts mode, when `accounts.json` does not exist:

1. The relay creates the operator account.
2. Every enrolled device becomes owned by the operator account.
3. Every live sign-in, under any approved name such as `grok-bot`, joins the operator account.
4. Plain device tokens in `credentials.json` become hashes. The old file is kept as `credentials.json.pre-hash` (mode 0600) until the operator deletes it.

The owner's sign-in and the kit keep working with no new sign-in and no reflash. Rollback: stop the relay, restore the backup of the config directory, start the previous release.

## Threat model

| # | Threat | Control |
| --- | --- | --- |
| C1 | Guessing a claim, share, transfer or link code | 40 bits; 10-minute life; one use; live session needed for claim codes; limits in §5; one answer for every failure |
| C2 | A stranger near the gadget reads its code | The code makes a claim only while the gadget is unclaimed. On a claimed gadget it makes a pending transfer that the owner can refuse. |
| C3 | A reset gadget is taken over | A reset never changes ownership; transfer needs the owner's unclaim or the grace period; the owner sees it pending |
| C4 | A code opens an existing account | A claim, share or transfer code always creates a new account or adds a gadget; only a link code from a live session or the operator reaches an account |
| C5 | Two people behind one shared credential | Static bearer tokens are refused in accounts mode |
| C6 | Cross-account read through a side tool | All six tools scoped; command status per account; diagnostics per account; a regression test per tool |
| C7 | Event stream leaks across accounts | Events filtered by visible gadgets; the shared cursor carries only a relay sequence number |
| C8 | A share outlives its purpose | Revocable by the owner, droppable by the grantee, removed by unclaim and transfer |
| C9 | Stolen relay backup | Device tokens, OAuth tokens and recovery codes are hashes; codes are never on disk |
| C10 | Compromised relay or operator | Not prevented. Documented; the operator's view is stated in the privacy note |
| C11 | Flood of sign-ins or codes | ADR 008 T1–T4, §5 limits, `claim_flood` alert |
| C12 | Released firmware breaks on new reply fields | Fields only after the gadget's opt-in; old relays fall back cleanly |
| C13 | The same `client_id` for many people | The account follows the refresh-token family, never the `client_id` |
| C14 | Lost account after 30 days without use | Recovery code or the operator; never a gadget code |

## Owner decisions (taken 17 October 2026)

The owner chose: a **7-day grace period**; the operator account sees **only its own gadgets**; a **recovery code** with the operator as the fallback.

1. **Grace period for a pending transfer:** none (only the old owner's unclaim completes it), 7 days, or 30 days. Recommendation: 7 days. A sold or lost gadget then moves even if the old owner never answers, and the old owner can refuse within a week.
2. **Does the operator account see every gadget?** Recommendation: no. The operator account sees its own gadgets. The operator uses the CLI for the others. A leaked operator sign-in then reaches only the operator's gadgets.
3. **Account recovery:** a recovery code shown once at account creation, or the operator only. Recommendation: the recovery code (16 characters, 80 bits, stored as a hash, replaced after each use), with the operator as the fallback.

Share-code policy as proposed: 10 minutes, one use, `use` or `view`, revocable, no re-share by a grantee.

## Acceptance (Phase 11)

Gateway tests for every item above, with two accounts in `rehearse`. Then, on the owner's relay and kit, with a second person's Grok Bot on their own phone:

- A unclaims the kit. B adds the relay, signs in with the code, claims it and shows text.
- A cannot list it, read it, command it or see its events.
- B shares it to A; A uses it; B revokes the share.
- Wrong and expired codes fail; a flood is limited and logged.
- B does a BOOT reset and a phone re-join. A claims it: pending until B unclaims. Then A shows text.

The record goes to `docs/verification/claim-2026-10-DD.md` with gateway log lines and the owners' observations.

## Not in scope

Client ID Metadata Documents (gateway #176), the builder kit, OTA, the firmware core migration, a shared relay and the Linux SDK remote transport.
