"""Preview issue migration offline; use --apply for the approved five GitHub repositories."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
from pathlib import Path
import sys
import time

from github_issue_api import GitHubIssueAPI
from issue_migration import (
    OWNER,
    REPOSITORIES,
    MigrationError,
    MigrationRunner,
    atomic_json,
    prepare,
)

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def apply_lock(root):
    directory = root / "artifacts/issue-migration"
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "apply.lock").open("a+") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            raise MigrationError(
                "Another migration command holds the local apply lock"
            ) from None
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def current_plan(root, path):
    previous = json.loads(path.read_text())
    if not isinstance(previous, dict) or previous.get("owner") != OWNER:
        raise MigrationError("Migration plan must belong to adidshaft")
    plan = prepare(root, previous, owner=OWNER)
    for row in plan["records"]:
        if row["owner"] != OWNER or row["repository"] not in REPOSITORIES:
            raise MigrationError(
                "Stored mapping is outside the five approved repositories"
            )
    if {row["repository"] for row in plan["records"] if row["source_present"]} != set(
        REPOSITORIES
    ):
        raise MigrationError(
            "Migration must include the current ledgers of all five repositories"
        )
    if not plan["validation"]["ready"]:
        raise MigrationError(
            "Current manifest/dependency validation must pass before migration"
        )
    return previous, plan


def preview(plan):
    print(
        f"Offline preview for {OWNER}: {len(plan['records'])} durable records; no GitHub calls or changes"
    )
    for repository in REPOSITORIES:
        rows = [
            row
            for row in plan["records"]
            if row["source_present"] and row["repository"] == repository
        ]
        closed = sum(row["record"]["stage"] == "done" for row in rows)
        mapped = sum(row["github_number"] is not None for row in rows)
        print(
            f"{repository}: {len(rows)} issues, {closed} final closed, {len(rows) - closed} final open, {mapped} existing mappings"
        )


def apply(root, path):
    with apply_lock(root):
        # Reload under the lock; do not overwrite a checkpoint read before another run.
        previous, plan = current_plan(root, path)
        run_id = (
            datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
            + "-"
            + str(time.time_ns())
        )
        directory = root / "artifacts/issue-migration" / ("apply-" + run_id)
        atomic_json(directory / "previous-mapping.json", previous)
        api = GitHubIssueAPI(allow_writes=True)
        api.verify_targets()
        plan.update(mode="github apply", fixture_only=False, migration_complete=False)
        sequence = 0

        def checkpoint(value):
            nonlocal sequence
            sequence += 1
            atomic_json(directory / f"{sequence:04d}-checkpoint.json", value)
            atomic_json(path, value)
            mapped = sum(row["github_number"] is not None for row in value["records"])
            print(
                f"Saved {value.get('migration_phase', 'prepared')}: {mapped}/{len(value['records'])} mapped",
                flush=True,
            )

        checkpoint(plan)
        result = MigrationRunner(api, checkpoint, fixture_only=False).run(plan)
        print(
            f"Verified {len(result['records'])} GitHub mappings; repository issue migration complete"
        )
        print("GitHub Project setup remains a separate operation")
        return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plan", type=Path, default=ROOT / "publication/issue-migration.json"
    )
    parser.add_argument("--owner", choices=[OWNER], default=OWNER)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create/reconcile GitHub labels, milestones and marked issues",
    )
    args = parser.parse_args(argv)
    try:
        if args.apply:
            apply(ROOT, args.plan)
        else:
            _, plan = current_plan(ROOT, args.plan)
            preview(plan)
        return 0
    except MigrationError as exc:
        print("Migration stopped: " + str(exc), file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError):
        print(
            "Migration stopped: invalid/unavailable local data or checkpoint. Preserve saved mappings and reconcile before resuming.",
            file=sys.stderr,
        )
        return 1
    except KeyboardInterrupt:
        print(
            "Migration interrupted; resume the same command from its saved mappings",
            file=sys.stderr,
        )
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
