# Static website

Create the hub environment with `uv venv .venv --python 3.13` and `uv pip install --python .venv/bin/python -r website/requirements.txt`. Run `.venv/bin/python website/build.py` from the hub, then `python3 -m http.server 4173 --bind 127.0.0.1 --directory website/dist`. Open http://127.0.0.1:4173. The free public host is Cloudflare Pages at `https://grok-gadgets.pages.dev/`; HTTPS and key routes were verified on 5 October 2026. The project doesn't own a custom domain.

Pinned markdown-it-py renders safe canonical docs and the issue-ledger roadmap. The homepage presents one short pitch and a large continuous SVG architecture scene. Tap or keyboard-select a node for a concise explanation and documentation link. LED and Button views reveal only their relevant simulated controls. Menu opens the documentation, roadmap and community paths; Escape returns focus to its trigger. Below the scene, ten native disclosure entries list every SDK, connection and project tool. Each opens a short description, verification state, docs links and relevant commands; they remain interactive without JavaScript. No framework, remote font or animation library is required.

Original community artwork is copied from the user-approved local brand package. Official Grok and SpaceXAI marks are unchanged product/company references, separate from the community identity. See media/provenance.json and THIRD_PARTY_NOTICES.md for source hashes and trademark conditions. These official assets are not Apache-2.0 licensed project artwork.

Design reference inspected 4 October 2026: https://paradigm.xyz — open composition and broad geometric motion. The projected device architecture and implementation are original. Motion advances at approximately 30 redraws/second and stops when hidden, outside the viewport, explicitly paused, or while the menu is open. OS reduced-motion preference defaults to a static scene; interactions still work. Native buttons, visible focus indicators and a keyboard skip link are included.

The illustration makes no network or hardware requests. Simulated LED/button/disconnect reports do not establish Grok connectivity or physical verification. Both gates remain explicitly pending on the homepage.

The deployment workflow refreshes public repository activity. Local `python3 website/activity.py` makes no live request by default. `--live --owner OWNER` writes timestamped JSON and can use a server-side GITHUB_TOKEN. To test synthetic data, run `GROK_ACTIVITY_FILE=website/activity-fixture.json .venv/bin/python website/build.py`. Without that override, the build uses the configured public snapshot. Counts and release text are validated and escaped.

Verification: docs/verification/website-redesign.md records desktop/mobile, actual animation samples, keyboard, offline controls and build/test checks. Earlier website.md and screenshots retain the initial alpha design evidence.

Public documents are explicitly selected in website/documents.json. Host logs, raw verification journals and machine inventories are omitted. Source-relative component links use compatibility/documentation-sources.json; unmirrored tracked files have verified checkout instructions on source-reference.html. Raw HTML and unsafe URL schemes are disabled. Supported acyclic Mermaid flowcharts generate bounded accessible static SVG, without remote scripts or runtime callbacks. Unsupported diagrams fail the build. The fixed generated website/dist directory is replaced on each build; unrelated files outside it are preserved.

A live cache is fresh for less than one hour (the refresh throttle). Builds classify older live records as cached even if a refresh never ran; future timestamps and incomplete/corrupt records become unavailable. Failed refreshes atomically persist the same validated cached/unavailable result they report.

## Hosting and refreshes

This section describes static website hosting. It does not describe a gadget gateway service. The site runs no MCP endpoint or device tunnel. See the canonical [hosting and remote access FAQ](../docs/getting-started/hosting.md) for gateway operators, tunnel ownership and future product hosting choices.

The hub repository is the website source. `.github/workflows/pages.yml` deploys via Cloudflare Pages Direct Upload only after the exact main commit passes both `Hub checks` and `Integrated acceptance`. The build validates the complete GitHub issue snapshot, the bounded cross-repository activity data, all website tests, the project-root/deep-link check and the simulator kit before upload. The Cloudflare Pages token is held by the protected `cloudflare-pages-production` GitHub environment and is visible only to the final deploy job.

Successful main deployments refresh issues and activity across the five `adidshaft` repositories. A daily run at 06:17 UTC (11:47 IST) refreshes activity such as star counts that has no dependable event trigger. If the issue snapshot cannot be fully refreshed, deployment stops and the prior site remains live. Activity failures show timestamped cached or unavailable data. Neither snapshot refresh changes tested component pins or commits generated data back to `main`.

For a local rehearsal, set `GROK_GADGETS_PUBLIC_SITE` to the intended HTTPS site root before running `website/build.py` and `scripts/check-pages-prefix.py`; the default is `https://grok-gadgets.pages.dev/`.

The homepage workbench shares a strict configuration format with the gateway simulator. Customize a name/ID, starting RGB/brightness, response delay and offline startup, then export JSON. Browser controls are local simulation. The inspectable downloadable kit contains exact source, wheel, hashed dependencies and license notices; setup is in docs/getting-started/simulator-kit.md.

Each website build validates kit source/input freshness and acceptance before replacing the previous preview. With a clean sibling gateway checkout, stale inputs trigger source tests and fresh installed MCP acceptance before the new download is copied. Without it, only the included kit matching the compatibility pin is accepted. `python3 scripts/build-simulator-kit.py --check`, `python3 scripts/test_simulator_kit.py` and `node --test website/test_simulator.cjs` verify the download/model. The Cloudflare Pages publication workflow runs these gates before deployment. See docs/verification/simulator-playground.md.

## Documentation navigation

`docs_navigation.py` assigns each published document to one task-based section. Linux and ESP32 guides have separate subgroups under Build a gadget. Community maintenance drafts and verification records stay outside the starting path.

To add a document, register it in `documents.json` and the navigation taxonomy. The build rejects missing or duplicate entries. Keep existing page URLs stable when moving a guide between sections.

Each article has breadcrumbs, a local navigation menu, a heading list and previous/next links within its subgroup. Native disclosure controls work without JavaScript. `docs.js` collapses the outer menu on narrow screens. The active subgroup stays open.

Run `.venv/bin/python -m unittest discover -s website -p 'test_*.py'`, build the site, and inspect desktop, narrow-screen and keyboard navigation before publishing a navigation change.
