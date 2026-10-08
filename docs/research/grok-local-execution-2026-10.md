# Grok Bot Execution on Local Computer: what it allows (October 2026)

Research for [LAUNCH-GROK-001 (#31)](https://github.com/adidshaft/grok-gadgets/issues/31) and [HARD-GROK-REMOTE-001 (#4)](https://github.com/adidshaft/grok-gadgets/issues/4). Question: can the owner's existing Grok Bot reach a gateway on the owner's Mac through **Execution on Local Computer**? If not, we need a remote HTTPS route.

Sources are official SpaceXAI Grok Bot pages only, read on 8 October 2026. None of the pages shows a last-updated date. Quotations are short; read the linked page for context. Third-party guides and forum posts were seen during the search but are not used as evidence.

## Short answer

| Question | Answer | Status |
| --- | --- | --- |
| Can Grok Bot run shell commands on my own computer? | Yes, through the desktop app, after you enable the setting and approve the command. | Confirmed by docs |
| Can it read files and move files between its cloud computer and my computer? | Yes. | Confirmed by docs |
| Can it connect to a local MCP server (stdio on the Mac, or a `127.0.0.1` URL with a bearer header)? | The docs do not say so. They describe two MCP server types, **Remote HTTPS** and **Command**, and place Bot work on a Grok Bot computer. | **Unconfirmed** |
| Which plans have local execution? | No plan limit is stated for the setting itself. Team admins can cap it. | Partly confirmed |
| Which platforms? | The desktop app (macOS, Windows, Linux). Mobile behaviour is not stated. | Partly confirmed |
| What approvals does it show? | A card with the exact command; Allow once, Always allow, Deny. | Confirmed by docs |
| Which logs exist? | Audit logs and Action Recording are team and Enterprise features. No personal local-command log is documented. | Partly confirmed |

The documented route is therefore outcome **(b)**: Grok Bot runs an approved command on the Mac, and that command talks to the gateway on `127.0.0.1`. A direct MCP connection, outcome **(a)**, is not documented. Only an owner test with the gateway request log can settle it. See the [owner checklist](../grok-local-test.md).

## 1. What Execution on Local Computer allows

- The [security page](https://docs.x.ai/grok-bot/security) says Bots "can act on a member's own machine through the desktop app: run commands, read files". The same page says they can move files between the cloud computer and the local machine.
- The [computer and apps guide](https://docs.x.ai/grok-bot/computer-and-apps) says a Bot "only runs commands on your local computer when that capability is enabled and you approve it."
- The [troubleshooting page](https://docs.x.ai/grok-bot/troubleshooting) says cloud-computer work and local-computer work "use different permissions".
- The [approvals page](https://docs.x.ai/grok-bot/approvals-security-and-privacy) says the local settings "do not prevent the Bot from using its cloud computer."

Inference, not documented: a command that runs on the Mac uses the Mac's network. A command such as `grok-gadgets-gateway rehearse` can therefore reach a gateway that listens on the Mac's `127.0.0.1`. The [hosting guide](../getting-started/hosting.md) already describes this boundary.

## 2. MCP servers

- The [Team Bots page](https://docs.x.ai/grok-bot/team-bots) names two MCP server types. **Remote HTTPS** uses "the Bot's own credential, or each person's sign-in if the server uses OAuth". **Command** "runs on the computer each conversation uses".
- The same page says "a Team Bot works on a Grok Bot computer, like any Bot", and lists which computer each conversation uses. Every entry is a Grok Bot computer: the owner's, a teammate's, or one shared computer for a channel. The page does not list the member's own desktop.
- The [computers page](https://docs.x.ai/grok-bot/computers) describes "one hosted computer where every Bot they run does its work".
- The [security page](https://docs.x.ai/grok-bot/security) lists an "MCP allowlist" and "Allow Local Egress" as Enterprise-only settings. It does not explain "Allow Local Egress".
- No official Grok Bot page says that a Command server can run on the member's own computer. No page says that a Remote HTTPS server can use `http://` or a loopback address.
- For comparison only: the Grok app [connectors page](https://docs.x.ai/grok/connectors) says a custom MCP server "must be reachable over the public internet". It says a server on your local machine needs a tunneling service. That page is about the Grok app, not Grok Bot.

**Unconfirmed:** whether a Grok Bot Command server or a Remote HTTPS server can reach a gateway on the owner's Mac. The likely result, from the pages above, is no: both server types appear to run from Grok Bot computers. We record it as unconfirmed until the owner test.

## 3. Settings, plans and platforms

- Setting: "**Settings → General → Bot → Execution on Local Computer**", with **Ask every time**, **Always allow** or **Never allow**. The default is **Ask every time** ([approvals page](https://docs.x.ai/grok-bot/approvals-security-and-privacy)).
- After the account has registered computers, the choice moves to **Settings → Computer → Computers**. Each computer then has its own **Execution on this computer** setting (same page).
- First use shows the prompt "Allow Grok Bot and all Bots to run commands on your local computer?" The choices are **Always allow**, **Allow once**, **Never** and **Deny once**. **Always allow** and **Never** change the setting for every Bot (same page).
- A team admin can cap the setting. The stricter of the team and member settings applies ([approvals page](https://docs.x.ai/grok-bot/approvals-security-and-privacy), [security page](https://docs.x.ai/grok-bot/security)).
- Plans: the [get-started page](https://docs.x.ai/grok-bot/get-started) lists the plans that include Grok Bot. They are paid individual plans, the Teams plan, or a linked SuperGrok, SuperGrok Plus or SuperGrok Heavy subscription. **Unconfirmed:** any plan limit on local execution itself. None is documented.
- Platforms: the desktop app runs on macOS, Windows and Linux ([get-started page](https://docs.x.ai/grok-bot/get-started), [overview](https://docs.x.ai/grok-bot)). Local execution works "through the desktop app" ([security page](https://docs.x.ai/grok-bot/security)). **Unconfirmed:** whether a chat on iPhone or Android can run a command on a registered desktop.

## 4. Approvals and logs

- "Per-command approval is the default, and the approval card shows the exact command" ([security page](https://docs.x.ai/grok-bot/security)).
- The conversation shows "the proposed operation and its inputs". **Allow once** continues, **Always allow** can save a matching rule, **Deny** blocks it. "The controls are the same on iPhone" ([approvals page](https://docs.x.ai/grok-bot/approvals-security-and-privacy)).
- Approvals for work that started without you expire after about 10 minutes ([approvals page](https://docs.x.ai/grok-bot/approvals-security-and-privacy)).
- Audit Logs are Enterprise only. Action Recording is off by default; when enabled, it records Bot actions, including scrubbed shell commands, for 90 days ([security page](https://docs.x.ai/grok-bot/security)). **Unconfirmed:** which plans offer Action Recording.
- No page documents a personal history of local commands. The approval card in the conversation is the only documented personal record.

## 5. Consequence for Grok Gadgets

1. The gateway must keep its own record. `serve --request-log PATH` and `stdio --request-log PATH` write one JSON line per tool call to a mode-0600 file ([gateway #65](https://github.com/adidshaft/grok-gadgets-gateway/issues/65)). That log, not the Bot's narrative, is the test evidence.
2. Outcome (b) is the documented local path. It needs no tunnel and no public URL. Its limit: the Bot runs a fixed command line. It does not discover or call the six MCP tools itself.
3. Outcome (a) needs a direct test. If the Bot cannot reach `127.0.0.1` through an MCP server, a Grok Bot-native tool route needs the remote HTTPS design in [#4](https://github.com/adidshaft/grok-gadgets/issues/4).

## Sources

All read on 8 October 2026; no page shows an update date.

- Grok Bot overview: <https://docs.x.ai/grok-bot>
- Get started: <https://docs.x.ai/grok-bot/get-started>
- The computer and apps: <https://docs.x.ai/grok-bot/computer-and-apps>
- Approvals, security and privacy: <https://docs.x.ai/grok-bot/approvals-security-and-privacy>
- Security: <https://docs.x.ai/grok-bot/security>
- Troubleshooting: <https://docs.x.ai/grok-bot/troubleshooting>
- Team Bots: <https://docs.x.ai/grok-bot/team-bots>
- Computers: <https://docs.x.ai/grok-bot/computers>
- Grok app connectors (comparison only): <https://docs.x.ai/grok/connectors>
