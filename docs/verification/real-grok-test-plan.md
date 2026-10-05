# Real Grok simulator experiment — original proposal

Historical proposal: the user subsequently authorized the desktop cloud simulator experiment and requested a new dedicated Bot. See [recorded experiment and evidence gate](real-grok-experiment.md). The authorization statements below describe the original proposal, not the current approval state.

Checked official docs on4October2026: [Grok Bot overview](https://docs.x.ai/grok-bot/overview) describes its persistent cloud computer; [Team Bot plugins](https://docs.x.ai/grok-bot/team-bots#plugins) lists Command and Remote HTTPS custom MCP routes. Availability must be confirmed in the actual account/client before configuration. Nothing here configures an account or grants approval.

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

## Future physical connection

The current [hosting FAQ](../getting-started/hosting.md) explains gateway operators, tunnel ownership and future deployment options. A tunnel supplies reachability only. It does not implement remote MCP or gateway authorization.

The gateway currently supports local stdio MCP plus authenticated loopback device transport. It has no authenticated remote HTTPS MCP/OAuth service for the cloud Bot to reach devices on this Mac. HARD-GROK-REMOTE-001 tracks the missing implementation: route/access design, OAuth or scoped credential lifecycle, TLS, authorization and isolation, bounded connections/commands, negative auth tests, redacted diagnostics and revocation. Do not expose raw loopback device frames or substitute an unauthenticated tunnel. Service development/activation must be approved separately.

Next decision: authorize the existing-account cloud Command simulator experiment above, or choose a separately scoped authenticated remote transport design. The prepared local release does not depend on either decision.
