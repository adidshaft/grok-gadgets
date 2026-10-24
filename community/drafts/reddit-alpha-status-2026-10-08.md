# Reddit draft — public alpha status

**Status:** Draft only. Publishing requires final confirmation.

**Suggested flair:** Release

## Title

Grok Gadgets v0.1.4-alpha.1: public alpha status

## Body

Grok Gadgets is a public software alpha for building device integrations for Grok Bot. The current release set is published, and the website, roadmap, source branches, simulator kit, and integration checks are available for review.

### Current release set

- **Hub / website:** `v0.1.4-alpha.1`
- **Gateway:** `v0.1.0-alpha.4`
- **Linux SDK:** `v0.1.0-alpha.4`
- **ESP32 SDK:** `v0.2.0-alpha.5`
- **Home Assistant:** `v0.1.0-alpha.4`

### Start here

- **Roadmap:** <https://grokgadgets.org/roadmap>
- **Website and simulator:** <https://grokgadgets.org/>
- **Alpha releases:** <https://github.com/adidshaft/grok-gadgets/releases>
- **`main` release branch:** <https://github.com/adidshaft/grok-gadgets/tree/main>
- **`dev` integration branch:** <https://github.com/adidshaft/grok-gadgets/tree/dev>
- **Integration checks:** <https://github.com/adidshaft/grok-gadgets/actions/workflows/integration.yml>

### How releases move

`dev` receives ordinary feature, fix, documentation, and test work. When the integrated set is ready, it moves to `main`, is tagged, and is published as a release. `main` supplies the website and simulator download. The scheduled integration workflow checks compatibility; downloadable alpha builds are published in GitHub Releases.

### What this alpha shows

The public evidence covers the browser simulator, local gateway paths, SDK acceptance checks, ESP32 compilation, Home Assistant fixture checks, and release artifacts. Native Grok Bot operation, physical hardware operation, real Home Assistant installs, mobile behavior, and independent reproduction remain the next evidence gates.

If you test a release, include the release version, board or OS, expected and observed behavior, and redacted logs. Please keep private tokens, keys, logs, addresses, and household details out of posts.

---

**Companion graphic:** `reddit-project-progress-executive-2026-10-08.png` (16:9 project-progress slide). Source: `reddit-project-progress-executive-2026-10-08.html`.
