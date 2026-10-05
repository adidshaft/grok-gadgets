# HUB-WEB-001 — Source-driven website and local visual verification

Owner: grok-gadgets

Stage: done · M7

Labels: feature, website, P1

Intended behaviour: Source-driven website and local visual verification

Acceptance:

- Documented commands reproduce observed behaviour
- Evidence identifies actual verification level

Dependencies: HUB-001

Commits: 7c76969, 48cadc5

Evidence:

- 27-page static build/link checks
- 3 activity tests, fixture escape check, desktop/mobile visual check, keyboard/reduced-motion browser checks
- Final browser review fixed scroll-dependent Menu pointer interception by isolating scene layers; pointer open/close and Escape focus restoration verified at desktop1265px and narrow375px; LED green still works. Screens and exact final source are in the approval packet.

Blocker: None
