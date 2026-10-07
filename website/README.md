# Static website

From the hub, run `python3 scripts/dev.py setup`, then `python3 scripts/dev.py site`. Open http://127.0.0.1:4173. The public site is at `https://grokgadgets.org/`. These commands build a local preview; they do not deploy it.

Pinned markdown-it-py renders safe canonical docs and the issue-ledger roadmap. The homepage opens on a wireframe motion canvas with a centered identity, a short Grok Bot description, a separate Devices / Connections / Workbench / Roadmap scene selector, Start building and Explore. Light, Sensor, Display and Home stay inside the Devices scene. Connections places the supplied Grok Bot mark among meaningful platform routes: ESP32, Linux/Raspberry Pi and Home Assistant. Workbench illustrates LED commands, button events and USB availability on a conceptual C124 gadget. Roadmap presents selectable evidence gates with links to the canonical documentation. Explore opens a native dialog containing connection status, simulated light controls, a collapsible customization workbench and three builder paths. Existing `#scene-demo`, `#playground`, `#builder-paths` and `#components` links reveal their destination in the dialog. The homepage has no activity statistics, release list or repository directory. The separate Project components page holds the ten-item inventory. Documentation exposes simulator, ESP32, Linux/Raspberry Pi and Home Assistant paths directly. Menu opens the docs, roadmap and community paths; Escape closes the dialog and restores focus. The footer and menu credit @adidshaft with a link to the X profile. No framework, remote font or animation library is required.

Original community artwork is copied from the user-approved local brand package. Official Grok and SpaceXAI marks are unchanged product/company references, separate from the community identity. See media/provenance.json and THIRD_PARTY_NOTICES.md for source hashes and trademark conditions. These official assets are not Apache-2.0 licensed project artwork.

Design reference inspected 4 October 2026: https://paradigm.xyz — open composition and broad geometric motion. The projected device architecture and implementation are original. Subtle projected movement and conceptual route packets loop at approximately 30 redraws/second. Inactive scenes stop their animation. Motion stops when the page is hidden, the scene is outside the viewport, the user pauses it, or the menu or Explore dialog is open. The user’s pause choice survives closing a dialog. OS reduced-motion preference keeps the scene static; interactions still work. Native buttons, visible focus indicators and a keyboard skip link are included.

The illustration makes no network or hardware requests. Its routes are conceptual. Simulated LED/button/disconnect reports do not establish Grok connectivity or physical verification. The Explore dialog identifies Grok Bot and hardware connection tests as pending and links to the support matrix. The simulator page shows the local gateway rehearsal; it establishes software simulation only. The Bot mark is a redraw based on the reference supplied by the project owner; it is not an official asset provenance claim.

The deployment workflow refreshes public repository activity. Local `python3 website/activity.py` makes no live request by default. `--live --owner OWNER` writes timestamped JSON and can use a server-side GITHUB_TOKEN. To test synthetic data, run `GROK_ACTIVITY_FILE=website/activity-fixture.json .venv/bin/python website/build.py`. Without that override, the build uses the configured public snapshot. Counts and release text are validated and escaped.

Historical verification: docs/verification/website-redesign.md records desktop/mobile, animation, keyboard, offline controls and build/test checks for an earlier layout. Earlier website.md and screenshots retain the initial alpha design evidence. These records do not verify the current canvas and Explore dialog redesign; the initial canvas review is recorded in docs/verification/website-canvas-2026-10-06.md.

Public documents are explicitly selected in website/documents.json. Host logs, raw verification journals and machine inventories are omitted. Source-relative component links use compatibility/documentation-sources.json; unmirrored tracked files have verified checkout instructions on source-reference.html. Raw HTML and unsafe URL schemes are disabled. Supported acyclic Mermaid flowcharts generate bounded accessible static SVG, without remote scripts or runtime callbacks. Unsupported diagrams fail the build. The fixed generated website/dist directory is replaced on each build; unrelated files outside it are preserved.

A live cache is fresh for less than one hour (the refresh throttle). Builds classify older live records as cached even if a refresh never ran; future timestamps and incomplete/corrupt records become unavailable. Failed refreshes atomically persist the same validated cached/unavailable result they report.

## Hosting and refreshes

This section describes static website hosting. It does not describe a gadget gateway service. The site runs no MCP endpoint or device tunnel. See the canonical [hosting and remote access FAQ](../docs/getting-started/hosting.md) for gateway operators, tunnel ownership and future product hosting choices.

The hub repository is the website source. `.github/workflows/pages.yml` deploys via Cloudflare Pages Direct Upload only after the exact main commit passes both `Hub checks` and `Integrated acceptance`. The build validates the complete GitHub issue snapshot, the bounded cross-repository activity data, all website tests, the project-root/deep-link check and the simulator kit before upload. The Cloudflare Pages token is held by the protected `cloudflare-pages-production` GitHub environment and is visible only to the final deploy job.

Successful main deployments refresh issues and activity across the five `adidshaft` repositories. A daily run at 06:17 UTC (11:47 IST) refreshes activity such as star counts that has no dependable event trigger. If the issue snapshot cannot be fully refreshed, deployment stops and the prior site remains live. Activity failures show timestamped cached or unavailable data. Neither snapshot refresh changes tested component pins or commits generated data back to `main`.

For a local rehearsal, set `GROK_GADGETS_PUBLIC_SITE` to the intended HTTPS site root before running `website/build.py` and `scripts/check-pages-prefix.py`; the default is `https://grokgadgets.org/`.

The customization workbench inside the homepage Explore dialog shares a strict configuration format with the gateway simulator. Customize a name/ID, starting RGB/brightness, response delay and offline startup, then export JSON. Browser controls are local simulation. The inspectable downloadable kit contains exact source, wheel, hashed dependencies and license notices; setup is in docs/getting-started/simulator-kit.md.

Each website build validates kit source/input freshness and acceptance before replacing the previous preview. With a clean sibling gateway checkout, stale inputs trigger source tests and fresh installed MCP acceptance before the new download is copied. Without it, only the included kit matching the compatibility pin is accepted. `python3 scripts/build-simulator-kit.py --check`, `python3 scripts/test_simulator_kit.py` and `node --test website/test_simulator.cjs` verify the download/model. The Cloudflare Pages publication workflow runs these gates before deployment. See docs/verification/simulator-playground.md.

## Documentation navigation

`docs_navigation.py` assigns each published document to one task-based section. Linux and ESP32 guides have separate subgroups under Build a gadget. Community maintenance drafts and verification records stay outside the starting path.

To add a document, register it in `documents.json` and the navigation taxonomy. The build rejects missing or duplicate entries. Keep existing page URLs stable when moving a guide between sections.

Each article has breadcrumbs, a local navigation menu, a heading list and previous/next links within its subgroup. Native disclosure controls work without JavaScript. `docs.js` collapses the outer menu on narrow screens. The active subgroup stays open.

Run `.venv/bin/python -m unittest discover -s website -p 'test_*.py'`, build the site, and inspect desktop, narrow-screen and keyboard navigation before publishing a navigation change.
