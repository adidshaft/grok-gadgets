# REVIEW-DEV-001 — developer handoff review

Date: 5 October 2026. Scope: the five public-lineage `simplify-and-fix` branches.
This is a local software review. No push, deployment, tunnel, Grok Bot session,
physical device action or Reddit change was performed.

## Verdict

The local alpha follows the intended product: reusable ESP32 and Linux SDKs,
a gateway for the existing Grok Bot, and reuse of Home Assistant's own MCP server.
The C124 is an example, not the SDK boundary. The separate generic ESP32-S3 example
also compiles. No other model backend was added.

The branches are ready for a later authorized source push and PR review. They are
not a verified Grok Bot hardware product. Publish component commits before the hub,
which refers to those exact commits. Keep the individual commits. Hosted CI must
pass before merge; this review did not run the new commits on GitHub.

## Changes made in this review

- Rejected device-supplied schema regular expressions before evaluation. Documented
  the supported alternatives in both SDK guides.
- Preserved command retry protection when its cache is full. New work returns
  `busy` rather than evicting IDs still inside the retry window. This is not a
  durable exactly-once guarantee.
- Added a real local CLI/HTTP test for init, enrollment, discovery, commands,
  duplicate receipts, device revocation, token rotation and process shutdown.
- Tested the Linux README's exact gadget factory after a fresh source installation.
  Fixed source-install commands, init-before-serve order, client setup and token
  recovery. Ignored the user's `my_gadget.py` example.
- Shortened first steps and corrected HTTP, USB recovery, button-event and Grok Bot
  claims across the READMEs and website. Kept the visual design, motion and exact
  hero, “Grok, meet the real world.”
- Separated the simulator ZIP's short bundled README from the website guide.
  Website prose changes no longer require a new ZIP. Bundled changes still do.
  Rebuilt and verified the kit, source imports and component pins.
- Supplied Ruff in the integration workflow and restored explicit candidate-kit
  rebuilding in its disposable checkout. Normal website builds only verify the kit.
- Removed 36 automated co-author trailers from unpublished history. All 52 affected
  commit trees and commit counts were preserved. Active history contains no agent
  author, committer or co-author identity. Published base commits and Git config
  were unchanged. Current commits use the owner's GitHub noreply identity.

## Checks and evidence

| Check | Result |
| --- | --- |
| `python3 scripts/check.py` | All hub checks passed, including ZIP-only site build, kit freshness, browser tests, script/community/website tests and lint/format |
| `.venv/bin/python scripts/check-all.py` | All 14 groups passed; local run `20261005T144245-1791211365451578000` |
| Gateway: `uv run pytest -q` | 126 passed on each of Python 3.11, 3.12, 3.13 and 3.14 |
| Gateway: Ruff and `uv build` | Passed |
| Linux: frozen sync, Ruff, unittest with `GROK_GATEWAY_SOURCE`, `uv build` | 41 tests passed, including seven gateway cases; wheel and sdist built |
| Fresh Linux README setup | Authenticated HTTP discovery, `lamp.set`, reported state and clean SIGTERM passed; logs contained no credentials |
| Home Assistant: frozen sync, Ruff, unittest, `uv build`, fixture probe | 26 tests passed; fixture made zero tool calls and zero resource reads |
| ESP32: `sh tools/check.sh` | Four host suites passed |
| ESP32: `.venv/bin/python tools/check_contract.py` | Actual host-executed sketches emitted 129 C124 and 130 generic valid frames; protocol hashes matched |
| ESP32: gateway Python running `tools/check_gateway.py` | Simulated firmware/PTY/USB bridge/gateway, duplicate ACKs, event overflow, restart and revocation passed |
| ESP32: `.venv/bin/pio run -e atoms3-lite-usb -e esp32s3-led-button` | Both firmware examples compiled; neither was flashed |
| Browser review of local site | Hero/design preserved; simulator path, nested SDK navigation and Linux quickstart checked; no browser warning/error logs observed |
| Metadata and compatibility audit | Public bases retained; rewritten trees identical; current four component pins match clean checkouts; public commit-email check passed |

The full integration record is local ignored output under `artifacts/verification/`.
It records the hub's pre-commit changes and clean component commits. The final hub
check also runs before this review is committed. These records do not establish
independent human reproduction, Linux peripherals, systemd or Grok Bot execution.

The gateway tests emit one known upstream Pydantic settings warning. The pinned
MCP library can also log `ClosedResourceError` when its optional SSE stream closes.
The CLI test checks actual process exit, connection behavior and credential leakage;
it does not mistake that upstream log for a failed command.

The simulator archive SHA-256 is
`7c8a775f321cd1aa0f9018e6e0f99b1438809c7533f4846a4499bdfe8d57bf34`.
Its gateway source is `a02e8889f3936031040a67644112076e140954b1`.
See `compatibility/tested-components.json` for the component commits. Its firmware
object remains an older unpublished build; it was not relabeled as the new build.

## Deliberate deferrals

| Item | Reason and next gate |
| --- | --- |
| Real Grok Bot, mobile, tunnel, TLS/OAuth, relay, Wi-Fi and pairing | Later product work and separately approved account/network activation; `HARD-GROK-REMOTE-001` stays blocked |
| Physical C124, USB buffer behavior, LED/button and power recovery | Needs the board and physical observation |
| Linux systemd/peripherals and real Home Assistant | Needs the selected operating environment and devices; no new container or real-home run claimed |
| Mutual authentication, boot-ID guarantees and protocol request IDs | Documented limits; no protocol 0.2 redesign in this pass |
| Name, marks and old public private-email commits | Owner already deferred these decisions; no published-history rewrite |
| GitHub settings, PR #45, deployment, Reddit and old private checkouts | Outside this local review; left unchanged |

The next product test is a bounded Grok Bot-to-local-simulator experiment through
an approved authenticated route. Confirm server logs and observed tool results.
After the board arrives, repeat the path with real LED/button and recovery checks.
`grok_verified`, `hardware_verified` and `independently_reproduced` remain false.
