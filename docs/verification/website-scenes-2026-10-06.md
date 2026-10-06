# Interactive website scenes — 6 October 2026

Issue: HUB-WEB-007 / #106.

Three bounded GPT-6 Astra Max subagents implemented the Roadmap and Signal scenes and audited website links. The parent integrated them with the existing Devices scene. Light, Sensor, Display and Home remain device-route choices, separate from the scene selector. The footer and menu credit the owner with a link to https://x.com/adidshaft.

## Interaction and visual review

The in-app Chromium browser was used with CSS viewports 1440×900, 1280×600, 768×1024, 667×375 and 320×568. The page matched the viewport dimensions, with the illustration, scene selector, primary actions and footer visible. All three scenes were inspected on the smallest phone size. Roadmap details for software, Grok Bot and C124 hardware were exercised. These are browser checks, not physical device testing.

- Roadmap buttons and arrow keys select the milestone and update its concise status, explanation and documentation link.
- Gallery arrow navigation starts from the focused button, even when it differs from the selected scene.
- Pause held Roadmap at phase 31.824 across observations. The inactive Devices scene remained at phase 11.558. Pause persisted when switching to Signal.
- With motion paused, selecting Sensor produced the accessible message “Reading returns in this local illustration. No Grok Bot or hardware connection.”
- The 320px menu has equal client and scroll widths (304px), without horizontal overflow.
- The browser reported no JavaScript errors during the final review.
- System reduced-motion, document visibility and cleanup behavior were reviewed in source; no OS preference change was performed.

Screenshots are in ignored `artifacts/design-review/`. CSS and JavaScript links carry content fingerprints so repeat visitors receive changed assets.

## Link audit

The final 66-page generated site has 4,043 local references, including 332 fragment links. All resolve. Fourteen dynamic JavaScript destinations also resolve; there are no duplicate HTML IDs. All 65 sitemap entries and the robots/sitemap URLs passed.

For 234 HTTPS URL variants, the audit made 231 distinct requests: 223 returned expected content, four GitHub action destinations required sign-in, one was the intentional error document, and three Reddit destinations limited direct verification. There were no confirmed broken links, HTTP 404/410 responses, network errors or missing external anchors. The X profile returned HTTP 200 with the expected owner identity. Email deliverability and signed-in GitHub actions were not exercised.

The Reddit welcome-post crawl predates the approval recorded in community/reddit-setup.md; current browser access is blocked. Its current visibility remains unresolved. The historical link was preserved; normal community navigation already points to the subreddit root. Reddit was not modified.

Full raw evidence is local and ignored under `artifacts/link-audit/`.

## Verification limits

All motion scenes are local illustrations. The roadmap derives its labels from the current support matrix and verification guidance. It does not claim native Grok Bot invocation, physical hardware success or independently reproduced installation. No invented completion dates or percentages are shown.

## Repository checks

`python3 scripts/check.py` passed, including website tests, build/link validation, ZIP source build, public URL prefix, simulator checks, lint and formatting. New module JavaScript syntax checks passed. The first ZIP check identified the new assets had not yet been added to Git's index; after including them, the complete check suite passed.
