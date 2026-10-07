"""Run the hub checks: the same steps as CI. Use --quick for structure only."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

root = Path(__file__).resolve().parents[1]
STAGES = ["proposed", "ready", "in progress", "review", "blocked", "done"]
ISSUE_KEYS = [
    "repository",
    "problem",
    "acceptance",
    "dependencies",
    "labels",
    "milestone",
    "commits",
    "evidence",
]


def fail(message):
    raise SystemExit("Check failed: " + message)


def structural():
    for name in [
        "LICENSE",
        "README.md",
        "AGENTS.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
    ]:
        if not (root / name).is_file():
            fail("missing " + name)
    issues = json.loads((root / "planning/issues.json").read_text())
    if len({i["id"] for i in issues}) != len(issues):
        fail("duplicate issue IDs in planning/issues.json")
    for i in issues:
        if i["stage"] not in STAGES:
            fail(i["id"] + " has unknown stage " + repr(i["stage"]))
        missing = [k for k in ISSUE_KEYS if k not in i]
        if missing:
            fail(i["id"] + " lacks " + ", ".join(missing))
        if len(i["labels"]) < 3:
            fail(i["id"] + " needs at least three labels")
    print(f"Hub foundation and {len(issues)} labeled issue records verified")
    for source in [
        *root.joinpath("scripts").glob("*.py"),
        *root.joinpath("website").glob("*.py"),
        *root.joinpath("community").rglob("*.py"),
    ]:
        compile(source.read_text(), str(source), "exec")
    print("Python source syntax verified")


def python():
    venv = root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return str(venv) if venv.exists() else sys.executable


def steps(py):
    ruff = [py, "-m", "ruff"]
    return [
        ("Browser simulator", ["node", "--test", "website/test_simulator.cjs"]),
        ("Simulator kit is current", [py, "scripts/build-simulator-kit.py", "--check"]),
        ("Simulator kit tests", [py, "scripts/test_simulator_kit.py"]),
        (
            "Script tests",
            [py, "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"],
        ),
        (
            "Community tests",
            [py, "-m", "unittest", "discover", "-s", "community/tests"],
        ),
        (
            "Website tests",
            [py, "-m", "unittest", "discover", "-s", "website", "-p", "test_*.py"],
        ),
        ("Website build", [py, "website/build.py"]),
        ("Build from a ZIP download", [py, "scripts/check-archive-build.py"]),
        ("Public URL prefix", [py, "scripts/check-pages-prefix.py"]),
        (
            "Plain language (ASD-STE100 sentence limit)",
            [
                py,
                "scripts/check_ste.py",
                "README.md",
                "CONTRIBUTING.md",
                "SUPPORT.md",
                "docs/public/support-matrix.md",
                "docs/getting-started/simulator-kit.md",
                "docs/getting-started/hosting.md",
                "docs/getting-started/physical-test.md",
                "docs/contributing/ready-issues.md",
                "docs/contributing/writing-guide.md",
            ],
        ),
        ("Lint", [*ruff, "check", "scripts", "website", "community"]),
        ("Format", [*ruff, "format", "--check", "scripts", "website", "community"]),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="Structure only (seconds)")
    args = parser.parse_args()
    if sys.flags.optimize:
        fail("run without python -O; checks must not be optimized away")
    structural()
    if args.quick:
        return
    py = python()
    probe = subprocess.run(
        [py, "-c", "import markdown_it, yaml, ruff"], capture_output=True, cwd=root
    )
    if probe.returncode:
        fail("dependencies missing. Run: python3 scripts/dev.py setup")
    in_ci = os.environ.get("CI") == "true"
    failed, skipped = [], []
    for title, command in steps(py):
        if shutil.which(command[0]) is None and not Path(command[0]).exists():
            skipped.append(title)
            print(f"SKIP  {title} ({command[0]} is not installed)")
            continue
        started = time.monotonic()
        result = subprocess.run(command, cwd=root, capture_output=True, text=True)
        seconds = time.monotonic() - started
        if result.returncode:
            failed.append(title)
            print(f"FAIL  {title} ({seconds:.0f}s)")
            print((result.stdout + result.stderr)[-3000:])
        else:
            print(f"PASS  {title} ({seconds:.0f}s)")
    if failed or (skipped and in_ci):
        fail(", ".join(failed + skipped))
    if skipped:
        print("Passed, but some steps were skipped: " + ", ".join(skipped))
    else:
        print("All hub checks passed")


if __name__ == "__main__":
    main()
