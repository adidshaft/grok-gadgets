# Reviewable publication package — inactive

Proposed state: `0.1.0-alpha.1`, local alpha, simulation/build evidence only unless exact component manifests establish otherwise. Five independent repositories retain incremental commit history. No public owner, remote, package, release, site, or Reddit change has been created.

Approval must identify the GitHub owner, five repository creations/pushes, desired visibility, release/package destinations, and website hosting separately. The current package can be reviewed without granting those actions.

Before activation: rerun all-checks; inspect license/dependency notices and redacted secret scan; verify clean repositories and compatibility hashes; establish real private security reporting; resolve public policy links; choose actual maintainer ownership; review exact issue migration output, release notes/assets/checksums, protection settings, and deployment permissions. A sole maintainer uses no impossible second-human rule.

Approved sequence: create five repositories under selected owner; add remotes and push main preserving histories; activate workflows; migrate component ledgers and hub parent issues retaining local-to-GitHub mapping; apply labels/milestones and overall project board; apply desired protections after check names actually appear; enable private security reporting; create prerelease tags at verified commits; attach artifacts/checksums; deploy static website only. Gateway and identity backend need separately reviewed authenticated service architecture.

Rollback: retain previous tested compatibility manifest and firmware; revoke credentials/disable exposed service if a security issue occurs; withdraw misleading release claims; rebuild previous static site snapshot. Device SDK firmware recovery instructions are authoritative.

Reddit audit, proposed before/after settings, post drafts, and recognition design are in community/. A moderator audit must precede changes. Live recognition needs approved runtime/access/proof validation and private data storage. No automation is activated.

## Corrected local candidate

From a clean tracked source tree containing allfive sibling Git repositories and the pinned website environment:

```sh
.venv/bin/python scripts/package-local.py
.venv/bin/python scripts/verify-publication.py --require-current
python3 -m unittest discover -s scripts -p test_publication.py -v
```

The latest pointer is artifacts/publication/latest.json. Each run has a unique subdirectory; older flat artifacts and prior runs remain preserved. Manifest format2 identifies exact source HEADs, all25artifact records and their source commits. SHA256SUMS also hashes the manifest; the latest pointer independently hashes it. Allfive source archives are exact Git archives and allfive complete-history bundles have no prerequisites. Python packages are freshly built offline from those Git archives, with runtime byte checks and configuration/environment provenance. Firmware hashes are checked against its clean build manifest; ancestor evidence-only changes are explicitly recorded, while changed runtime/toolchain files require rebuilding. Static site is freshly generated from committed inputs. No source assets/ or untracked work is packaged.

Integrity regressions challenge tampered binaries/packages/source archives, malformed provenance, stale firmware runtime, incomplete bundles, dirty source and preservation of prior candidates. Final package reviewer checks the assembled candidate, separately from source review. Raw logs and local filesystem inventories stay outside the public static site. Hosted hub CI will need allfive sibling checkouts at the pinned sources when public repositories are approved; the current local multi-repository build does not infer those future URLs.
