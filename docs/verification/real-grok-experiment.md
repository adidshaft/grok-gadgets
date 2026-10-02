# Real Grok simulator experiment — reported results, receipt gate

User authorized the proposed existing-account simulator connection test on 4 October 2026. Scope: inspect current MCP availability, install the reviewed gateway in the Bot environment, configure the simulator connection and request the concrete tools/tests. No physical hardware, public repository, deployment, purchase, Reddit action or broad unrelated Bot operation is included. Earlier local H0–H7 goal remains complete; this is the separately authorized next experiment.

Client: installed Grok Bot 0.61.0, bundle com.anysphere.sand. Native app is signed in. A blocking introduction requires designating a Primary Bot. User chose to create a new Bot. The Create Primary Bot flow created a new Primary Bot, renamed Grok Gadgets Test through its native name control. The startup briefly performed its built-in onboarding scan, then the explicit simulator-only prompt was sent and acknowledged: no other Bot messages/changes, Finance/trading, purchases, routines or sign-in. No unrelated Bot was selected for this test. The Bot reports Command MCP is available and the reviewed gateway is installed in its cloud environment. Local execution is Ask every time; security settings remain unchanged.

Reviewed gateway source:84b06fb9bef0f01639c215f2b5ada83fe5074218. Candidate wheel grok_gadgets_gateway-0.1.0a1-py3-none-any.whl,24,264bytes, SHA256ad21e29244d3e11e4dbcca93c07d4039cc844b6455c77c34c7050a55e2e3ea95; parent independently matched actual file against final candidate manifest. Runtime pins:mcp1.26.0,jsonschema4.26.0,pyserial3.5,Python>=3.11. Initial cloud executable arguments:--simulator --test-controls; no --credentials/device listener needed. The local Mac path is not a cloud executable path.

## Outcome and evidence strength

On 4 October 2026, the dedicated Bot returned JSON described as results of direct registered MCP calls, following explicit instructions to avoid terminal clients and mocked output. The observed app shows Bot messages containing these JSON results, not native connector invocation cards. The Bot explicitly says it has no native receipt view, link or downloadable original export. Accordingly this record establishes **Bot-reported simulator operation**, not independently verified actual Grok invocation. HUB-GROK-001 and M5 remain blocked on that evidence gate; compatibility `grok_verified` remains false. The reviewed local software acceptance remains complete.

The wheel and frozen hashed runtime requirements were uploaded through native chat attachments. Grok reports both hashes matched, Python 3.13.5, a venv at `/workspace/grok-gadgets-test/.venv`, runtime install/wheel install/official MCP demo exit 0, and seven tools initially registered. The terminal demo was explicitly kept separate from the reported direct connector calls. Runtime export: 37,943 bytes; SHA256 `24dfa1e3b7c86e8c557784c0d5c8f794c9944a5c50534b70d7f660e8aa143c0e`; generated with `uv export --frozen --no-dev --no-emit-project` from unchanged gateway lockfile. These cloud installation statements are Bot reports, not an independently inspected cloud filesystem.

## Reported acceptance

| Phase | Bot-reported result | App reply time (Asia/Kolkata) |
| --- | --- | --- |
| A | Discovery of sim-c124; green command executed, matching command status and green state; simulated true; diagnostics/receipt physical_verified false | 23:13:24 |
| B | Identical command ID returns unchanged timestamps; button/state/unknown rejected as unsupported_capability; range/empty/boolean/extra RGB rejected as invalid_arguments; rejected IDs unknown_command; green unchanged | 23:16:53 |
| C | Press/release edges read once; next cursor empty; disconnect offline; command rejected unavailable; reconnect new boot/session and reset off state; new blue command and off command executed | 23:18:10 |
| Cleanup | Args changed to --simulator; six ordinary tools, test_simulator_control absent; final off executed with matching status and off state | 23:19:01 |

These are simulated device reports. They do not establish physical LED/button behavior, an event waking a Bot, mobile behavior, Linux peripherals, actual Home Assistant or a cloud route to devices on the Mac.

The initial A instruction incorrectly required physical_verified in device state. The Bot stopped correctly. The corrected instruction read that field from diagnostics and the command receipt; state itself declares simulated. The initial compact discovery message omitted capability_contracts; later reported states include the rgb.set contract with required integer channels 0..255, boolean on and no extra properties. Phase B's state age 210.499 was stale, correctly distinguished from offline. Phase C's actual reported error code is `unavailable`, correcting the prompt's guessed `device_unavailable`.

Command IDs use prefix `grok-live-20261004-`: green-1; b-button/b-state/b-unknown/b-range/b-empty/b-bool/b-extra; c-offline/c-recovered/c-off; final-off. Distinct IDs were used for lifecycle commands to avoid retained receipt replay.

Reported initial gateway epoch `c6d0db8c0fde41ab91eeb5e25a6e9956`, boot `45a941d09f494129b2b7c8551506364c`, session `6447d11f5c964934b2f1fa7f17b15c98`. Green requested at `2026-10-04T17:43:16.256780+00:00`, executed at `17:43:16.257418+00:00`. Event next cursor `<epoch>:2` returned empty events, history_lost false, retention 128. Reconnect boot `2f5efc43af5c41ce875ff7120b53cd9d`, session `e6ef6b1c2a694756bf09cb1352252c99`. C off executed at `17:47:52.569573+00:00`. Diagnostics then reported two events, three commands, credentials redacted and physical_verified false. Cleanup restart produced boot `9050f7a65cf84cb28724b40712c3b415`, session `0ed300b7f83e4aa195b798d9bed08686`; final off executed at `17:48:47.617618+00:00`, state age 5.785 fresh.

## Final reported configuration and scope deviation

Name: Grok Gadgets Simulator. Command: `/workspace/grok-gadgets-test/.venv/bin/grok-gadgets-gateway`. Args: `["--simulator"]`; env: `{}`. Reported tools: gadgets_command, gadgets_command_status, gadgets_diagnostics, gadgets_get_state, gadgets_list_devices, gadgets_read_events. The Bot says connector status shows connected/stdio/six tools but does not echo the saved executable line; the saved configuration is therefore also reported evidence.

We requested restarting only this connector. The Bot subsequently disclosed there is no single-connector restart and its restart reconnected every installed connector. It reports no other connector settings were changed. This wider reconnect is recorded as a deviation; no further account actions are requested. Local execution approvals and Auto-review were not disabled. No credentials were requested, device listener exposed, public repository created, push, public gateway/site deployment, purchase or Reddit modification performed.

Private local evidence under ignored `artifacts/grok-live/`: phase-a-ax.txt, phase-b-ax.txt, phase-c-ax.txt and final-ax.txt contain accessibility observations of the dedicated test conversation only. Some offscreen code blocks are virtualized/truncated: these are not complete raw MCP exports. `final-bot-result.png` crops out unrelated sidebar conversations. These files remain local and are excluded from publication archives.

## Remaining gate

Obtain inspectable native connector invocation evidence or independently corroborated server-side execution records before closing HUB-GROK-001 or declaring actual Grok verification. No hardware is required for that simulator evidence gate. The C124 physical path, mobile client, actual Home Assistant, authenticated remote MCP/OAuth and independent human reproduction remain separate gates. The original authorized experiment has reached the available app evidence limit; it does not justify bypassing protections or exposing the Mac.
