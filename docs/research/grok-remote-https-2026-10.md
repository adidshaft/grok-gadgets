# Grok Bot Remote HTTPS MCP servers, phone use and usage (October 2026)

Research for [HARD-GROK-REMOTE-001 (#4)](https://github.com/adidshaft/grok-gadgets/issues/4) and the owner test [#154](https://github.com/adidshaft/grok-gadgets/issues/154). Questions: how does a person add a Remote HTTPS MCP server to Grok Bot, how does it authenticate, can the phone use a server added on the desktop, and how does Grok Bot show or export plan usage?

Sources are official Grok Bot pages only, read on 13 October 2026. No page shows a last-updated date. Quotations are short; read the linked page for context. The [earlier note](grok-local-execution-2026-10.md) covers local execution.

## Short answer

| Question | Answer | Status |
| --- | --- | --- |
| Where do I add a custom Remote HTTPS server? | In the Bot's info pane ("choose a card to add"), or by asking the Bot in chat. Connectors are plugins under **Connect apps**. No page shows the exact fields. | Partly confirmed |
| Header token or OAuth? | Both: "the Bot's own credential, or each person's sign-in if the server uses OAuth". | Confirmed by docs |
| Must the server be public HTTPS? | Not stated for Grok Bot. Bot computers reach the internet from shared egress addresses, so a server on the owner's Mac needs a public name. | **Unconfirmed**; inference |
| Can the phone use a server added on the desktop? | The phone app uses "the same Bots, conversations, routines, connectors". Connectors are account-wide. Custom MCP servers are not named. | Partly confirmed by docs; worked in the owner test |
| Where is plan usage shown? | Desktop: **Weekly usage limit** in Grok Bot Settings. Phone: **Weekly usage**. On-demand: **Settings → Usage & Billing**. | Confirmed by docs |
| How is usage measured? | "agent steps and tokens", not messages (stated for the trial). Nothing per tool call. | Partly confirmed |
| Can usage be exported or read by an API? | No personal export or API is documented. Teams can stream usage metrics to their own OpenTelemetry collector. | Confirmed by docs (team only) |

## 1. Adding a Remote HTTPS server

- The [Team Bots page](https://docs.x.ai/grok-bot/team-bots) lists "Custom MCP server, **Remote HTTPS**". Its credential is "the Bot's own credential, or each person's sign-in if the server uses OAuth". Teammates need "None, or a one-time sign-in".
- The same page says to set a Bot up from its info pane: "Choose a card to add to it or manage what it holds, or ask the Bot in chat."
- It advises: "For a custom server that needs secrets, choose **Remote HTTPS**." A **Command** server "runs on the computer each conversation uses", which is a Grok Bot computer.
- The [computer and apps page](https://docs.x.ai/grok-bot/computer-and-apps) installs connectors from **Connect apps → Add**, then `@` in chat attaches one. "Installed connectors are account-wide."
- The [Teams and Enterprises page](https://docs.x.ai/grok-bot/teams-and-enterprises) says Grok Bot uses the team's connector policy. The MCP allowlist is Enterprise only; a blocked server shows **Disabled by team admin**.

**Unconfirmed:** the exact screen and field names for a custom URL and header on a personal Bot. The owner test records them.

## 2. Authentication: header or OAuth

- A **Bot credential** is documented. We read it as a fixed secret that the Bot sends, such as `Authorization: Bearer <token>`. The gateway's named tokens match this.
- **OAuth** is documented as per-person sign-in; the "OAuth tokens stay on" the connector backend and Bots "use tools without receiving them" ([Teams and Enterprises](https://docs.x.ai/grok-bot/teams-and-enterprises)). The gateway has no OAuth yet ([gateway #71](https://github.com/adidshaft/grok-gadgets-gateway/issues/71), parked).
- The [approvals page](https://docs.x.ai/grok-bot/approvals-security-and-privacy) says secret values entered through the credential prompt are "masked, excluded from the transcript, and not shown to the model". Never paste the token in ordinary chat.

## 3. Network path

- "Hosted computers reach the internet through shared static egress IP addresses by default" ([security page](https://docs.x.ai/grok-bot/security)). The ranges are shared by all customers. An IP allowlist therefore does not identify the owner's Bot; the token does.
- A team network policy can restrict destinations; teams without one allow all.
- No Grok Bot page allows `http://` or a loopback URL. The 12 October test saw Grok Bot decline `http://127.0.0.1` ([result](../verification/grok-local-execution-2026-10-12.md)).

Inference, not documented: Grok Bot connects from its own computers, so the gateway needs a public HTTPS name. The [owner-run tunnel](https://github.com/adidshaft/grok-gadgets-gateway/blob/dev/docs/tunnel.md) gives one.

## 4. Phone

- The [mobile page](https://docs.x.ai/grok-bot/mobile) says the app "connects to the same Bots, conversations, routines, connectors, and shared cloud computer as the desktop app". Phone settings include "Install or review plugins".
- Approvals work on the phone; "the controls are the same on iPhone" ([approvals page](https://docs.x.ai/grok-bot/approvals-security-and-privacy)).
- "Some advanced desktop controls … are not available on mobile." Team Bots are set up on the desktop.

**Unconfirmed:** that a custom Remote HTTPS server added on the desktop works from the phone. It is likely, because connectors are account-wide and tools run on Grok Bot computers, not on the phone. The owner test checks it.

## 5. Usage and credits

- The [overview](https://docs.x.ai/grok-bot) says "Usage resets weekly". It links a plans and billing page hosted by the billing partner. That page says:
  - the desktop shows a **Weekly usage limit** row in Grok Bot Settings, and the phone shows **Weekly usage**;
  - on-demand spending is under **Settings → Usage & Billing → On-demand monthly limit**;
  - trial usage is "measured by agent steps and tokens", and "larger or longer agent jobs use more";
  - a limit "is not a hard stop in the middle of a run".
- The [troubleshooting page](https://docs.x.ai/grok-bot/troubleshooting) points to **Usage & Billing** "when that section is available".
- No page gives a cost per tool call or per MCP call, a personal usage export, or a personal usage API.
- Teams: an admin can stream usage metrics and logs, including recorded Grok Bot actions, to an OpenTelemetry collector the team runs ([Teams and Enterprises](https://docs.x.ai/grok-bot/teams-and-enterprises)). This is the only documented machine-readable usage path. It is a team-admin feature, not tested here.

## 6. Consequence for Grok Gadgets

1. Use **Remote HTTPS** with a **named bearer token** (`grok-bot`). OAuth stays later work (gateway #71).
2. Put an owner-run TLS tunnel in front of `127.0.0.1:8766/mcp` only. Never tunnel device ports. Allow only the tunnel Host.
3. The gateway request log is the evidence that Grok Bot called a tool; the Bot's narrative is not.
4. Grok Bot usage is read by the owner from **Weekly usage** before and after each step. Any credit figure per tool call is an estimate from those readings. Never scrape the account.
5. The team OpenTelemetry export is a possible later source of measured usage; it is tracked as later work, not built now.

## 7. What the owner tests showed (13 October 2026)

Observed on the owner's personal Grok Bot (desktop 0.70.2, iPhone app); details in the [record](../verification/grok-remote-https-2026-10-13.md) and [ADR 007](../decisions/007-grok-bot-remote-https.md):

- No settings screen adds a custom server. Grok Bot adds one when asked in chat, after a confirmation card. Added servers appear under **Connect apps** with source "Added manually".
- Grok Bot would not put a fixed bearer token into a server's setup, even from its masked secure prompt.
- With OAuth, Grok Bot needed only the URL. Its connector backend registered itself, a sign-in page opened in the browser, and the tools appeared after the owner approved.
- A server added on the desktop worked from the iPhone app with no setup there.
- **Weekly usage** showed whole percent only and did not move during 11 messages and 9 tool calls.

## Sources

All read on 13 October 2026; no page shows an update date.

- Grok Bot overview: <https://docs.x.ai/grok-bot> (links the plans and billing page)
- Team Bots: <https://docs.x.ai/grok-bot/team-bots>
- The computer and apps: <https://docs.x.ai/grok-bot/computer-and-apps>
- Mobile: <https://docs.x.ai/grok-bot/mobile>
- Teams and Enterprises: <https://docs.x.ai/grok-bot/teams-and-enterprises>
- Security: <https://docs.x.ai/grok-bot/security>
- Approvals, security and privacy: <https://docs.x.ai/grok-bot/approvals-security-and-privacy>
- Troubleshooting: <https://docs.x.ai/grok-bot/troubleshooting>
- Bots: <https://docs.x.ai/grok-bot/bots> (no MCP content)
