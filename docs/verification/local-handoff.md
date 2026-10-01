# Local alpha handoff — 4 October 2026

The independently achievable local alpha is complete. It is exclusively for Grok and remains unpublished. Actual existing Grok Bot use, physical hardware and independent reproduction are not verified.

## Repositories and verification

| Repository | Tested implementation commit | Observed evidence |
| --- | --- | --- |
| `/path/to/grok-gadgets` | `72c9d6ed` | Hub checks,48-page link build,3activity tests,6recognition tests,desktop/narrow/keyboard/motion review |
| `/path/to/grok-gadgets-gateway` | `4cf42fff` | 13 tests; official stdio MCP demo; authenticated TCP/USB PTY |
| `/path/to/grok-gadgets-linux-sdk` | `256a07e2` | 15 tests macOS and Linux installed wheel/CLI; actual gateway TCP |
| `/path/to/grok-gadgets-esp32-sdk` | `585adda7` | 3 CTest suites; canonical frames; actual consumer PTY incl overflow/restart/revocation; ESP32-S3 compile |
| `/path/to/grok-gadgets-home-assistant` | `a8b2370b` | 13tests incl loopback HTTP official MCP client; clean wheel; no actions |

Full commit histories are in publication/commit-summary.md. All repositories have Apache-2.0 original code, contribution foundations, pinned toolchains/dependencies where needed, feature-branch commits and local issue records. Canonical shared policies live in hub. Component docs are pinned by commit/hash in compatibility/documentation-sources.json.

## Start locally

From the hub:

```sh
python3 scripts/check-all.py
python3 website/build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory website/dist
```

Website: http://127.0.0.1:4173. Run gateway demo in another terminal:

```sh
cd /path/to/grok-gadgets-gateway
uv sync --locked
uv run python -m grok_gadgets_gateway.demo
```

Normal MCP server: `uv run grok-gadgets-gateway --simulator`. Simulator test controls require `--test-controls`; absent by default. The demo uses an actual official MCP ClientSession over stdio and asserts discovery, colour/off, button edges, disconnect/offline error, reconnect and honest simulation flags. This is not actual Grok connectivity.

Linux software example, service template and credential setup: sibling Linux README/docs/operation.md. HA diagnostics: `uv sync --frozen`, then `uv run ha-probe --fixture fixtures/assist.json` in its repository. C124 build: sibling ESP README/docs/build-flash.md; `.venv/bin/pio run -e atoms3-lite-usb`. Do not flash until hardware and authorization are available.

## Evidence and artifacts

Coordinator reran gateway13, Linux15, HA13 tests plus ESP3CTest, schema/frame and actual-consumer USB PTY integration, hub/activity/community/build checks. Retained check logs and machine results: artifacts/verification/. Linux Docker acceptance independently rerun by coordinator against installed wheel with no networking or published ports. Environment: aarch64 kernel6.10.14-linuxkit, CPython3.11.17 and pinned official image in compatibility manifest. This is container runtime evidence; physical peripherals and systemd host lifecycle remain pending.

ESP32 cross-compilation passed: RAM54,628bytes, program flash276,113bytes. Final firmware binary276,480bytes, SHA256 `de12327c4fdc7ef6a728c5841a81d844257012d558c71ecd4fe331c6708af709`. Path: `/path/to/grok-gadgets-esp32-sdk/artifacts/c124-usb/firmware.bin`; ELF/bootloader/partition source provenance/checksums in manifest.json. Pins: RGBGPIO35; active-low buttonGPIO41. No electrical/USB-enumeration observation was made.

Independent Astra review found an overflow reconnect loop, fixed in ESP74085a9. A20-edge host test reports16 ordered events and4lost, preserves session, then executes another command. Reviewer independently reran the integration and confirmed resolution. Explicit reduced motion now disables both animation and smooth scrolling. Screenshots: website-desktop.jpg, website-mobile.jpg.

Gateway emitted one known third-party annotation warning on stderr; assertions pass. Component evidence details document this. No success claim is based only on printed PASS.

## Backlog, community and publication

Main coordination ledger planning/issues.json, exported issue files, milestones and component ledgers remain labeled. Publication/issue-migration.json prepares35records without contacting GitHub. Local-to-public numbers are null pending owner/approval. M0–M4, M6–M7 and M9 preparation are complete at their stated local evidence levels; M5/M8 and external activation remain open.

Community package includes guidelines, recognition/moderation policies, Reddit audit/before-after procedure, proposed flairs/menu/pins, and four unpublished post drafts. Six tests cover offline recognition, consent/ownership/merged contribution checks, higher role preservation, account changes, redacted dry-run logs and bounded idempotent retries. It is no live identity verifier/backend or activated award service.

Publication/README.md, desired-protections.json, labels.json, issue-migration.json, release-notes.md and website-deployment.md specify concrete inactive settings and proposed0.1.0-alpha.1 release. `python3 scripts/package-local.py` generates ignored artifacts/publication source archives with complete commit lists, wheels/sdists, C124 output, static website archive, manifest andSHA256SUMS. `python3 scripts/audit.py` prepares a redacted tracked-files and reachable-Git-history heuristic secret/license inventory. No remotes, pushes, public repos, paid calls, deployment or Reddit changes occurred.

## Remaining external gates

1. Existing Grok account/extension access and approved authenticated reachable route. Standard local MCP is ready, but remote HTTPS service/OAuth is not implemented. Cloud-command routing cannot reach a local Mac path. Record actual tool calls/client versions for desktop/mobile; arbitrary event-triggered Bot wake remains unestablished.
2. Physical C124/data cable, authorized flashing, visible LED and button observations, USB enumeration/disconnect/reboot acceptance. Wi-Fi needs a separately designed authenticated/provisioned transport; do not expose the loopback-only raw device protocol on LAN.
3. Actual Home Assistant installation and deliberately selected exposed entities; safe real Bot actions and physical observations. Upstream MCP notifications are unsupported.
4. Real Linux systemd host lifecycle and physical peripherals/USB serial permissions, beyond tested container software runtime.
5. Second person independent installation/test report.
6. GitHub owner and separate repo creation/push/package/prerelease/site approval; private security contact and actual maintainers; hosted CI/protections then need verification. Binary redistribution needs LGPL dependency source/license/relinking review (Arduino/NeoPixel) before uploading firmware.
7. Logged-in Reddit moderator audit, approved exact changes/posts, developer access/scopes/external-domain approvals, and separately reviewed private identity/runtime/deletion operations before live recognition.

The source assets/grok-gadgets-brand-v1 folder and zip remain preserved and untracked. The user subsequently approved website use; selected original icon/logo copies and unchanged official reference marks now live in website/media with provenance and third-party notices. See website-redesign.md for the additional UI verification. The entire source brand archive remains excluded from Git source archives; public naming/press-brand review remains a publication gate.
