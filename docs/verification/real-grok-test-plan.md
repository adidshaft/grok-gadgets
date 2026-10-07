# Real Grok simulator experiment — original proposal

Historical proposal: the user subsequently authorized the desktop cloud simulator experiment and requested a new dedicated Bot. See [recorded experiment and evidence gate](real-grok-experiment.md). The authorization statements below describe the original proposal, not the current approval state.

Checked official docs on 4 October 2026: [Grok Bot overview](https://docs.x.ai/grok-bot/overview) describes its persistent cloud computer; [Team Bot plugins](https://docs.x.ai/grok-bot/team-bots#plugins) lists Command and Remote HTTPS custom MCP routes. Availability must be confirmed in the actual account/client before configuration. Nothing here configures an account or grants approval.

## Proposed first route

After separate approval, use an existing Bot's cloud computer and its supported Command MCP option for simulation only. Transfer the reviewed gateway wheel from the final candidate, verify SHA256 against its manifest, install it and locked runtime dependencies into a dedicated environment there. Record OS/Python/client/account feature availability and installed version/hash. Configure the absolute executable path in that cloud environment with `--simulator --test-controls`. A private Mac path cannot be executed by the cloud command. No Mac device listener is exposed and no hardware is required.

If Command custom MCP is absent for the selected account, stop this experiment and record that exact availability gate. Do not create another API bot or assume localhost on the Mac is reachable.

## Actual tool acceptance

1. Ask the existing Grok Bot to call `gadgets_list_devices`; record actual tool payload/result and explicit simulated=true. Device command capabilities include rgb.set; button/state are input/read capabilities.
2. Ask it to call `gadgets_command` on the discovered device with capability rgb.set, valid green channels and a unique command_id. Verify executed status through `gadgets_command_status` and the resulting `gadgets_get_state`. Repeat off and inspect state.
3. Record state before attempting button/state/unknown and malformed RGB commands. Each must fail visibly and preserve LED state. Match actual published tool signatures rather than inventing parameters.
4. Explicitly request `test_simulator_control` button press/release and inspect `gadgets_read_events` edges/cursors. These are simulated events, not physical observations or proof that an event wakes a Bot.
5. Explicit disconnect, command failure/offline state, reconnect, discovery and successful command after reconnect. Keep test controls opt-in and remove them from ordinary configuration afterward.
6. Record client version, source/package hash, command IDs, timestamps, tool errors, before/after state and any consent prompts. Redact credentials and account identifiers. Repeat selected discovery/read/command in the existing mobile client after separate approval; do not infer mobile behavior from desktop.

Pass means an actual existing Grok Bot invoked the corrected simulator tools. Physical C124, local Linux peripherals and actual Home Assistant remain separate gates. No API charges, deployment, new Bot/team publication or account changes are currently authorized.

## Current connection paths and remaining gates

The [hosting FAQ](../getting-started/hosting.md) defines three separate paths:

1. **Cloud computer:** Grok Bot normally runs commands on its cloud computer. Its internet connection does not expose the user's private LAN. The cloud simulator experiment above cannot prove access to a Mac or Pi at home.
2. **Manual Mac → SSH → Pi experiment:** **Execution on Local Computer** is a separate capability. If the user enables it and approves a command, Grok Bot can run that command on the Mac. The command can reach a Pi if the Mac can reach it over the home network and SSH is set up. USB alone does not create the route. This possible experiment is not verified Grok Gadgets support or a packaged MCP integration.
3. **Packaged remote MCP:** The gateway implements stdio MCP, bearer-authenticated local HTTP MCP at `127.0.0.1:8766/mcp`, and authenticated loopback device transport. An authenticated remote MCP endpoint with TLS and approved, verified Grok Bot invocation are not complete. Do not point Grok Bot at the alpha as a ready-to-use remote service.

`HARD-GROK-REMOTE-001` tracks the remote route, authentication and access controls, credential revocation, and actual Grok Bot evidence. The local `serve` listener already exists. A tunnel adds reachability, not authentication. Do not expose raw device frames. Service activation needs separate approval.

**M5 — Actual Grok is blocked** on supported invocation and reload evidence for the exact kit, plus the remote route. **M8 — Physical and independent verification is blocked** pending a real Pi/device setup, observed peripheral behavior and independent reproduction. A successful manual SSH experiment would not, by itself, complete either gate.
