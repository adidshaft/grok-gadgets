"""Explicit five-repository GET-only snapshot refresh; builds remain offline."""

import argparse
from pathlib import Path
import sys

from github_snapshot import load_snapshot, refresh_snapshot
from issue_migration import MigrationError

ROOT = Path(__file__).resolve().parents[1]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "publication/github-issues.json"
    )
    parser.add_argument(
        "--check", action="store_true", help="Validate the saved snapshot offline"
    )
    args = parser.parse_args(argv)
    try:
        snapshot = (
            load_snapshot(args.output) if args.check else refresh_snapshot(args.output)
        )
    except (MigrationError, OSError, ValueError, KeyError, TypeError):
        print(
            "Snapshot check/refresh failed; previous snapshot preserved. "
            "No GitHub changes were made.",
            file=sys.stderr,
        )
        return 1
    print(
        f"{'Validated offline' if args.check else 'Refreshed'} "
        f"{len(snapshot['issues'])} issues from GitHub Issues; "
        f"snapshot time {snapshot['refreshed_at']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
