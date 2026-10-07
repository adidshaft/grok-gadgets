"""Prepare a durable migration dry-run only; never invokes GitHub."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

from issue_migration import MigrationError, OWNER, atomic_json, prepare

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "publication/issue-migration.json"
    )
    parser.add_argument(
        "--existing",
        type=Path,
        default=ROOT / "publication/issue-migration.json",
        help="Read durable mappings here even when output is a scratch preview",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=ROOT / "artifacts/issue-migration",
        help="Timestamped local dry-run/restore reports",
    )
    args = parser.parse_args()
    try:
        existing = (
            json.loads(args.existing.read_text()) if args.existing.is_file() else {}
        )
        plan = prepare(ROOT, existing, owner=OWNER)
        run_id = (
            datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
            + "-"
            + str(time.time_ns())
        )
        report = {
            "run_id": run_id,
            "mode": "local dry-run",
            "remote_actions": 0,
            "prepared_at_utc": plan["prepared_at_utc"],
            "owner": OWNER,
            "record_count": len(plan["records"]),
            "mapped_count": sum(
                row["github_number"] is not None for row in plan["records"]
            ),
            "unknown_retained_count": sum(
                not row["source_present"] for row in plan["records"]
            ),
            "validation": plan["validation"],
            "previous_mapping_snapshot": existing,
            "restore": "Review this previous_mapping_snapshot and use atomic_json to restore the intended local checkpoint; no remote rollback is performed.",
        }
        # Preserve the pre-write mapping snapshot before replacing the canonical plan.
        atomic_json(args.report_dir / (run_id + ".json"), report)
        atomic_json(args.output, plan)
        print(
            f"Prepared {len(plan['records'])} local issue records for {OWNER}; no GitHub changes"
        )
        print(f"Dry-run/restore report: {args.report_dir / (run_id + '.json')}")
        if not plan["validation"]["ready"]:
            for error in plan["validation"]["errors"]:
                print("Blocked: " + error, file=sys.stderr)
            return 1
        return 0
    except (MigrationError, OSError, ValueError, KeyError, TypeError) as exc:
        print("Migration preparation failed: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
