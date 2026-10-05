# WEB-CLARITY-001 — Homepage paths and finite scene motion

Local acceptance record for the website hierarchy, simulator entry point and conceptual motion story.

## Changes

- Named the product target as the user's existing Grok Bot and put local-alpha, Grok and hardware verification limits beside the hero actions.
- Added direct simulator and ESP32, Linux/Raspberry Pi and Home Assistant paths. Kept the ten-component inventory at `components.html` and exposed it from the homepage and docs index.
- Added cached/live/unavailable activity state, refresh time, definitions and links to all five public source repositories.
- Replaced independent looping route packets with one selectable Light, Sensor, Pi display or Home Assistant route. Each route makes one 3.3-second conceptual pass, then holds; Replay does not reset simulator state.
- Redrew the supplied Grok Bot round-face reference as `website/media/grok-bot-mark.svg`; documented its source as a user reference, not an official asset.
- Centralized motion availability across user pause, OS reduced-motion, open menu, hidden document and offscreen scene. Scene geometry is cached outside the animation frames; control widths are read together before positioning writes.
- Retained the last reported simulated LED color on disconnect and announce that current output is unknown. Offline commands remain unconfirmed and do not change state.

## Verification

Local checks on 2026-10-05:

- `./.venv/bin/python -m unittest discover -s website -p 'test_*.py'`: 29 tests passed.
- `./.venv/bin/python website/build.py`: built and link/fragment-checked 64 static pages.
- `./.venv/bin/python scripts/check-archive-build.py`: source-archive build and website tests passed without Git metadata.
- `./.venv/bin/python scripts/check-pages-prefix.py`: all 64 pages and 4,648 local links resolved under the production URL prefix.
- Ruff lint/format, `node --check` for both scene and motion scripts, and `git diff --check` passed.
- Refreshed the local homepage in an in-app browser at its available 576px-wide viewport. Grok Bot mark, pending-verification copy, all four story choices, Replay, simulator controls, disconnect state, and fixed footer rendered. Responsive checks at 360px, 768px, 1440px and 200% zoom were not available through this browser surface.
- In the browser, selected Home Assistant and verified its route copy/link; selected green and verified only simulated LED state changed; pressed the simulated button and observed two press/release events; disconnected and verified the page preserved the last reported color while stating current output is unknown.
- `python3 scripts/check.py`: browser simulator, community, website tests, website build, archive build, public URL prefix, lint and format passed. Simulator kit freshness failed because its pin is gateway `f807c536` while the sibling gateway checkout is at `1f03319a`; the simulator-kit test suite and aggregate script tests each had the same two gateway-dependent errors. No kit refresh was made against an unmerged dependency.

GitHub integration remains pending: PR #51 and the relevant gateway, Linux, ESP32 and Home Assistant PRs have not merged, so this feature branch has not been integrated into current `main` or deployed. No Grok Bot or physical-device calls were made. A CPU-throttled DevTools performance trace was unavailable in this environment; no performance score is claimed.
