# Local issue migration preparation

Run from the hub checkout:

```sh
.venv/bin/python scripts/prepare-issue-migration.py
```

This command prepares `publication/issue-migration.json` for the planned owner `adidshaft`. It makes no GitHub calls. Existing GitHub numbers, URLs, extra mapping fields, and rows absent from current ledgers survive regeneration. Stable keys have the form `owner/repository/local-id`; a local ID is never recycled for a different issue. The source identities use repository-relative ledger paths.

A timestamped report under ignored `artifacts/issue-migration/` stores the previous mapping snapshot, validation result, and restore instructions before the plan is replaced atomically. Keep these local recovery reports private. To restore, inspect the recorded `previous_mapping_snapshot` and write only the intended checkpoint through `issue_migration.atomic_json`; restoring a local file does not undo any approved future external actions.

For a preview that leaves the canonical mapping untouched:

```sh
.venv/bin/python scripts/prepare-issue-migration.py --output /tmp/grok-issue-preview.json
```

The preview still reads existing canonical mappings. Use `--existing <checkpoint.json>` to inspect another checkpoint and `--report-dir <directory>` to choose local report storage. Validation errors are included in the preview and return exit code 1. Identity/URL collisions fail before replacing output. Preserve the last valid checkpoint and resolve the specific error before continuing.

Labels come from `publication/labels.json`; they need unique names, six-digit colors, and descriptions. Milestones combine historical `planning/milestones.json` IDs with new `publication/milestones.json` IDs. Every issue must select one declared primary milestone; combined values such as `M5/M8` are rejected. Historical IDs stay visible in the issue record. Extra prerequisite milestones belong in descriptive metadata rather than a fabricated combined milestone.

Issue bodies contain `<!-- grok-gadgets-local-id:adidshaft/repository/local-id -->`. Acceptance, evidence, commits, concrete blockers, and dependencies come from the owning ledgers. An unqualified dependency ID resolves within the same repository first, then to a unique issue under this owner. Use `repository#LOCAL-ID` or `owner/repository#LOCAL-ID` for an explicit cross-repository dependency. Ambiguous or missing IDs block preparation; narrative prerequisites stay text and never become invented issues.

## Fixture recovery rehearsal

```sh
.venv/bin/python -m unittest discover -s scripts -p test_issue_migration.py -v
```

`FixtureMigrator` accepts only an injected test API and checkpoint callback. No live API adapter, credential handling, migration CLI, or remote execution is supplied. Its fake interface expects complete issue-marker matches and label/milestone lists, including closed historical resources. It follows this order:

1. Validate manifests and mapping collisions, and reconcile every mapped issue before fake writes. A stale number pointing at an unrelated issue blocks all writes. Multiple marker matches require review.
2. Create missing labels and each required milestone before attaching them to issues.
3. Reconcile again before creating each issue. If an interrupted fake create already stored the issue, its marker recovers the ID. Save every accepted number and URL before proceeding.
4. Once all current issue identities are durable, write cross-repository links and final states. `done` becomes closed; blocked and other unfinished stages remain open. Retained rows absent from current ledgers are read-only.
5. Read back every mapped issue and verify the final payload before marking the fixture run complete.

A missing mapped issue without a marker match requires review rather than silently recreating deleted history. A stale number with one correct marker match may be repaired, retaining its prior mapping in `mapping_history`. Failures propagate; resume from the latest durable checkpoint. Re-running an unchanged successful fixture creates no duplicate issues or prerequisite resources and performs no redundant issue updates.

Public activation requires separate approval, a reviewed live adapter, complete remote reconciliation/readback, and the repository/project permissions described in the launch plan. After approved migration, GitHub Issues/Project become the authoritative status source; local ledgers become generated snapshots with the durable IDs retained. This local dry-run does not establish that transition or create the planned Project.
