# Archive: first-launch tooling

These scripts and records served only the first public launch in October 2026. No CI job, `scripts/dev.py`, `scripts/check.py` or website build uses them. They are kept as a record and are not maintained or tested. Their paths still assume their original locations, so they do not run from here.

Dated launch documents, such as `docs/github-launch-plan.md` and `docs/verification/local-handoff.md`, still name these files at their original paths. Find them here.

| Moved from | What it did |
| --- | --- |
| `scripts/prepare-issue-migration.py`, `scripts/migrate-github-issues.py` | Built and applied the one-time move of local ledger issues to GitHub Issues |
| `scripts/test_issue_migration.py`, `scripts/test_github_issue_api.py` | Offline tests for that migration |
| `scripts/package-local.py`, `scripts/verify-publication.py`, `scripts/test_publication.py` | Built and checked the local release candidate |
| `scripts/audit-launch.py`, `scripts/test_audit_launch.py` | Pre-launch publication audit |
| `scripts/audit.py` | Pre-launch inventory and secret scan |
| `scripts/export-roadmap.py` | Exported the local ledger to Markdown |
| `publication/issue-migration.json`, `publication/migration-guide.md` | Migration map and guide |
| `publication/activation-guide.md`, `publication/expected-checks.json`, `publication/desired-protections.json` | Launch activation steps, expected checks and proposed protections |
| `publication/commit-summary.md`, `publication/history-and-assets-review.md`, `publication/release-notes.md` | Launch history review and draft release notes |

The live snapshot refresh still imports `scripts/github_issue_api.py` and `scripts/issue_migration.py`, so they stay in `scripts/`. `scripts/test_github_snapshot.py` tests the read path they serve.
