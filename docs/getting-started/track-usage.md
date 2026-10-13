# Track usage

Two counts matter: what your gadgets did, and how much of your Grok Bot plan the work used. The gateway records the first. Grok Bot shows the second. Neither one measures the other.

## Gadget calls: the gateway log

With a request log (always on for the service and for a tunnel), each tool call records the token name, client, device, capability, tool, outcome, duration and bytes. Summarize it:

```sh
grok-gadgets-gateway usage
grok-gadgets-gateway usage --token grok-bot --since 2026-10-13
```

The summary groups calls by token, device, capability and UTC day. Add `--json` for scripts. Full options: [gateway usage guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/usage.md).

For a live feed, start the gateway with `--usage-hook CMD`. Your program gets one JSON line per call on its standard input. The line holds no tokens, arguments or device state. A slow or failed program never delays a call.

## Grok Bot plan usage: Grok Bot's own pages

- Desktop: **Settings → Usage & Billing → Weekly usage limit**.
- Phone: **Settings → Usage → Weekly usage**.

The pages show whole percent, and the allowance resets weekly. Grok Bot measures its own work, not tool calls. No personal usage export or API is documented ([research note](https://github.com/adidshaft/grok-gadgets/blob/main/docs/research/grok-remote-https-2026-10.md#5-usage-and-credits)). The gateway never reads your Grok Bot account.

## An estimate per call

Read **Weekly usage** before and after a session, and note both times. Then let the gateway work out a rate:

```sh
grok-gadgets-gateway usage --token grok-bot \
  --since 2026-10-13T09:00 --until 2026-10-13T10:00 \
  --calibrate 2 --unit "% weekly usage"
```

Later summaries add a column labelled **estimate**. It covers everything Grok Bot did in that window, not only the tool calls.

In the owner's 13 October test, 11 messages and 9 tool calls left the page at 1%. That puts the session under 1 percentage point, as an upper bound ([ADR 007](https://github.com/adidshaft/grok-gadgets/blob/main/docs/decisions/007-grok-bot-remote-https.md#usage-per-prompt-and-per-tool-call-estimate)). A longer session gives a better rate.
