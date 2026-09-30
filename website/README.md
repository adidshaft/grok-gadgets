# Local website

Run `python3 website/build.py` from the hub, then `python3 -m http.server 4173 --bind 127.0.0.1 --directory website/dist`. Open http://127.0.0.1:4173. No deployment occurs.

Python standard library generates escaped canonical docs and the issue-ledger roadmap. The homepage presents one short pitch and a large continuous SVG architecture scene. Tap or keyboard-select a node for a concise explanation and documentation link. LED and Button views reveal only their relevant simulated controls. Menu opens the documentation, roadmap and community paths; Escape returns focus to its trigger. No framework, remote font or animation library is required.

Original community artwork is copied from the user-approved local brand package. Official Grok and SpaceXAI marks are unchanged product/company references, separate from the community identity. See media/provenance.json and THIRD_PARTY_NOTICES.md for source hashes and trademark conditions. These official assets are not Apache-2.0 licensed project artwork.

Design reference inspected 4 October 2026: https://paradigm.xyz — open composition and broad geometric motion. The projected device architecture and implementation are original. Motion advances at approximately 30 redraws/second and stops when hidden, outside the viewport, explicitly paused, or while the menu is open. OS reduced-motion preference defaults to a static scene; interactions still work. Native buttons, visible focus indicators and a keyboard skip link are included.

The illustration makes no network or hardware requests. Simulated LED/button/disconnect reports do not establish Grok connectivity or physical verification. Both gates remain explicitly pending on the homepage.

Activity is unavailable until public repositories exist. `python3 website/activity.py` is inactive by default. After public-owner approval only, `--live --owner OWNER` writes timestamped cached JSON using an optional server-side GITHUB_TOKEN environment variable. `GROK_ACTIVITY_FILE=website/activity-fixture.json python3 website/build.py` exercises explicitly synthetic activity; omit the variable to return to unavailable. Counts and release text are validated/escaped. No live fetch has been performed.

Verification: docs/verification/website-redesign.md records desktop/mobile, actual animation samples, keyboard, offline controls and build/test checks. Earlier website.md and screenshots retain the initial alpha design evidence.
