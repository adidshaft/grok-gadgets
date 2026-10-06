# Public-history sanitization — 5 October 2026

The owner approved sanitization before the first public GitHub push. Original repositories and recovery bundles remain private. Public development continues from the sanitized checkouts; never merge the original private history into them.

All 99 existing commits were retained: hub 51, gateway 14, Linux 12, ESP32 14 and Home Assistant 8. Original messages, author/committer dates and parent relationships were checked against the private originals during the privacy rewrite. Commit IDs changed. New maintenance, provenance and publication commits follow that preserved history.

The owner subsequently requested distributing the unpublished commit timeline across the seven calendar days ending 5 October 2026. This is a reconstructed import timeline, not a record of work or testing on those earlier dates. Commit order, messages and source trees are retained by that date-only rewrite; author/committer timestamps and descendant IDs change. Actual verification dates, execution receipts and build timestamps remain unchanged. Fresh tests and artifact regeneration after the rewrite are recorded at their real execution times. Original dates remain in the private backups.

The private author email was replaced with the owner's GitHub noreply identity in Git metadata and source text. Machine-account paths were replaced with generic paths; the website privacy test now checks the generic `/Users/` prefix. Historical generated simulator ZIPs were removed because compressed source documentation retained the private address. This removed generated payloads, not their surrounding commits. A new verified kit is committed from sanitized gateway source.

Current component/protocol pins, issue commit references and documentation inventories were remapped or regenerated. Earlier execution logs and platform observations remain historical evidence; rewriting provenance is not a new native Grok or physical hardware test. The current kit was rebuilt and exercised through its installer and official local MCP acceptance. ESP32 firmware was freshly compiled from clean sanitized source; binary distribution remains gated separately.

Each repository has updated ignore rules for environment files, credentials, private device configurations, traces, logs, caches, builds, artifacts and reports. Reviewed example files and the public kit remain addable. `git check-ignore` probes cover both exclusions and exceptions. CONTRIBUTING.md and AGENTS.md require maintaining these rules as tools and outputs change. Ignore rules do not retroactively remove tracked content.

A second independent literal scan checks the known private identity and machine prefix across reachable commit metadata, blobs and nested archives, complementing the generic heuristic audit. No raw private values or private recovery references belong in public reports. Only reviewed `main` is intended for the first push; old/checkpoint refs and bundles stay private.

The first GitHub-created publication merge used the account email rather than the local checkout's noreply identity. A post-merge check caught it. That one merge commit was corrected to the noreply identity without changing its tree, parents, message or timestamps; its original signature cannot survive a metadata rewrite. A narrowly scoped owner bypass was removed immediately after the correction, and the original active rules were verified again. This repairs current branch history; it does not establish deletion of the old object from GitHub's pull-request or cached references. Future maintainer merges verify a public author/committer identity. GitHub rejected the explicit noreply address for the server-created follow-up merge, so the fallback is a locally authored merge with the same reviewed tree and required checks under the existing protection; the private default email is never a fallback. Account-wide settings remain unchanged.

From 6 October 2026 the owner treats the account Gmail address as public; commits `b642401` (hub) and `e2468b0` (Linux SDK) carry it, and no rewrite is planned. The private-email commit check and its local hooks were retired the same day; GitHub secret scanning with push protection still guards real secrets.

The first source push and issue setup are authorized. Pages deployment, package/prerelease uploads, firmware downloads, Reddit changes and recurring automation remain separate operations. The published project is an experimental software alpha with native Grok receipts, physical hardware, real-home and mobile acceptance still pending.

## Reconstructed timeline

The date-only rewrite covered 106 commits: the 99 original commits plus seven tested publication-preparation commits. Every repository has commits on all seven dates. Later cleanup, regenerated evidence and publication commits use their actual creation times. Source trees, messages and parent ordering are unchanged by the date rewrite itself; current source references are refreshed in subsequent commits.

| Repository | Sep 29 | Sep 30 | Oct 1 | Oct 2 | Oct 3 | Oct 4 | Oct 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| grok-gadgets | 8 | 8 | 7 | 8 | 7 | 8 | 7 |
| grok-gadgets-gateway | 3 | 2 | 2 | 2 | 2 | 2 | 2 |
| grok-gadgets-linux-sdk | 2 | 2 | 2 | 2 | 2 | 2 | 1 |
| grok-gadgets-esp32-sdk | 3 | 2 | 2 | 3 | 2 | 2 | 2 |
| grok-gadgets-home-assistant | 2 | 1 | 1 | 2 | 1 | 1 | 1 |
