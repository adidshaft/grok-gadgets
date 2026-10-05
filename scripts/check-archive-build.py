"""Build the site from tracked files only, the way a GitHub ZIP download sees it."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    tracked = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")
    with tempfile.TemporaryDirectory() as folder:
        export = Path(folder) / "grok-gadgets"
        for raw in filter(None, tracked):
            name = raw.decode()
            source = ROOT / name
            if not source.exists() and not source.is_symlink():
                continue
            target = export / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target, follow_symlinks=False)
        env = {k: v for k, v in os.environ.items() if k != "GROK_ACTIVITY_FILE"}
        for command in (
            [sys.executable, "website/build.py"],
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "website",
                "-p",
                "test_*.py",
            ],
        ):
            result = subprocess.run(
                command, cwd=export, env=env, capture_output=True, text=True
            )
            if result.returncode:
                sys.stderr.write(result.stdout[-4000:] + result.stderr[-4000:])
                raise SystemExit(
                    "Source-archive build failed: " + " ".join(command[1:])
                )
    print("Source-archive build and website tests passed without Git metadata")


if __name__ == "__main__":
    main()
