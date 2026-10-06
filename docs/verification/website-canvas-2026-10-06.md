# Website canvas review — 6 October 2026

Issue: HUB-WEB-006 / #104.

The owner requested a quiet, motion-first homepage using Paradigm's open canvas as the visual reference. The homepage now shows centered branding, a concise purpose, the complete device illustration, four scene selectors, Start building and Explore. Statistics, release lists and the large headline are removed from the opening screen. The native Explore dialog contains the simulator controls and customization. The proof recording is on the simulator page.

## Browser evidence

Reviewed with the Codex in-app Chromium browser on the local generated site:

| CSS viewport | Result |
| --- | --- |
| 1440 × 900 | Complete illustration; page dimensions equal viewport; no fixed footer over content |
| 1280 × 600 | Complete illustration; page dimensions equal viewport after correcting the short-screen height calculation |
| 1024 × 768 | Complete illustration; page dimensions equal viewport |
| 768 × 1024 | Tablet portrait composition; page dimensions equal viewport |
| 390 × 844 | Complete phone composition; page dimensions equal viewport; all five node bounds inside the stage |
| 844 × 390 and 667 × 375 | Landscape-phone canvas, toolbar and footer fit entirely; page dimensions equal viewport |
| 320 × 568 | Small-phone composition; page dimensions equal viewport; no wrapped primary action or cropped artwork |

Local screenshots are saved under the ignored `artifacts/design-review/` directory. Browser viewport overrides were reset after review. These are browser viewport checks, not physical mobile-device verification.

The Explore panel at 320px had equal client and scroll widths (263px). The green LED control updated the simulated status. Escape closed the dialog and returned focus to Explore. Motion stopped while the dialog was open. Direct `index.html#playground` navigation opened the dialog and customization disclosure, scrolled to its target, and held the animation phase at 0.000 across separate observations.

The pause control held the animation at phase 0.024 across observations; after resume it advanced to 9.450. The same motion controller retains the system reduced-motion preference, page visibility, menu and offscreen gates. System preference behavior was reviewed in source; no physical OS preference change was made during this audit.

The relocated simulator recording was reviewed at 390px. Its rendered width was 327px inside a 375px document client width, with no horizontal overflow.

## Repository checks

`python3 scripts/check.py` passed: browser simulator, simulator kit freshness and tests, script tests, community tests, 30 website tests, 66-page build, source-archive build, URL prefix, plain-language checks, lint and formatting.

No native Grok Bot connection, physical device operation, or real-home verification is established by this website work.
