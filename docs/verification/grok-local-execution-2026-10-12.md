# Grok Bot local-execution result — 12 October 2026

Run of the [owner checklist](../grok-local-test.md) on the owner's Mac, 12 October 2026, Asia/Kolkata (UTC+05:30). Software simulator only.

| Item | Value |
| --- | --- |
| Grok Bot desktop app | 0.66.0 |
| macOS | 27.0 (26A5388g) |
| Gateway | `dev` `5d1fcf3594622bb01ac349fa9ca8f00d314a8332`, package `0.1.0a4` |
| Hub | `dev` `381d30113fc77000e49931a8a4cc62aeaa7c957b` |
| Gateway log SHA256 | `5b6ab4290bbc7e612b561f367ca92d4ae8e54d44f37049de1a8ba2cc886a4c9e` (private, mode 0600) |

## Result

| Part | What the gateway log shows | Evidence level |
| --- | --- | --- |
| A1: Remote HTTPS to `http://127.0.0.1:8766/mcp` | No tool calls. Grok Bot declined to add the server. No token was sent. | Not verified. The Bot's reason is narrative only. |
| A2: Command MCP server on this Mac | No `stdio` log file was created. No tool calls. Grok Bot declined to add the server. | Not verified. The Bot's reason is narrative only. |
| B: approved local shell command | Six calls from client `grok-gadgets-rehearse/0.1.0a4`: list, command, state, twice. Both commands `executed`, `simulated: true`, blue `{"r":0,"g":120,"b":255,"on":true}`. Both state reads `fresh` and blue. | **Grok verification of the local-command route:** native approval cards showed the exact commands, and the independently retrieved gateway log matches them in time. |

Outcome: **(b)**. Grok Bot can run an approved `grok-gadgets-gateway rehearse` command on the Mac, and that command reaches the gateway on `127.0.0.1`. Grok Bot did not connect to the gateway as an MCP server in this run.

## Correlation

| Run | Native event (local time) | Gateway calls (UTC) | Output in chat |
| --- | --- | --- | --- |
| 1 | Retry requested 09:58:40 | 04:28:47.324581–04:28:47.329608 | 09:58:50 |
| 2 | Approval card 10:01:04 | 04:31:52.667769–04:31:52.673242 | 10:01:56 |

The client name is self-reported. Attribution rests on the native command cards, the chat output and the time match together. Nobody ran `rehearse` by hand during the test.

## Gateway log lines

The six tool-call lines, with request IDs and the HTTP user agent removed:

```json
{"ts":"2026-10-12T04:28:47.324581+00:00","event":"mcp_tool_call","transport":"streamable-http","client":"grok-gadgets-rehearse/0.1.0a4","tool":"gadgets_list_devices","args_sha256":"44136fa355b3678a","outcome":"ok","duration_ms":0.1,"devices":["sim-c124"]}
{"ts":"2026-10-12T04:28:47.327763+00:00","event":"mcp_tool_call","transport":"streamable-http","client":"grok-gadgets-rehearse/0.1.0a4","tool":"gadgets_command","args_sha256":"b79e3d10ec76dc8a","outcome":"ok","duration_ms":0.8,"device_id":"sim-c124","capability":"rgb.set","command_id":"gw-128dbbb4adb04c099a1edab518aae19d","status":"executed","duplicate":false,"simulated":true,"arguments":{"r":0,"g":120,"b":255,"on":true}}
{"ts":"2026-10-12T04:28:47.329608+00:00","event":"mcp_tool_call","transport":"streamable-http","client":"grok-gadgets-rehearse/0.1.0a4","tool":"gadgets_get_state","args_sha256":"63c35c833b649602","outcome":"ok","duration_ms":0.0,"device_id":"sim-c124","state":{"rgb":{"r":0,"g":120,"b":255,"on":true},"button":{"pressed":false}},"freshness":"fresh","simulated":true}
{"ts":"2026-10-12T04:31:52.667769+00:00","event":"mcp_tool_call","transport":"streamable-http","client":"grok-gadgets-rehearse/0.1.0a4","tool":"gadgets_list_devices","args_sha256":"44136fa355b3678a","outcome":"ok","duration_ms":0.2,"devices":["sim-c124"]}
{"ts":"2026-10-12T04:31:52.671220+00:00","event":"mcp_tool_call","transport":"streamable-http","client":"grok-gadgets-rehearse/0.1.0a4","tool":"gadgets_command","args_sha256":"b79e3d10ec76dc8a","outcome":"ok","duration_ms":0.8,"device_id":"sim-c124","capability":"rgb.set","command_id":"gw-2fd65ef1fe7449ddbbf61e898b8d1628","status":"executed","duplicate":false,"simulated":true,"arguments":{"r":0,"g":120,"b":255,"on":true}}
{"ts":"2026-10-12T04:31:52.673242+00:00","event":"mcp_tool_call","transport":"streamable-http","client":"grok-gadgets-rehearse/0.1.0a4","tool":"gadgets_get_state","args_sha256":"63c35c833b649602","outcome":"ok","duration_ms":0.0,"device_id":"sim-c124","state":{"rgb":{"r":0,"g":120,"b":255,"on":true},"button":{"pressed":false}},"freshness":"fresh","simulated":true}
```

The log also holds three `serve_started` / `serve_stopped` pairs. The server was stopped before A2 because the `stdio` server and `serve` both default to device port 8765.

## Deviations

- The owner selected **Always allow** on both approval cards instead of **Allow once**, and chose to keep it. The final setting is **Always allow**.
- The first Part B attempt failed because the gateway was stopped while the approval waited. The retry, with the gateway running, passed.
- Raw screenshots of the account stay private. They are not published.

## What this does not show

- Grok Bot discovering or calling the six MCP tools itself.
- Button events, slow-command polling, a read-only state read, invalid input, retry, off, disconnect or recovery through Grok Bot.
- Mobile clients or physical hardware. No physical device was used.
- That every local MCP route is impossible. Only the two configurations in the checklist were tried.

Issues: [#31](https://github.com/adidshaft/grok-gadgets/issues/31), [#4](https://github.com/adidshaft/grok-gadgets/issues/4), [#12](https://github.com/adidshaft/grok-gadgets/issues/12). Decision: [ADR 004](../decisions/004-grok-bot-route.md).
