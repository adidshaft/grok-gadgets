# Grok Gadgets — audit corrections and local release readiness

**Prepared:** 4 October 2026
**Status:** Continuation plan; none of these corrections has been implemented by the planning chat.
**Execution:** A separate Codex chat using the accompanying `/goal` prompt.
**Workspace:** `<workspace>/grok-gadgets` and its four existing sibling repositories.
**Outcome:** Correct the six audited problems, demonstrate the corrected behavior, preserve incremental history, and deliver an accurately documented local alpha candidate.

This plan extends `docs/implementation-plan.md`; it does not replace the product direction or restart the project. Read the original plan and applicable `AGENTS.md` files before implementing. The original handoff's statement that the local alpha is complete predates the findings below and must be qualified during this work.

The user specifically requires sustained execution, tested incremental commits, and documentation of the process and stages. Continue through the required local stages without requesting permission after each ordinary development step. A passing pre-existing test suite alone does not close this goal.

## 1. Scope and authorization

The product remains exclusively for the existing Grok Bot, with independent Linux and ESP32 SDKs, upstream Home Assistant reuse, and an open-source project hub. Original code remains Apache-2.0. Keep exactly the existing five repositories; put the website and community preparation in the hub.

Local source changes, dependencies needed for those changes, isolated branches/worktrees, builds, test execution, documentation, and local commits are authorized when this plan is activated in the build chat. Public documentation research is permitted. Preserve unrelated user work, especially the untracked `assets/` directory in the hub. Do not automatically add, delete, license, or incorporate those brand files.

The existing external boundaries still apply:

- Do not create public repositories, push, publish packages/releases, deploy websites/gateways/tunnels, purchase anything, or make paid model API calls.
- Do not change Reddit, award real flair, send messages, or activate recurring/unattended automation.
- Do not access Grok/Reddit accounts, flash hardware, or operate real household devices merely because test preparation is complete. Use the existing separate authorization gates.
- Use Chrome or the permitted built-in browser. Never open Brave, Safari, or Passwords. Stop the affected step and ask if it would require Passwords.
- Do not create additional user-visible chats. Use bounded collaboration subagents within the goal chat.
- Do not change global Codex settings or add another AI backend to the product.

Account, physical hardware, independent human testing, and public activation are outside the mandatory completion criteria for this local correction goal. Prepare concrete next steps for them. Do not represent them as accomplished or wait indefinitely for them while useful local work remains.

## 2. Starting evidence and repository ownership

At the audit, all eleven existing groups in `python3 scripts/check-all.py` passed. The five repositories contained 29 commits, and all seventeen publication files matched their recorded checksums. Additional focused probes nevertheless found the six problems in Section 3. Test counts and hashes below describe that historical snapshot, not a guarantee about the next chat's starting state.

| Repository under `<workspace>` | Audited HEAD | Ownership |
| --- | --- | --- |
| `grok-gadgets` | `6f749f840c613b50deb60b1b6737b00bfb783895` | Coordinator, issues, cross-repository acceptance, website, community, publication preparation |
| `grok-gadgets-gateway` | `d2b1008c2f2a7474288bf3ae9aa83cd49c1e5554` | Canonical protocol, gateway, simulator, MCP and device transports |
| `grok-gadgets-linux-sdk` | `2fea71b65e6a3a0e1aa4583270442cc2bb7cbfed` | Linux library, CLI, developer example and service instructions |
| `grok-gadgets-esp32-sdk` | `41ee9635efeef553197e3d15363e02146d87e773` | Portable firmware SDK, C124 USB example, host tests and board compilation |
| `grok-gadgets-home-assistant` | `5a808b23371e373e961a0217ac94d1e6b6129418` | Upstream integration recipe, read-only probe and fixture tests |

Reinspect current branches, remotes, dirty files, local instructions and active agent assignments. Do not reset newer work to these commits. If another chat is editing the same files, reserve ownership or use an isolated checkout before proceeding. No substantive Home Assistant change is required unless integration testing finds a defect.

**Concurrent work observed during plan preparation:** the hub changed from `main` to `feat/interactive-website`, with modified `website/build.py`, `website/motion.js`, and `website/style.css`, plus untracked `website/home-scene.html`, `website/scene.css`, and `website/scene.js`. The existing untracked `assets/` directory remained present. These changes were not made by this planning task. Reinspect rather than assume this inventory remains current. Do not switch, reset, stage or commit another workstream's checkout. Coordinate file ownership or use an isolated worktree, and agree integration before editing the website files. Reproduce website findings against the appropriate current version; a concurrent correction may already resolve part of them.

Copy this plan into the hub as `docs/hardening-plan.md` in the first implementation stage. Keep that repository copy authoritative during execution. Preserve the original implementation plan as historical context and make its status/date clear rather than silently rewriting its original conclusions.

## 3. Six audited correction work items

Use the proposed IDs below if they are unused; otherwise allocate stable alternatives and retain a mapping. Create a hub coordination issue `HARD-001` and component issues in their owning local ledgers. Add type, area, priority and milestone labels. This table's priorities are triage recommendations, not claims that every defect has the same impact.

### HARD-ESP-001 — preserve acknowledgements across repeated retries

**Repository:** ESP32 SDK. **Priority:** P1.
**Starting location:** `lib/GrokGadgets/src/GrokGadgets.h`, around line 59; `tests/device_tests.cpp`, around line 42.

`Device::execute` deserializes a cached acknowledgement from a mutable `char[]`. The installed ArduinoJson parser modifies that buffer. The original command and first retry return a valid acknowledgement; subsequent retries return JSON `true` in the focused host reproduction. The handler still executes once, but the transport response is invalid. Existing tests exercise only one retry.

Reproduce by registering a `counter.bump` handler, sending an identical command ID and arguments four times, and serializing each returned acknowledgement. The observed sequence was:

```text
call 1: executions=1, valid executed acknowledgement
call 2: executions=1, valid executed acknowledgement
call 3: executions=1, true
call 4: executions=1, true
```

Use the actual installed headers and current implementation for the reproduction. Fix the buffer ownership/read-only parsing problem and handle deserialization failures explicitly. Do not merely special-case the reproduction or remove duplicate protection.

Acceptance:

- Multiple repeated requests return equivalent valid acknowledgements and execute the handler once while the ID is retained.
- Cover both successful and failed acknowledgements, interleaved command IDs, and duplicate IDs with changed arguments.
- Preserve documented bounded retention and reboot semantics; do not claim durable exactly-once execution.
- Exercise the retry behavior through the actual firmware consumer/host transport where practical, as well as the library regression.
- Host tests, formatting, canonical contract checks, gateway USB simulation and real C124 compilation pass.
- Regenerate firmware outputs, source provenance and checksums after the fix. Keep physical verification explicitly pending.

### HARD-GW-001 — route simulator commands by capability

**Repository:** Gateway. **Priority:** P1.
**Starting location:** `src/grok_gadgets_gateway/simulator.py`, around lines 38–49; `domain.py`, around lines 103–107 and 145.

The simulator declares `rgb.set`, `button`, and `state`. Its execution loop treats any delivered command as an RGB command. A `button` command carrying RGB-shaped arguments changes the simulated LED and returns `executed`. Discovery also exposes event/state capabilities as though they were command contracts.

Reproduction at the audited snapshot:

```python
gateway.command("sim-c124", "button", {"r": 1, "g": 2, "b": 3, "on": True}, "audit-button")
simulator.execute()
```

Construct the gateway and simulator using their existing test helpers. Confirm the wrong state change and result before fixing it.

Acceptance:

- Only supported command capabilities execute. `button`, `state`, unknown commands, and malformed RGB requests cannot mutate the LED or report a successful wrong action.
- Input events and state reads remain usable through the intended interfaces. Test-only button injection stays separate and absent by default.
- Discovery accurately communicates which operations are callable, without silently breaking valid custom SDK capabilities.
- Add negative tests through the real MCP tool surface, not only direct Python calls.
- Existing RGB, event, disconnect, reconnect, authentication and transport tests remain green.
- If clarifying the capability model affects canonical schemas or SDK assumptions, document the compatibility decision and update pinned consumers together. A small backward-compatible fix is preferable to unnecessary protocol redesign.

### HARD-GW-002 — isolate event duplicate windows by device and boot

**Repository:** Gateway. **Priority:** P2.
**Starting location:** `src/grok_gadgets_gateway/domain.py`, around lines 254–272; `protocol/0.1.0/README.md`, around line 11.

The contract promises a retained duplicate window of 256 event identifiers per device/boot. The implementation uses a single global cache of 256 entries. In the reproduced case, device A sends an event, device B sends 256 events, and retrying A's original event is accepted as a new event.

Implement the documented isolation with bounded resource management. Do not close this issue merely by changing the wording to weaken the promised behavior. If a stronger constraint makes the current promise impractical, record the tradeoff and propose a coordinated contract decision before changing it.

Acceptance:

- Two devices may reuse the same event ID without interfering with each other.
- A busy device cannot evict another device's retained duplicate window prematurely.
- Identical retries do not increment sequence or enqueue another event; changed content under a retained ID still conflicts.
- Boundary tests cover the last retained ID and eviction beyond the stated per-device/boot window.
- Reconnect, boot change and gateway restart follow explicit documented semantics. Stale sessions cannot inject events.
- Histories, retired sessions and device/boot bookkeeping remain bounded under the supported lifecycle. Do not fix isolation by introducing unbounded retention.
- Update protocol evidence and any affected SDK pin/hash records consistently.

### HARD-LIN-001 — make the documented custom-gadget path work

**Repository:** Linux SDK. **Priority:** P1.
**Starting location:** `docs/development.md`, around line 26; `src/grok_gadgets_linux/cli.py`, around line 29.

The guide tells a developer to create `my_gadget.py` and run `uv run grok-linux-agent --factory my_gadget:create`. The installed console entry point does not automatically make that working directory importable. A focused isolated-directory check failed before the factory ran; adding that directory explicitly to `PYTHONPATH` reached the factory. The root audit completed that control check.

Choose and document one clear supported onboarding route: an explicit module/file path option, a properly installed example package, or another standard invocation that actually works. Avoid silently adding arbitrary directories to global import settings. An explicit trusted local code path is different from accepting remote/untrusted code.

Acceptance:

- From a clean temporary directory and fresh environment, install the built wheel and follow the written example exactly. It must reach the custom factory, register with a local gateway, execute a custom capability, and report state.
- Do not hide the problem through a test-only `PYTHONPATH`, editable source checkout, IDE configuration or inherited developer environment unless that setup is explicitly the documented supported route.
- Keep the built-in example, `--help`, bad factory/module/function cases, and credential-safe diagnostics working.
- Errors explain an actionable category without exposing tokens or private exception data.
- Run the corrected onboarding on macOS and an available actual Linux environment, preferably the existing pinned container setup. Record the tested package and platform.
- The correction does not imply systemd, USB permissions or physical peripherals were verified.

### HARD-WEB-001 — persist accurate activity states after refresh failure

**Repository:** Hub website. **Priority:** P2.
**Starting location:** `website/activity.py`, around lines 119–152; `website/test_activity.py`.

On a refresh error, `refresh()` returns a `cached` or `unavailable` result before writing it to the cache. A subsequent website build consuming that file can still read its old `live` state. The audit confirmed `returned state=cached` while the saved file remained `live`.

Acceptance:

- Persist the same validated result that the refresh operation reports, including failed-refresh cached/unavailable states. Avoid truncated intermediate files.
- Test the actual refresh-to-file-to-build path: start with old live data, simulate a fetch failure, rebuild, and assert the visible status is cached with its last successful timestamp.
- Missing, invalid or corrupt cache data has an honest documented fallback; stale data is not silently called live.
- An owner change cannot display the previous owner's metrics. Test this through the saved file, not only a returned Python object.
- Preserve successful refresh throttling, bounded requests, fixture labels, safe output escaping and no client-side credentials.
- Tests use fixtures or a local fake requester. Do not enable the real GitHub refresh job or scheduler.

### HARD-WEB-002 — render documentation as a usable website

**Repository:** Hub website. **Priority:** P2.
**Starting location:** `website/build.py`, around lines 219–249; component-document import logic and the source manifest.

Canonical Markdown currently appears inside a single escaped `<pre>` block. Its links, tables, headings and diagrams are displayed as source text. The generated ESP32 README page had zero links inside its main content even though its source points users to additional instructions.

Use a maintained, pinned Markdown renderer or another small, justified solution. Preserve the site's existing visual direction and static/self-hostable design; this is not authorization for an unrelated redesign. Update dependency setup and CI commands if the builder gains dependencies.

Acceptance:

- Headings, paragraphs, lists, tables, fenced code and internal anchors render correctly and accessibly.
- Component README links reach the correct generated component guides. Resolve paths against the original repository/source path recorded in the import manifest, not the flattened snapshot filename.
- Render project diagrams with a pinned local tool/bundle or generated accessible static output. Do not execute arbitrary content, load unapproved remote scripts or use an external rendering service.
- Reject unsafe URL schemes and unsafe raw HTML. Retain script-injection regression coverage, including malicious links and diagram input if diagrams are rendered dynamically.
- The link checker validates rendered document links and fragments, not only the handwritten navigation. Links to source files not mirrored into the site need a real, clearly documented local alternative or a correctly identified publication gate, never a fabricated GitHub URL.
- Images and code remain readable on narrow screens; check representative gateway, Linux, ESP32 and Home Assistant guides at desktop and approximately 390px widths.
- Keyboard navigation, focus, reduced-motion behavior and the existing home page continue to work.
- Deleted or renamed source documents do not leave stale generated pages behind. Clean only the known generated output directory, preserving unrelated files.
- Define which documents belong on the public site. Local operation logs, private account information and machine-specific paths must not be indiscriminately published by a recursive documentation glob. Keep public progress summaries informative and sanitized.

## 4. Stages, dependencies and exit gates

Each stage needs a recorded start, outcome, evidence, local issue status and commit references. Parallelize independent work after H0; do not serialize all six fixes unnecessarily. Integration and package preparation depend on the tested component commits.

| Stage | Deliverable | Exit gate |
| --- | --- | --- |
| H0 — Baseline and tracking | Plan copy, current inventory, six labeled issues, execution journal and stage tracker | Current state preserved; baseline checks recorded; repository/file ownership agreed; tracking commit exists |
| H1 — Behavioral corrections | ESP32 retry fix and both gateway fixes | Focused before/after evidence, full affected checks, firmware build and coherent local commits |
| H2 — Linux onboarding | Reproducible custom-gadget installation and updated CLI/docs | Installed-wheel path works as written, relevant Linux evidence recorded, regression tests committed |
| H3 — Website corrections | Accurate persistent activity states and rendered documentation | File-to-build failure tests and useful document navigation pass; desktop/mobile review recorded |
| H4 — Cross-repository acceptance | Compatible snapshots, refreshed docs, clean-environment exercises | Corrected components work together; original acceptance remains green; evidence identifies exact source states |
| H5 — Independent review and closure | Bounded reviewer report and fixes for material findings | Six audit items meet acceptance; remaining local review defects resolved or explicitly prevent completion |
| H6 — Candidate and next validation package | Updated manifests, archives, checksums, release notes and real-Grok test procedure | Artifacts correspond to final source commits; handoff separates local completion from external gates |
| H7 — Final completion audit | Final status, commit map, test matrix and resumable handoff | Section 11 checklist satisfied; tracked implementation work committed; user receives concrete result |

H1, H2 and H3 may overlap under exclusive ownership. H4 runs after their integration. H5 may begin reviewing an already completed component earlier, but final review must cover the final integrated changes. H6/H7 must not archive or certify obsolete pre-fix artifacts.

### H0 details

1. Read all relevant instructions, both plans and the old handoff; inspect all five working trees.
2. Record actual HEADs, dirty paths and available runtimes without dumping credentials or unrelated environment variables.
3. Reserve bounded workstreams. If using worktrees, record their paths and the integration owner.
4. Run the baseline once. Existing suite success and the audit regressions are different evidence.
5. Create the local issues and tracking documents. Qualify the earlier completion claim and link the new correction milestone from the roadmap/handoff.
6. Commit this useful setup as one coherent documentation/tracking increment. Do not create empty placeholder scaffolding.

### H4 details

Run the normal acceptance suite on the integrated component set, then execute the scenarios missing from the original suite:

- Repeat a firmware command several times through the actual consumer path and validate every acknowledgement.
- Invoke an invalid simulator capability through MCP and verify no unintended state mutation.
- Interleave two devices' events and retries across the retention boundary.
- Install the Linux wheel into a fresh environment and execute the documented custom example against the gateway.
- Build the website from a persisted failed-refresh result and inspect the visible data state.
- Follow rendered component documentation links from getting started through build/run instructions.

Use deterministic, bounded fault scenarios for disconnect, reconnect, overflow, changed arguments, boot/server restart, and revocation where affected. Do not run an arbitrary hours-long soak or endlessly repeat green tests simply to keep the goal active.

### H6 details

Refresh tested-component records, component documentation snapshots, issue exports/migration data, stage summaries, release notes and source histories. Rebuild changed packages, firmware and website output before producing the final local publication package. Verify hashes by reading the actual output files.

The package generator currently collects existing `dist` and firmware outputs; their existence does not prove they were built from the new commits. Prevent stale artifacts from being labeled as corrected. Record each artifact's actual source commit and build environment. Use clean/staged source provenance honestly.

A Git-tracked manifest cannot contain the hash of its own future commit. Record tested implementation commits in tracked evidence, then generate final archives from the resulting committed HEADs and record those HEADs in the external artifact manifest. Do not create an endless chain of metadata-only commits trying to solve self-reference.

Prepare `docs/verification/real-grok-test-plan.md` with the exact next experiment: real existing Grok Bot discovers and operates the corrected simulator, including a failure case. Identify where the MCP process would run and how it would reach the user's host. A cloud command cannot execute a private Mac path.

Recheck current official Grok documentation for that procedure. If an authenticated remote transport is still unimplemented, say so plainly and create a concrete follow-up issue with implementation and test criteria. Do not call it merely an account-access problem, substitute a separate developer-API bot, invent a supported route, expose a port, or expand this correction goal into an unreviewed hosted service.

## 5. Commit discipline

Use `main` plus short-lived feature branches. Keep unrelated agent work isolated and integrate only tested changes. Preserve existing history; no destructive reset, force push, project-wide squash or blind staging of all files.

For every coherent correction or stage deliverable:

1. Read the issue acceptance and establish the relevant baseline.
2. Reproduce the problem with a meaningful assertion or observable failure. Keep expected failing experiments off `main`.
3. Implement the smallest sufficient correction together with its regression test and affected documentation.
4. Run the changed subsystem's checks and regressions that protect earlier completed work. For firmware changes, compile the actual C124 target as required by the repository.
5. Run the hub's `python3 scripts/check.py` before committing, plus the owning repository's required checks. Coordinate reads of shared tracking files with their owner.
6. Inspect the diff and stage only intended files. Document actual failures and recovery, not just the final green result.
7. Commit with a clear subject and the local issue ID, such as `fix: preserve cached firmware acknowledgements [HARD-ESP-001]`.
8. Record the resulting SHA in the next issue/journal checkpoint and update the stage tracker before dependent work proceeds.

Each independent fix should have its own meaningful commit; split larger work into additional tested slices. Documentation/tracking, integration, and final evidence deserve separate commits when they are distinct deliverables. There is no artificial commit quota, timer or requirement to create empty progress commits.

Before accepting commit N+1, checks protecting functionality through commit N must still pass. Re-run all cross-repository acceptance at shared-interface boundaries and before final completion; avoid full ecosystem rebuilds after a purely textual journal edit unless it changes a tested input.

Do not commit a known broken implementation as a progress milestone. If an interruption occurs mid-fix, preserve the working tree and record its exact state in the checkpoint. A draft branch is not a passing integration. Do not amend unrelated history to make evidence appear earlier than it was recorded.

## 6. Documentation of execution and stages

Keep the process understandable without requiring access to the chat. Record concise engineering facts, commands, observations and decision reasons; do not dump private chain-of-thought, full agent transcripts, credentials or private account data.

Create these substantive records in the hub during H0 and maintain them throughout:

| Record | Purpose and update cadence |
| --- | --- |
| `docs/hardening-plan.md` | Versioned copy of this plan; update only for justified scope/implementation decisions |
| `docs/verification/hardening-journal.md` | Chronological work log; append at meaningful experiments, failures, decisions, fixes and stage transitions |
| `planning/hardening-stages.json` | Machine-readable H0–H7 status, owners, dependencies, linked issues, checks, commits and blockers |
| `docs/verification/hardening-status.md` | Short current checkpoint: completed work, active work, repository HEADs, dirty paths, next exact action |
| `docs/verification/hardening-review.md` | Independent findings, disposition, fixes and rerun evidence |
| `docs/verification/hardening-handoff.md` | Final user/developer guide, correction summary, commands, evidence and external gates |

Use the existing local issue ledgers as the authoritative issue state and the stage tracker as a rollup. Do not create a competing tracker with different statuses. Regenerate issue Markdown exports, migration fixtures and website roadmap when their sources change. If no remote exists, update local issues only; do not create GitHub issues through a connector.

Journal entry shape:

```text
Time (UTC):
Stage and issue:
Repository / branch / agent and actual model setting:
Starting commit or source state:
Objective and observed problem:
Action or decision, with short reason:
Checks: exact command, environment, exit/result, evidence location:
Outcome: passed / failed / blocked / superseded:
Commit: known SHA, or explicitly pending until the next checkpoint:
Limitations and next action:
```

Evidence should include timestamp, repository, source commit and working-tree state, relevant dependency/toolchain versions, command and exit code. The current acceptance runner logs HEAD even when there may be uncommitted changes; do not present such a run as proof of a clean committed snapshot. Improve evidence capture where necessary and retest the integrated committed sources.

Keep concise sanitized results and manifests in Git. Large raw logs, packages and binaries can remain in ignored artifact directories, with hashes and reproduction commands in tracked records. Before rerunning a tool that overwrites its last result, preserve any evidence needed to explain a failure or stage transition under a separate run identifier.

Update status and journal before context compaction, handoff or an interruption when possible. On continuation, read the status, active issues, Git state and latest evidence instead of restarting the project. Refresh source facts if another chat or user has changed the checkout.

Chat progress updates should explain what became usable, what failed, and what the next step will establish. Do not stop after every commit to ask whether to continue; ongoing local execution is already authorized by the activated goal.

## 7. Subagent organization and model policy

Use one coordinator and bounded subagents when useful. Never exceed the tool's actual concurrency limit. Assign exclusive repository or file ownership and communicate proposed interface changes before dependent edits.

Suggested initial waves:

- Coordinator owns hub tracking and integration; gateway agent owns HARD-GW-001/002; firmware agent owns HARD-ESP-001; Linux agent owns HARD-LIN-001.
- When capacity frees, assign the two website issues to one owner or separate non-overlapping files under an agreed interface. Coordinator retains shared status and final integration ownership.
- Use a bounded independent reviewer after fixes; the reviewer should inspect implementation and evidence, reproduce important cases, and report findings without editing another agent's files.

Model settings inherit the original project's approved policy:

| Work | Preferred model | Effort |
| --- | --- | --- |
| Coordinator and ordinary implementation | `gpt-6.1-sol` | Medium |
| Firmware retry semantics, event retention and protocol changes | `gpt-6.1-sol` | High |
| Linux onboarding and website implementation | `gpt-6.1-sol` | Medium; raise to High for difficult failures or unsafe rendering questions |
| Independent correctness/integration review | `gpt-6-astra` | Medium |
| Bounded documentation/inventory assistance | `gpt-6-luna` | High, when useful and supported |

Allowed models: `gpt-6.1-sol`, `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`, `gpt-5.6-sol`, `gpt-5.6-terra`. Prefer current 6.1/6 models. GPT-5.6 Terra is the lowest permitted fallback; do not use 5.6 Luna, 5.5 or earlier models.

These are project assignments, not benchmark claims. Verify supported tool identifiers and effort combinations. Select them explicitly where supported, report substitutions, and record the actual settings. Respect bounded-context/full-context fork restrictions and never silently downgrade outside the allowlist. No global settings edits.

Agent handoffs must contain owned files/repository, issue and acceptance criteria, starting/refined interfaces, branch/commit IDs, commands/results, limitations, and the next dependency. A subagent's assertion of completion does not replace coordinator verification. Keep user-owned additional chats separate from collaboration agents; do not create or message them without explicit permission.

## 8. Verification commands and coverage

Read the current scripts before running them. Paths and commands below were valid at the audit; if a justified dependency or interface change alters a command, update all developer docs and CI references together.

From the hub:

```sh
python3 scripts/check.py
python3 scripts/check-all.py
python3 -m unittest discover -s community/tests
python3 -m unittest discover -s website -p 'test_*.py'
python3 website/build.py
```

The existing cross-repository runner covers hub validation, website build, website activity tests, community tests, gateway tests, official MCP demo, Linux tests, Home Assistant tests, ESP32 host tests, canonical contract validation and the USB consumer integration. Extend it to include the new regressions rather than leaving important probes as one-off chat snippets.

Component requirements:

| Repository | Required relevant checks |
| --- | --- |
| Gateway | `uv run pytest`; `uv run ruff check .`; official MCP demo; new command-routing and multi-device event regressions |
| Linux SDK | Frozen dependency sync as needed; Ruff lint/format; `uv run python -m unittest discover -s tests -v`; `uv build`; fresh installed-wheel custom example; actual Linux run for changed Linux behavior |
| ESP32 SDK | `sh tools/check.sh`; `.venv/bin/python tools/check_contract.py`; gateway-environment `tools/check_gateway.py`; `.venv/bin/pio run -e atoms3-lite-usb`; refreshed build package/provenance |
| Home Assistant | Existing lint/format and thirteen-test baseline or its current successor; fixture/transport regressions as part of final integration |
| Hub website | Existing lint/format; rendered Markdown/link/anchor tests; persisted cache failure tests; static build; representative browser review |

Use current pinned tools and existing reusable environments where appropriate, plus clean environments for installation acceptance. Test an installed wheel without accidentally importing from the editable checkout. Run a safe, bounded local gateway for the custom example. Keep any test port bound to loopback and clean up only processes owned by the test.

Do not equate these evidence levels:

- A passing simulator or fake endpoint proves the tested software behavior.
- Firmware compilation proves buildability in that toolchain.
- A Linux container run proves the tested Linux software behavior, not real systemd/peripherals.
- An actual Grok account invoking the tools is required for Grok verification.
- Physical LED/button observation is required for C124 hardware verification.
- Another human following the instructions is required for independent reproduction; another agent or a fresh local environment is useful but does not satisfy that claim.

## 9. Long-running execution and interruption policy

This is a persistent, finite goal with observable completion conditions. Its duration follows the work required; it has no artificial minimum time, fixed number of iterations, or expectation to consume all available usage.

Continue across goal turns and context compactions while there is authorized, useful local work. Complete the fixes, documentation, integration, review and package together. Do not finish after proposing a plan, after the first green suite, or after one repository reports success.

When an attempt fails, record the observation, change the hypothesis or implementation using that evidence, and run the relevant check again. Escalate a difficult unresolved defect to a stronger permitted model or focused reviewer. Avoid cycling through the same failing command without new evidence.

If one work item is externally blocked, document the exact dependency and keep independent work moving. Do not ask repeatedly for already-settled product decisions. Ask only for a missing consequential decision/access that cannot be resolved within the authorized scope, and make the dependent action concrete first.

Obey the runtime's goal lifecycle and any user/system pause, interruption or budget limit. Save a truthful checkpoint; do not call unfinished work complete to end a turn or because usage is low. If required local work reaches a genuine impasse, keep it incomplete, record attempts and the smallest needed input, and use the supported blocked workflow only when its conditions are met. External gates explicitly excluded from this local goal may remain open at successful local completion.

Do not implement recurrence, cron, a heartbeat, perpetual polling or a monitoring service to make this goal run longer. The user requested a long-running build goal, not ongoing community automation.

The goal-writing approach follows [official OpenAI guidance on persistent goals](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex): a verifiable outcome with constraints, progress evidence and explicit stopping conditions. This plan adds project-specific execution requirements; it does not promise unlimited unattended runtime.

## 10. Expected commit and review sequence

The following is an example of coherent history, not a rigid count:

1. Hub: adopt continuation plan, baseline, issues and stage tracking.
2. ESP32: fix immutable ACK reuse with repeated-retry regression and required firmware validation.
3. Gateway: fix command routing/discovery with negative MCP coverage.
4. Gateway: isolate event windows with multi-device and lifecycle coverage.
5. Linux: repair the supported custom-factory route and prove installed-wheel onboarding.
6. Hub: persist failed-refresh states with file-to-build regression coverage.
7. Hub: implement safe documentation rendering and correct source-relative navigation; split renderer and integration into tested commits if useful.
8. Components/hub: incorporate independent findings, refresh protocol/doc pins, and record integrated acceptance.
9. Hub: refresh candidate evidence, publication preparation, stage closure and handoff.

Commit test and fix together when a separate red-test commit would make an integrated branch fail. Record the initial failure in evidence. Preserve the meaningful commits at integration; do not squash the complete correction project into one commit.

Independent review must specifically challenge the six acceptance criteria and the claim that the final package contains corrected code. Reviewers should also check that onboarding does not depend on the maintainer's environment and that website success is assessed on actual rendered documentation. Fix material in-scope findings and rerun affected checks. Avoid an unbounded audit of unrelated future features.

## 11. Completion checklist

Mark the local goal complete only when all required items below are supported by evidence:

- [ ] H0–H7 tracking exists and each completed stage has evidence and coherent commit references.
- [ ] All six findings are fixed and their concrete regressions pass; a newer pre-existing fix may count only after reproducing its corrected behavior and recording it.
- [ ] No material in-scope correction/review defect is left hidden behind a green old suite.
- [ ] The complete integrated local suite passes on identified source states, with new regressions in repeatable commands/CI configuration.
- [ ] Corrected C124 firmware compiles and all rebuilt firmware artifacts have accurate provenance/checksums.
- [ ] Linux custom onboarding works from a fresh installed package using the documented commands, with the available real Linux acceptance completed or an explicitly unresolved requirement that prevents overstating completion.
- [ ] Website cache states survive the actual file/build path; documentation links, formatting and diagrams work; desktop/mobile/keyboard/reduced-motion checks are recorded.
- [ ] The existing Home Assistant integration and community dry-run tests still pass, with their verification limits unchanged.
- [ ] Independent review findings have explicit dispositions and required fixes are validated.
- [ ] Issue ledgers, roadmap, documentation snapshots, compatibility records and handoffs agree on status.
- [ ] Final local archives/packages/site outputs contain corrected versions, have verified hashes, and retain complete source histories.
- [ ] The journal covers meaningful stages, failed experiments, fixes and validation; the short checkpoint is current.
- [ ] Implementation changes are committed locally and integrated into the intended `main` branches. Unrelated user files remain preserved and explicitly listed.
- [ ] Actual Grok, mobile, physical hardware, real home devices, systemd/peripherals, independent human testing and public activation retain truthful status.
- [ ] A concrete real-Grok simulator test plan and the remaining access/transport requirements are ready for the next decision.

If a required item cannot be completed, report it as unfinished with evidence and a resumable checkpoint. Do not redefine acceptance after the fact merely to close the goal.

## 12. Final handoff to the user

The last response should state what is now usable, then provide:

1. The six findings and their resolved/unresolved status, with component commit IDs.
2. A short stage summary and links to the journal, review, current checkpoint and final handoff.
3. Tests/builds actually run, relevant environment facts, and any limitations.
4. Exact commands for the corrected simulator, Linux custom example and local website.
5. Final repository HEADs, branch/working-tree status, and the location of verified local artifacts.
6. A clear statement of whether this local correction goal is complete.
7. The next concrete user decision: how to authorize/test the real existing Grok Bot connection, plus the separately pending hardware/publication/community gates.

Do not claim that Grok controls hardware merely because every local stage has passed. Conversely, do not leave the six local fixes unfinished simply because real hardware or account access is still unavailable.

## 13. Compact goal prompt

Paste the following into a new Codex chat attached to `<workspace>/grok-gadgets`:

```text
/goal Complete the Grok Gadgets local correction cycle using docs/hardening-plan.md. Read it fully, the original docs/implementation-plan.md and each repository's AGENTS.md, then execute H0–H7 across the five existing repositories. Fix all six audit findings, add meaningful regressions, verify clean installation and cross-repository behavior, rebuild affected firmware/packages/site, obtain independent review, and refresh the local release candidate.

Keep working across goal turns until the required local acceptance is met; do not stop at a plan or the first passing suite. Use bounded subagents with the plan's approved models. Commit every coherent tested increment on short-lived branches, preserve history, update labeled local issues, and maintain the stage tracker, execution journal and resumable checkpoint throughout. Before accepting each next commit, run checks protecting previous work. Record failures and decisions as well as successes.

Preserve unrelated files, keep the product Grok-exclusive, and obey the existing no-publish/push/deploy/spend/live-account/hardware/automation boundaries. Never open Brave, Safari or Passwords. Complete independent local work while recording external gates honestly. Finish with verified commit/artifact evidence, corrected run instructions, and the concrete next real-Grok test. If required local work is genuinely blocked, report the exact blocker and checkpoint instead of claiming completion.
```
