# Grok Bot local-execution test: owner checklist

This ten-minute test shows whether your existing Grok Bot can drive the gateway on this Mac through **Execution on Local Computer**. The gateway request log is the evidence. The Bot's own description of what it did is not evidence.

Run it yourself, in your own Grok Bot account, in the desktop app on this Mac. Everything stays on `127.0.0.1`. You do not need a tunnel or a public URL. Background: [research note](research/grok-local-execution-2026-10.md).

There are two possible outcomes:

- **(a)** Grok Bot connects to the gateway's MCP endpoint directly and calls the six tools itself.
- **(b)** Grok Bot only runs shell commands that you approve. The command `grok-gadgets-gateway rehearse` then calls the tools.

The docs confirm (b). They do not document (a). Part A tests (a); Part B tests (b).

## 0. Prepare the gateway (2 minutes)

The request log is on the gateway `dev` branch. It is not released yet.

1. In Terminal tab 1, update the gateway checkout and set a short name for the command:

   ```sh
   cd ~/projects/grok-gadgets-gateway && git switch dev && git pull && uv sync --locked
   G="$HOME/projects/grok-gadgets-gateway/.venv/bin/grok-gadgets-gateway"
   "$G" init --client http
   ```

   Expected: `init` prints an HTTP settings block for `http://127.0.0.1:8766/mcp`. The token stays in `~/.config/grok-gadgets/mcp-token`.

2. Start the gateway with the simulated light and the request log:

   ```sh
   "$G" serve --simulator --request-log ~/grok-gadgets-requests.jsonl
   ```

   Expected: `MCP http://127.0.0.1:8766/mcp on 127.0.0.1; device listener 127.0.0.1:8765.` Leave this tab open.

3. In Terminal tab 2, watch the log:

   ```sh
   tail -f ~/grok-gadgets-requests.jsonl
   ```

   Expected: one `serve_started` line. Write down the time you start the next step. Times in the log are UTC.

## 1. Grok Bot settings (1 minute)

1. In the Grok Bot desktop app, open **Settings → General → Bot → Execution on Local Computer**. Select **Ask every time**. This is the default. Do not select **Always allow**.
2. If your account has registered computers, open **Settings → Computer → Computers** instead. For this Mac, set **Execution on this computer** to **Ask every time**.
3. Start a new one-to-one chat with your Grok Bot.

## 2. Part A: direct MCP connection (4 minutes)

The docs name two MCP server types, **Remote HTTPS** and **Command**. They do not show the exact screen for adding one. Use the Bot's MCP server or plugin settings if you see them. Otherwise, ask the Bot in the chat. Approve a card only if it shows the exact URL or command below.

### A1. Remote HTTPS to 127.0.0.1

1. In a new Terminal tab, print the token: `cat ~/.config/grok-gadgets/mcp-token`. You rotate it in step 4, so this copy stops working after the test.
2. Type in the chat:

   > Add a custom MCP server named grok-gadgets-local. Type: Remote HTTPS. URL: http://127.0.0.1:8766/mcp. Header: Authorization: Bearer TOKEN

   Replace `TOKEN` with the file contents.
3. If the Bot adds it, type these three prompts, one at a time:

   > Using the grok-gadgets-local tools, list my gadgets.

   > Set the light blue.

   > What's its state?

4. Watch tab 2. Note what the Bot says if it refuses or reports an error.

### A2. Command server on this Mac

Do A2 even if A1 fails.

1. Type in the chat, with your real home path:

   > Add a Command MCP server named grok-gadgets-stdio. Command: /Users/YOU/projects/grok-gadgets-gateway/.venv/bin/grok-gadgets-gateway. Arguments: stdio --simulator --request-log /Users/YOU/grok-gadgets-stdio.jsonl

2. If the Bot adds it, repeat the three prompts with "Using the grok-gadgets-stdio tools".
3. In a terminal, run `ls -l ~/grok-gadgets-stdio.jsonl`. If the file exists, the server ran on this Mac. If it does not exist, the server did not run on this Mac.

### What the log shows if (a) works

For A1, tab 2 shows `mcp_tool_call` lines whose `client` is **not** `grok-gadgets-rehearse`:

```json
{"ts":"…","event":"mcp_tool_call","client":"<name the Bot sent>","tool":"gadgets_list_devices","outcome":"ok","devices":["sim-c124"],…}
{"ts":"…","event":"mcp_tool_call","client":"<name the Bot sent>","tool":"gadgets_command","device_id":"sim-c124","capability":"rgb.set","status":"executed","simulated":true,"arguments":{"r":0,"g":…,"b":…,"on":true},…}
{"ts":"…","event":"mcp_tool_call","client":"<name the Bot sent>","tool":"gadgets_get_state","device_id":"sim-c124","state":{"rgb":{…}},"freshness":"fresh","simulated":true,…}
```

For A2, the same lines appear in `~/grok-gadgets-stdio.jsonl` with `"transport":"stdio"`.

If no new lines appear, the Bot did not reach this gateway, whatever the Bot says.

## 3. Part B: approved shell commands (2 minutes)

1. Remove `grok-gadgets-local` and `grok-gadgets-stdio` from the Bot if it added them. This keeps Part B separate.
2. Type in the chat, with your real home path:

   > List my gadgets: run this command on my Mac and show me the output: /Users/YOU/projects/grok-gadgets-gateway/.venv/bin/grok-gadgets-gateway rehearse

3. Check the approval card. It must show that exact command. Select **Allow once**.
4. Type:

   > Set the light blue: run /Users/YOU/projects/grok-gadgets-gateway/.venv/bin/grok-gadgets-gateway rehearse --device sim-c124 --command rgb.set --args '{"r":0,"g":120,"b":255,"on":true}'

   Select **Allow once** again if the card shows that exact command.
5. Type:

   > What's its state? Read it from the output you got.

### What the log shows if (b) works

Each approved command adds three lines with `"client":"grok-gadgets-rehearse/0.1.0a4"`: `gadgets_list_devices`, `gadgets_command` with `"status":"executed"`, and `gadgets_get_state` with the state. Their times must follow your approval by a few seconds. The command output in the chat ends with `Rehearsal passed`.

### What (b) does not give you

- The Bot runs one fixed command line. It does not discover or call the six tools itself.
- Each `rehearse` run sends a command. There is no read-only state command, so "what's its state" comes from the last output.
- The Bot cannot read button events or poll a slow command.
- Each run needs your approval, the desktop app and an awake Mac.
- The log shows `grok-gadgets-rehearse`, the same as when you run it yourself. Only the time next to your approval links a line to the Bot.

## 4. Turn everything off (1 minute)

1. In tab 1, press Ctrl+C. Expected: `Gateway stopped; device sessions closed.` The log ends with `serve_stopped`. Stop `tail` in tab 2 with Ctrl+C.
2. In Grok Bot, remove any MCP server that the test added.
3. Set **Execution on Local Computer**, or **Execution on this computer**, back to your earlier choice. The docs recommend **Never allow** unless a Bot needs local files.
4. In **Settings → General → Bot → Auto-review**, delete any **Allow automatically** rule that the test created.
5. If you pasted the token in A1, replace it: `"$G" rotate-mcp-token`.
6. Copy the log lines into the results below. Then delete the files: `rm -f ~/grok-gadgets-requests.jsonl ~/grok-gadgets-stdio.jsonl`.

## 5. Results template

Paste this back with the log lines. The log contains no tokens, but read it before you paste it.

```text
Date and time zone:
Grok Bot desktop app version and macOS version:
Execution on Local Computer setting used:

A1 Remote HTTPS http://127.0.0.1:8766/mcp
  Bot added the server (yes / no / refused):
  Bot message if it failed (short summary):
  New mcp_tool_call lines with a client other than grok-gadgets-rehearse (yes / no):

A2 Command server on this Mac
  Bot added the server (yes / no / refused):
  ~/grok-gadgets-stdio.jsonl exists (yes / no):
  mcp_tool_call lines in that file (yes / no):

B Approved shell command
  Approval card showed the exact command (yes / no):
  Approval times (local):
  grok-gadgets-rehearse lines a few seconds after each approval (yes / no):

Log lines (from ~/grok-gadgets-requests.jsonl and ~/grok-gadgets-stdio.jsonl):

Other observations:
```

The result is recorded in [#31](https://github.com/adidshaft/grok-gadgets/issues/31) and [#4](https://github.com/adidshaft/grok-gadgets/issues/4). A simulated light is used, so the result is never physical verification.
