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

`FixtureMigrator` remains a compatibility alias for `MigrationRunner` with fixture mode enabled by default. The injected interface expects complete issue-marker matches and label/milestone lists, including closed historical resources. It follows this order:

1. Validate manifests and mapping collisions, and reconcile every mapped issue before fake writes. A stale number pointing at an unrelated issue blocks all writes. Multiple marker matches require review.
2. Create missing labels and each required milestone before attaching them to issues.
3. Reconcile again before creating each issue. If an interrupted fake create already stored the issue, its marker recovers the ID. Save every accepted number and URL before proceeding.
4. Once all current issue identities are durable, write cross-repository links and final states. `done` becomes closed; blocked and other unfinished stages remain open. Retained rows absent from current ledgers are read-only.
5. Read back every mapped issue and verify the final payload before marking the fixture run complete.

A missing mapped issue without a marker match requires review rather than silently recreating deleted history. A stale number with one correct marker match may be repaired, retaining its prior mapping in `mapping_history`. Failures propagate; resume from the latest durable checkpoint. Re-running an unchanged successful fixture creates no duplicate issues or prerequisite resources and performs no redundant issue updates.

## Explicit GitHub migration

Use the sanitized public checkout on macOS or Linux with Python and the existing authenticated GitHub CLI. Preview performs no GitHub calls, writes no files, and refreshes the plan in memory against all five current ledgers:

```sh
.venv/bin/python scripts/migrate-github-issues.py
```

Once source publication and issue population are authorized, apply with the same durable mapping file:

```sh
.venv/bin/python scripts/migrate-github-issues.py --owner adidshaft --apply
```

`--plan <checkpoint.json>` chooses another existing mapping checkpoint; the canonical default is `publication/issue-migration.json`. The command reloads it under a local apply lock, preserves retained rows and extensions, validates current manifests/dependencies and every target, then checks that `gh` authenticates as `adidshaft` and all five repositories have issues enabled and write permissions. It cannot target another owner/repository. Preview never constructs the API adapter. Writes require both explicit `--apply` and successful preflight.

`github_issue_api.py` uses `gh api` against `github.com`, JSON on standard input, pinned REST version `2022-11-28`, and bounded paginated inventories. It reads open and closed issues/milestones, excludes pull requests, verifies HTML issue URLs, resolves milestone titles to remote numbers, and compares labels independent of response order. Stable markers must be exactly the first body line, once only; duplicate or misplaced markers block migration. API stderr, response bodies and credentials are not printed or written into reports. Request uncertainty stops without an automatic mutation retry.

Each apply run saves the previous full mapping and numbered checkpoints under ignored `artifacts/issue-migration/apply-<run-id>/`. Every accepted identity is saved before the next issue and before dependency links/closed states. The canonical mapping is atomically replaced after each checkpoint. If a response or checkpoint is lost, rerun the same command: remote markers recover accepted issues before any new create. Existing unrelated/stale/ambiguous mappings, unknown API responses or incomplete pagination block writes. Retained rows absent from ledgers are verified without modification. Do not run migrations concurrently from separate workspaces.

Run the offline adapter/entry-point regressions with:

```sh
.venv/bin/python -m unittest discover -s scripts -p 'test*issue*.py' -v
```

Success records `migration_complete: true`, `fixture_only: false`, `activated: true` and `migration_phase: verified`, after readback of all mapped issues. This completes repository issue migration, not the separately scoped GitHub Project. Preserve the local mapping after activation; switch status ownership to GitHub Issues/Project only when their live setup and snapshot/export workflow have been verified. Do not continue writing conflicting independent local status.

API behavior: [GitHub issues REST API](https://docs.github.com/en/rest/issues/issues), [supported API versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions), and [GitHub CLI API](https://cli.github.com/manual/gh_api).
