# Public source alpha — 5 October 2026

All five source repositories are public under [adidshaft](https://github.com/adidshaft/grok-gadgets). Each has an Apache-2.0 license, README, contribution/security/conduct guidance, issue templates, repository description and topics. Private vulnerability reporting is enabled and verified. The static site is live on free Cloudflare Pages; package releases and firmware downloads remain separate operations.

## What works now

The website provides an interactive architecture, a customizable virtual light, exported configuration and an inspectable simulator download. Gateway and SDK software acceptance passes, including installed-package checks. C124 firmware compiles. These checks do not establish native Grok invocation, physical LED/button operation, real-home compatibility or mobile acceptance.

| Component | Published source | Verified evidence |
| --- | --- | --- |
| Gateway | `6c66a109084dc8480fdd49636dab2254d7e3d82e` | 77 tests, local MCP and installed simulator acceptance; hosted standalone CI |
| Linux SDK | `b0e5f4bb407f4d4419673d4c1a5d540f68511c23` | Unit/CLI tests, installed custom applications and hosted standalone CI |
| ESP32 SDK | `ef04fa0405ea4820de6430578684959f6e6dd8d8` | Three host suites, protocol/USB simulation and hosted firmware compilation |
| Home Assistant | `6afac04e39ca5cf16af9c4bfd3d9a12f6844386a` | 13 fixture/transport tests and hosted standalone CI; no real home actions |
| Hub | [Actions](https://github.com/adidshaft/grok-gadgets/actions) | Website, simulator, publication regressions and all fourteen integration groups |

The first hub hosted run exposed a filesystem-order assumption in an archive regression and missing pip resolver metadata in an otherwise warmed uv cache. Commit `f78a5f668b8108435acd18cba24ddd249e45abdf` selects the exact source archive and prepares pinned runtime dependencies before strictly offline installed-package acceptance. Its [hub checks](https://github.com/adidshaft/grok-gadgets/actions/runs/37260225878) and [integrated acceptance](https://github.com/adidshaft/grok-gadgets/actions/runs/37260225894) passed on GitHub. The corresponding failed runs remain available as historical diagnostics.

Current simulator kit: gateway `6c66a109084dc8480fdd49636dab2254d7e3d82e`, version `0.1.0a1`, SHA-256 `47f58e94ea6e3c8b6fd3acec1bd0fb4cc84597c3c8d7e28ac49b2bad08c3e894`. Fresh source and installed default/custom MCP acceptance passed. The current download is separate from historical Grok-account observations.

## Cloudflare Pages

The free static site is live at [grok-gadgets.pages.dev](https://grok-gadgets.pages.dev/). Production deployment `589fab44-972e-47d6-a02b-05cf12a0576c` is tied to main SHA `925d4b6e362f30202d1072ebfecd9d52fc49637e`, after both required workflows passed on that exact SHA. The deployment workflow refreshed complete issue and activity snapshots for all five repositories, built the site, checked its tested kit, and published it. HTTPS `/`, `/start`, `/architecture`, and `/activity` returned 200. The live simulator kit SHA-256 matches `47f58e94ea6e3c8b6fd3acec1bd0fb4cc84597c3c8d7e28ac49b2bad08c3e894`. All five repository About homepage links were updated and read back. Daily snapshot refresh is scheduled at 06:17 UTC; failed builds keep the last good deployment.

## History, issues and contribution flow

The original 99 commits were retained. Sanitization removed the private commit email and machine-account paths, and rebuilt historical generated downloads. At the owner's request, 106 pre-publication commits were distributed across 29 September–5 October; this is a reconstructed timeline. Actual execution timestamps remain unchanged. See [the history and privacy record](publication-sanitization.md).

GitHub Issues is the authority after migration. The local planning ledgers retain preparation history; the website reads a validated timestamped [GitHub snapshot](../../publication/snapshot-guide.md). New issues need no local-ledger entry. The private migration checkpoints and original history backups are excluded from publication. A separate GitHub Project board is not activated.

Main-branch policy requires pull requests, resolved review conversations and the exact GitHub Actions checks. Force pushes and deletion are blocked; original commit history is preserved. Zero mandatory human approvals supports the sole maintainer, while all required checks still apply. The repository rules pages are the authoritative live settings.

## Still pending

- Native invocation receipts from the supported Grok Bot route. Installation or model narration is not invocation evidence.
- C124 hardware, flashing, USB enumeration and physical LED/button observations.
- Real Home Assistant entities, Linux peripherals/systemd, mobile and independent human reproduction.
- Package/prerelease publication and firmware redistribution materials.
- GitHub Project activation, Reddit configuration, opt-in identity linking and unattended contributor-flair automation.

Use [the support matrix](../public/support-matrix.md) and each component README for the tested environments. Local macOS checks do not establish every platform. Historical build/account observations remain in [the launch journal](launch-journal.md) and [Grok evidence record](grok-launch-evidence.md).
