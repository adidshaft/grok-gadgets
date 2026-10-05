# Local publication candidate — inactive

Proposed experimental version: `0.1.0-alpha.1`, five independent repositories under confirmed owner `adidshaft`. Original code is Apache-2.0. Current names are retained; naming/official-mark disposition is deferred. The repositories and source push are active. Cloudflare Pages hosting is being configured under the decision in [003](../docs/decisions/003-cloudflare-pages-hosting.md); its first deployment and live URL remain unverified. No public tag, package/release upload, Reddit change or automation has occurred.

The public offer is software simulation, buildable source and clearly limited integrations. Local official-MCP acceptance and C124 compilation do not prove native Grok invocation or physical operation. Dedicated Grok computer installation evidence is in `docs/verification/grok-launch-evidence.md`; inspectable exact-kit native receipts remain gated. Use the support matrix and release notes for actual limits.

## Rebuild and inspect

With all five clean sibling Git checkouts and their documented pinned environments:

```sh
.venv/bin/python scripts/check-all.py
.venv/bin/python -m unittest discover -s scripts -p 'test_*.py'
.venv/bin/python scripts/package-local.py
.venv/bin/python scripts/verify-publication.py --require-current
.venv/bin/python scripts/audit-launch.py
```

`artifacts/publication/latest.json` points to a unique preserved candidate directory. Format2 manifests identify exact source HEADs,25 internal artifacts, provenance and hashes. All source archives come from those Git objects; all-history bundles are private recovery material. Python wheels/sdists are freshly rebuilt offline from exact archives, with matching runtime/schema bytes, LICENSE/NOTICE and configuration/environment provenance. Firmware must match a clean build manifest; only explicitly allowed evidence-only descendant changes can reuse it. Static site rebuilds from selected inputs with a verified content-addressed simulator download. Untracked `assets/` is preserved and excluded.

The simulator kit also works from a standalone hub checkout: it verifies the committed archive against the pinned gateway source and packaging-input hashes. A clean changed gateway/input rebuild runs source and installed default/custom acceptance. Dirty source, corruption and failed acceptance block promotion. The complete pair is staged/verified first; a promotion write error restores old files. Website promotion separately preserves the last-good site. See the download-build policy.

## Select the public subset

The internal25-artifact candidate is **not** an upload list. The proposed public subset is five current source archives, gateway/Linux/HA wheel+sdist and build provenance, the static site, the verified simulator kit and its manifest, reviewed release notes/checksums. Its final asset list must enumerate file hashes and source commits separately.

Exclude every recovery `.bundle`, raw account/log evidence, local inventories, credentials, dependency caches, untracked/raw branding assets and firmware BIN/ELF/bootloader/partitions. Firmware binary distribution needs corresponding-source/relinking/license material; source/build instructions can be reviewed separately. Official reference marks carry their own usage terms and no Apache trademark grant. The history/asset report records reachable deleted blobs, direct recovery tree refs, historical machine paths and personal commit identities; explicit disclosure approval is required before pushing main. No history or identity was rewritten.

## Approval and activation

The original publication approval packet identified exact candidate/manifest hashes, five selected commits, chosen source/release/site assets, and the pending history/branding decisions. Repository creation and source publication are complete. Review [activation steps](activation-guide.md), repository payloads, expected hosted checks, rulesets and resumable migration records for any remaining release work.

Hosted standalone/integrated acceptance, real check/app names, ruleset readback, issue/Project reconciliation, support/private-security routes and live HTTPS/deep-link/download behavior must be verified. Cloudflare Pages deployment is gated by the exact successful main checks, with a daily metadata refresh. Failed updates retain the reviewed last-good deployment; reviewed main reverts restore previous pins without rewriting history.

Reddit settings/drafts, recognition consent/proof/fixture logic and moderation policies are in `community/`. Their live audit, permissions, backend and activation remain separate. Remote authenticated device services, mobile clients, C124 hardware, real households/systemd/peripherals and independent human reproduction stay explicitly open.
