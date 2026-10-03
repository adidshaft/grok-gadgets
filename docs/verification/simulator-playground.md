# Configurable simulator acceptance

Local, unpublished acceptance. Gateway source `fa062a1db36cfbea90b807b9430d28d153bf585d` includes configurable simulation and offline button guards. The browser reuses the existing architecture animation; no Grok requests or physical operations occur in the browser.

## Automated checks

- `node --test website/test_simulator.cjs`: five tests passed. Strict config validation, command rejection without state changes, offline/button ordering, reconnect, bounded delay/concurrent calls, reset cancellation and detached snapshots.
- `python3 scripts/test_simulator_kit.py`: three tests passed. Actual downloadable ZIP/verifier, malformed inventory/version/source, tampering, traversal/symlinks, stale inputs/source, rejected dirty checkout, refresh failure, malformed manifest and standalone pinned checkout.
- Website suite: 12 tests passed. Publication suite: 11 tests passed. Ruff check and formatting passed. Final website build checks 50 page/link/fragment targets.
- Kit generator runs 73 gateway tests on an exact committed archive, builds its wheel/sdist, installs the readable kit into a fresh virtual environment and runs the official MCP demonstration with both default and custom/offline settings. All passed before archive replacement. Gateway agent additionally reported 52 installed configuration tests passing; gateway evidence is in its `docs/verification/simulator-config.md`.
- Original ZIP SHA-256 at 3266a05: `214cf7c37b69014b459d5c3fd11cc48d5cfd0623e10e51e39d5900b1a7794a8b`. This matches the file actually downloaded through the website. The separate website manifest records every file hash, build input and source commit.

## Browser and extracted kit

Tested in the Codex in-app browser at 1280×800 and 390×844. The mobile document has no horizontal overflow (390 viewport / 375 document). Native disclosures opened and closed with Enter. Whitespace-only names were rejected without replacing simulator state. LED controls visibly changed state; resetting clears prior session reports. Pause produced identical frame 938 across observations; resume advances motion. Existing offscreen/hidden/menu/reduced-motion handling is retained. No browser console errors were recorded.

The original config-content test manually used a separate custom filename; it did not catch the automatic export filename collision. That onboarding claim is superseded by HARD-SIM-EXPORT-001 and [corrected actual browser-to-kit acceptance](simulator-export-onboarding.md).

The browser exported `studio-light` / `Studio light`, RGB 26/51/128 on, delay 250 ms and offline startup. This exact export was validated and used by a clean extracted kit's real local stdio MCP demonstration: discovery name/ID/initial state, offline rejection, reconnect, blue execution/status/state, ordered injected button edges, LED off and physical=false assertions passed. The default demonstration also passed. The JSON download and clipboard copy matched the displayed export.

The manual clean kit acceptance used native Apple Silicon Python 3.11.15. A preliminary Intel Python 3.13 installation encountered a dependency source-build/toolchain failure. The installer now requires hash-pinned binary wheels and isolated pip; it refuses source builds and existing virtual environments. Windows and Intel Mac installs remain unverified. A nonfatal pinned upstream Pydantic lifespan annotation warning was observed; MCP assertions passed.

Ignored local proof files: `artifacts/verification/playground-desktop.png`, `playground-mobile.png`, `playground-customization.png`; extracted run logs in `artifacts/simulator-kit-final-acceptance/`. No credentials or environments enter the downloadable archive.

## Freshness and publication gates

Every website build validates the gateway commit, generator/template/guide fingerprints, acceptance record, ZIP inventory and file hashes. A committed source or input change triggers a tested rebuild when the sibling gateway is present. Dirty gateway source stops the build. A failed refresh preserves the last successful preview but exits unsuccessfully; publication must honor that exit. Without the gateway checkout, the checked-in kit must match the compatibility pin. Prepared CI performs the same freshness check and simulator regression tests.

This is automatic on local builds, not a deployed update service. Public repositories, cross-repository CI triggers and deployment still need explicit approval and activation. Downloaded copies are immutable snapshots. Updated downloads must be distributed through the gated website build; no hidden self-update occurs.

The configurable kit has not been run inside Grok. Earlier dedicated-Bot operation was Bot-reported on an earlier build; independently inspectable invocation receipts and mobile Grok verification remain pending. AtomS3 Lite C124 compilation evidence is separate; hardware is unavailable and physical verification remains false. No public push, deployment, paid service or Reddit modification occurred.
