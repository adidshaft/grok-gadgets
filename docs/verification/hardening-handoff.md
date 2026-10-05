# Corrected local alpha handoff —4October2026

All six audit corrections are implemented and locally tested. Twelve integrated acceptance groups passed on committed clean tracked inputs at hub5f3dedc, gateway221f73f, Linuxbe66ea4, ESPe78fb1c and Home Assistantb06eb07. Independent agent correctness review is closed. Independent assembled candidate certification passed; H0–H7 local acceptance is complete. Final current-HEAD candidate is generated after this evidence commit and identified by artifacts/publication/latest.json.

## Corrections and evidence

| Correction | Commit | Repeatable evidence |
| --- | --- | --- |
| Retained firmware ACK retry | ESPad89e7a | Actual ArduinoJson consumer repeated success/failure, FIFO/reboot;3CTest; C124 compile |
| Command/input capability routing | Gatewaye0b7256 | Negative official MCP calls preserve LED; discovery contracts;21tests |
| Per-device/boot event retention | Gateway7a4ba40 | Two-device saturation, reconnect and new boot dedup/window lifecycle |
| Installed custom factory | Linuxad3bb53 +abd7a28 | Documented and dataclass examples from fresh installed wheels; macOS and actual offline Linux |
| Honest persisted activity | Hub0078a5a +469db61 | Failed/owner-switch atomic file→build; old live cached; invalid/future unavailable |
| Safe usable documentation | Huba9550ab | Semantic Markdown, source-relative links/fragments, bounded static diagrams, explicit public selection and stale-output cleanup |

Independent reviewer accepted and fixed two additionalP2findings (old LIVE without refresh and dataclass module registration). See [review](hardening-review.md), [journal](hardening-journal.md), [checkpoint](hardening-status.md), [stages](../../planning/hardening-stages.json) and [compatibility](../../compatibility/tested-components.json). Source histories remain incremental, with full local Git repositories and final package bundles. Gateway and Home Assistant use separate environments because their MCP pins differ.

## Run locally

The five repositories must be siblings. In the hub:

```sh
uv venv .venv --python 3.13
uv pip install --python .venv/bin/python -r website/requirements.txt
.venv/bin/python scripts/check-all.py
.venv/bin/python website/build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory website/dist
```

Open http://127.0.0.1:4173/index.html. The main page includes all ten interactive component/tool entries, native keyboard/touch disclosures and concise evidence states, alongside the animated architecture and LED/button/offline illustration. This illustration is not a gateway connection.

Gateway simulation:

```sh
cd <workspace>/grok-gadgets-gateway
uv sync --locked
uv run python -m grok_gadgets_gateway.demo
```

Normal stdio MCP server: `uv run grok-gadgets-gateway --simulator`; test controls only with explicit `--test-controls`. The assertion-backed demo uses the official MCP client; it is not actual Grok.

Installed Linux custom acceptance, from hub:

```sh
.venv/bin/python scripts/check-installed-onboarding.py
```

This creates a fresh environment, installs the two built wheels with PYTHONPATH removed, extracts the exact documented custom example and runs both that and an annotated-dataclass variant through the installed console script and loopback gateway. For your own trusted file: in the SDK environment run `grok-linux-agent --factory-file ./my_gadget.py:create` with the credentials/port documented in the Linux operation guide. Python dependencies must be installed; file-directory/sibling imports are not automatically provided. See sibling Linux docs/development.md and docs/verification/hardening.md.

Home Assistant: in its repository `uv sync --frozen`, then `uv run ha-probe --fixture fixtures/assist.json`. C124: in ESP repository `.venv/bin/pio run -e atoms3-lite-usb` after its pinned setup; no flashing performed. All commands operate local software or compile.

## Verification levels

Observed:21gateway tests/MCP/TCP,20Linux source tests,13HA fixture/HTTPtransport tests,3ESP CTest suites plus canonical contracts/actual firmware consumer PTY,12website tests and6offline community tests. Twelve final runner groups pass; every group's report records command, UTC, HEAD, tracked diff hash and before/after status. Raw logs: artifacts/verification/20261004T164755-1791132475423552000/. The unrelated assets/ directory was the only untracked hub input and remains preserved.

Hub CPython3.13.5; installed Linux/macOS verifier3.11.15; actual offline Linux kernel6.10.14aarch64/glibc2.41 Python3.11.17 in pinned image from compatibility manifest. Fifteen installed Linux tests execute, five optional source-gateway tests skip; dedicated installed onboarding covers real local transport separately. No physical peripherals or systemd lifecycle claim.

Firmware: clean build source382444d5a7bb9372e8778421a337b82306aa2c58, PlatformIO6.1.18, espressif32 6.10.0, ArduinoJson6.21.5, NeoPixel1.12.3. RAM54,628bytes; programflash274,881bytes. Binary283,424bytes SHA256de30fff189e37682ede9613bfccabb39550b5fa30d606eab797da4c49b80de25. Source5ca2e5d afterward changes evidence/ledger only. Full bin/ELF/bootloader/partitions/toolchain manifest is in sibling artifacts/c124-usb. This proves compilation and host behavior, not electrical effects.

Website semantic guides reviewed at1280 and390px; original README→guide navigation, static diagram, keyboard disclosure and reduced-motion behavior recorded. Final desktop toolkit measurement:1280viewport,1265scroll width,10entries and Linux opened with Enter. Screenshot hardening-toolkit-final.jpg. Public website omits raw host logs and machine inventories.

## Publication and external gates

Original code Apache-2.0 in all five repositories; dependencies and official marks retain separate notices/provenance. The supplied assets/ source archive is preserved and excluded from Git. No public repositories, remotes, push, deployment, paid/account calls, device actions, Reddit changes or automation activation occurred.

The final unpublished package contains exact HEAD source archives, full-history bundles, freshly rebuilt Python packages, firmware outputs/provenance and the static site, with verified SHA256. Follow publication/README.md for the exact pointer and verification command. The reviewed candidate20261004T165602-1791132962841338000 is preserved; the final latest pointer identifies the subsequent evidence-only closure HEAD. Final external manifest identifies its own HEADs to avoid a self-referential tracked commit.

1. Actual existing Grok Bot account/client availability and approved cloud Command simulator experiment: [concrete next test](real-grok-test-plan.md). Remote HTTPS/OAuth for reaching this Mac's devices is unimplemented and tracked by HARD-GROK-REMOTE-001; not merely an account gate.
2. Physical AtomS3 Lite C124/data cable and separately authorized flashing/USB/LED/button/reboot observations. Wi-Fi provisioning/authentication remains future scope.
3. Actual Home Assistant installation, deliberately exposed entities and approved real Grok actions.
4. Real Linux systemd host, peripherals and serial permissions.
5. Another human independently installing/testing; agent review does not satisfy it.
6. Separate GitHub owner/repository/push/release/site approvals, verified hosted checks/protections, real private security reporting and dependency/binary redistribution review. Official-brand guidelines/naming remain a publication gate.
7. Separate Reddit moderator audit and exact change/post approvals; live recognition additionally needs approved identity, runtime, storage and deletion design.

The next concrete decision is approval to test the existing Grok Bot against simulation on its cloud computer. No such approval is assumed here.
