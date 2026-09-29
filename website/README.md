# Local static website

Run `python3 website/build.py` from the hub, then `python3 -m http.server 4173 --bind 127.0.0.1 --directory website/dist`. Open http://127.0.0.1:4173. No deployment occurs.

Python standard library generates escaped canonical docs and issue-ledger roadmap. No browser credentials or token required. Activity is explicitly unavailable until public repositories exist. No copied assets or remote fonts. Original geometric C124 schematic; Georgia/Verdana/monospace fallback typography.

Design reference inspected 4 October 2026: https://www.paradigm.xyz/ — sparse serif wordmark, large negative space, fine geometric diagrams, restrained motion. This implementation uses its own olive palette, device illustration, navigation, and content. Reduced-motion CSS disables animation. Keyboard skip link and visible focus indicators are included.

Activity refresh remains inactive by default: `python3 website/activity.py`. After public-owner approval only, `--live --owner OWNER` writes timestamped cached JSON using an optional server-side GITHUB_TOKEN environment variable. `GROK_ACTIVITY_FILE=website/activity-fixture.json python3 website/build.py` exercises explicitly synthetic activity rendering; omit the variable to return to unavailable. Counts and release text are validated/escaped. No live fetch has been performed.

The explicit Reduce motion control complements the OS media query and reports its pressed state. Desktop and 390px viewport were checked with the in-app browser; evidence is in docs/verification.
