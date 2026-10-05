> Historical pre-publication audit. Its privacy/history gates were subsequently addressed by the owner-authorized rewrite described in [the sanitization record](../docs/verification/publication-sanitization.md). Original execution timestamps and findings below describe that earlier audit.

# History and public-asset disposition — launch checkpoint

Local review for LAUNCH-PUBLIC-001/L6, 5 October 2026. This records a reviewed checkpoint, not authorization to push, publish, deploy or redistribute binaries. Histories, names, identities, refs and global configuration were preserved. No external research or account access was used.

Reproduce with `.venv/bin/python scripts/audit-launch.py`. It writes an ignored timestamped inventory under `artifacts/launch-audit/` and prints redacted counts/hash. `--output` selects an explicit local report; `--repo` supports bounded fixtures. Regenerate after the final source commit and main integration. The external inventory certifies its recorded sources; this document does not certify the commit that will contain it.

## Reviewed scope and results

Checkpoint inventory: `artifacts/launch-audit/review-complete.json`, SHA-256 `100754939dd8e7fd42ba2a7aaa7bc3545d99bab39d4c1e24b6719c89b1c38ab0`. The hub working tree contained the lead's ongoing launch edits; sibling tracked trees were clean. Each repository's HEAD remained stable during its scan. The component rebuild evidence advanced ESP32 to the head recorded below.

| Repository | HEAD | HEAD commits | Reachable blobs, including direct recovery refs | Replaced/deleted HEAD-history blobs |
| --- | --- | ---: | ---: | ---: |
| Hub, `prep/github-alpha-launch` | `0a6410f724619ae97ff4594825fa180139badb34` | 39 | 434 | 237 |
| Gateway, main | `2af35fa07910a6111fa3100496128b3db707dfcd` | 14 | 103 | 52 |
| Linux SDK, main | `7bff349dee943f20e07fa7cba7761023f0c9584a` | 12 | 85 | 38 |
| ESP32 SDK, main | `ef5a9cb0d1bc3dd74298e9750dfae954f712d3bd` | 14 | 128 | 71 |
| Home Assistant, main | `b0dad5fc5eb80941676665ec699aefd52f5671f6` | 8 | 49 | 19 |

Totals: 87 commits, 799 unique blobs per repository summed, 55 local refs. All commits reachable through local refs are also in the respective HEAD histories at this checkpoint. Three hub Codex refs point directly to tree `d1c5c5f250cc6a91ea346647167c67058cfbe5f0`, rather than commits. Walking only commit history would miss seven additional recovery-only blobs. Those contain raw brand assets, generation notes and a 3,138,712-byte ZIP; the inventory records full object IDs and hashes. The extra ZIP object is `6daf294ae95d7d3c45fc8236db58e8d9d054a603`. No refs were removed or rewritten.

The scanner reads every index-tracked worktree file, all HEAD/local-ref commit-tree blobs, direct tree/blob refs, author/committer identities and complete commit messages. It inspects binary bytes and ZIP/tar members, including nested kit wheels/sdists/source archives, to depth three with a 128 MiB expanded ceiling per archive. No members were skipped in these reviewed archives. Reflog-only, dangling/unreachable objects, OCR, arbitrary encodings, steganography and unknown credential formats are outside its scope. Match values and raw identities are never placed in inventory JSON/stdout.

Selected private-key, GitHub-token, AWS-access-key, xAI-key, bearer-literal and credential-assignment patterns found **zero matches** in the reviewed tracked files, reachable blobs, nested archive text and commit messages. This is a limited heuristic observation, not proof that no secrets exist. False positives and future changes require human review.

The full inventory lists 29 hub binary blobs, including six recovery-only binary assets and one large recovery ZIP. Twenty-five image objects were inspected as a private contact sheet; the new simulator screenshot was inspected separately. They show site/software UI and artwork without obvious account UI or credential values in the inspected views. Thumbnail review does not establish full-resolution OCR/privacy clearance. Historical images remain historical evidence, rather than current product/Grok/physical acceptance.

## Privacy and history gates

| Finding | Disposition before activation |
| --- | --- |
| 18 hub and four Linux historical blobs contain host-path patterns | Preserve history. Normalizing current files cannot remove old blobs from a public main push. Obtain an explicit decision to disclose the reviewed historical local paths, or separately authorize a different history strategy. Neither decision is inferred here. Examples: hub blob `9b3db8ea29f44e2758913316fc1d6aa3197e07ce` in `docs/hardening-plan.md`; Linux blob `0e008a03fd3e341f48409c0deb03e5a4d620f7d8` in `docs/verification/hardening.md`. Raw path values stay private. |
| All 87 commits use one personal author/committer email fingerprint | Preserve identities. The fingerprint is `9fb498561c8f0c80b0e01994957a1cca6230bbb6fa26e90607f336a30f63a3f4`; no raw email is reproduced. Public Git history exposes it even when current docs are sanitized. Explicit disclosure approval is required before pushing that history. |
| Current hub host-path matches | At the scan: `docs/verification/hardening-status.md` requires normalization; `website/documents.py` contains a normalization-pattern literal rather than a private account path. Lead owns current-file fixes. Rerun against the final clean main; do not treat this dirty-worktree checkpoint as final clearance. |
| Recovery refs and bundles | All `--all` bundles are **private recovery only**, including their Codex tree assets. Never upload a recovery bundle or use `git push --mirror`/`--all` as the approved public payload. A selected main push still includes its reviewed historical blobs and identity metadata. |
| Ignored account evidence and untracked assets | Exclude `artifacts/`, `reports/`, build logs, Bot/connector screenshots/receipts/configurations, dependency caches, `.env`, `.DS_Store` and the untracked `assets/` tree wholesale. Only individually reviewed copies may enter a public allowlist. |

## Licenses and package contents

All five complete LICENSE files are byte-identical Apache-2.0, SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`, and each has one unchanged reachable version. Every repository's NOTICE also has one unchanged reachable version; its current content was read in full.

| NOTICE | SHA-256 |
| --- | --- |
| Hub | `84222354b6836a8bb74d4de0ca58e3921260fbdd37e8b3ef1f07e0dcba4b1ae8` |
| Gateway | `aaa01a326c6adb0b7e10b6de1e0ce48e772d526cbd16dc3c9e8a70c155952c9a` |
| Linux SDK | `dad71e488069c4f7bc81f21683109aa6d80b8b3042db78d4fbee9e75706ea0bc` |
| ESP32 SDK | `b84c018319b2d92e9f4e72466305f0749a5f0f61ff96c16f506b69d8357b4255` |
| Home Assistant | `45b6bf837b7b76956f0a5941846c93704d61f2870013fb35d59830db4e46c55e` |

All three local Python wheels contain LICENSE and NOTICE under their distribution license directories; all three sdists contain the corresponding root files. Their embedded hashes match the owning repositories. Each wheel METADATA declares `License-Expression: Apache-2.0`. These six local packages are evidence, not approved current-head release assets: the final candidate must rebuild packages from its selected exact Git archives and repeat hash/runtime/license checks. Third-party dependencies are installed separately, not relicensed by this original-code declaration. Gateway NOTICE lists MCP/jsonschema/pySerial; Linux lists jsonschema; HA lists MCP/httpx and locked dependencies, and states Home Assistant code is not vendored. Retain installed-distribution attribution when redistributing dependencies.

ESP32 `platformio.ini`, lock/build records and `docs/dependencies.md` identify the pinned dependencies: Arduino-ESP32 includes LGPL-2.1/ESP-IDF components, NeoPixel is LGPL-3.0, ArduinoJson is MIT; PlatformIO/platform and pyserial also retain their notices. The local dependency record explicitly requires corresponding source, licenses and relinking review before binary distribution. Compilation/provenance alone does not supply that package. **Firmware BIN/ELF/bootloader/partition uploads remain excluded** until completeness and relinking requirements have a concrete reviewed disposition. Source/build instructions remain eligible subject to the other gates; this is a project release gate based on the local records, not legal clearance.

## Artwork and public artifact allowlist

The raw brand generation notes identify built-in image generation and macOS resize/crop exports, including creative references to Grok styling. They establish generation provenance, not ownership of third-party marks or blanket public permission. The selected icon and logo copies match the raw originals by hash (`6d0b4c7cd981d7895bc1763fc55d1c9dae13ad27dbd9c9398ead8a8690b8f56f` and `e984b8c1dcffeb9517b9e4d34effcb5178a95352f249765aca6d64fe1f2000b3`). The existing provenance's four file hashes match the actual media bytes. Lead is preparing sanitized provenance and a screenshot registry, without publishing raw generation notes.

Official `grok-mark.svg` and `spacexai-mark.svg` are separately attributed in THIRD_PARTY_NOTICES and media provenance. They are not Apache project artwork. No new terms review was performed; existing local records defer naming and official-mark usage decisions. Keep the current working names for preparation, and obtain the eventual activation disposition for names/marks without inferring approval from this audit. Original `.mmd`/SVG diagrams and the conceptual C124 reference have source records and explicit simulation/physical limits; the simulator screenshot shows the corrected export UI and is software evidence only.

| Candidate payload | Proposed public allowlist and gates |
| --- | --- |
| Five source ZIP/tar archives | Exact selected Git HEAD trees, with LICENSE/NOTICE and applicable third-party notices. No `.git`, recovery refs, ignored/private files or arbitrary untracked content. Final current-file/path/privacy review and explicit public approval remain required. Archives carry current trees, while a repository push additionally carries historical disclosures. |
| Gateway/Linux/HA wheel + sdist | Exact final-source rebuilds with embedded LICENSE/NOTICE, matching runtime/schema bytes, external source/hash provenance and approved version notes. No dependency caches or raw build evidence. |
| Website ZIP / Pages payload | Fresh build from approved committed sources: generated HTML/CSS/JS, sanitized activity/status JSON, selected original diagrams, individually reviewed site screenshots/media, simulator ZIP and its manifest. Explicit name/official-mark disposition applies to any included branded media. Enumerate/hash actual files from final `website/dist`; never publish the enclosing workspace or artifacts directory. |
| Simulator ZIP | One kit root containing LICENSE, NOTICE, README, SHA256SUMS, `install.py`, `try_simulator.py`, reviewed `requirements.txt`, default `simulator-config.json`, its schema, manifest, exact gateway wheel/sdist and `source.tar`. Check all 13 expected members, nested package licenses/hashes/runtime source, safe paths and exact current gateway provenance. No Bot account data, custom private config, credentials, logs, Git metadata or external recovery bundles. |
| Checksums/manifest/release notes | Reviewed public asset hashes, source commits, build environment, licenses and truthful simulation/build limits. Generate external final-candidate evidence after source commit; remove private recovery artifacts from the public asset list. |
| Firmware or raw brand ZIP, all-history bundles | Excluded. Firmware needs the dependency redistribution/relinking package; raw art ZIP/notes need explicit per-asset provenance/branding review; recovery bundles remain private regardless of token scan outcome. |

The internal publication manifest includes firmware and five recovery bundles for local verification/recovery. Its complete 25-artifact list is not the public release allowlist. The lead must select and hash the public subset before asking for approval.

## Verification and limitations

Five meaningful local audit tests pass: deleted-secret/history metadata redaction, commit recovery refs, direct Codex tree-only secrets, a large batch request, changed worktree/NOTICE versions, and nested archive attribution/token detection (some checks share one test). Ruff check/format and hub `scripts/check.py` pass. An initial full-run pipe-buffer stall was corrected with file-backed Git batch input/output; the large-batch regression prevents recurrence. The first thumbnail attempt lacked Pillow in the hub environment; the existing bundled runtime produced the ignored inspection sheet without changing project dependencies.

Keep inventories, object listings and inspection sheets private. Rerun at final clean source/main and independently inspect the selected public artifacts. Unresolved history/identity, naming/official-mark and firmware obligations are explicit gates; none is closed by a zero-match heuristic or an internally verified package.
