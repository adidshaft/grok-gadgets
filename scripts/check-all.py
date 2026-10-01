"""Run local component checks, preserving output and exact source commits."""

import os
from pathlib import Path
import subprocess
import json
import time
import sys
import hashlib
from datetime import datetime, timezone

root = Path(__file__).resolve().parents[1]
run_id = (
    datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + str(time.time_ns())
)
out = root / "artifacts/verification" / run_id
out.mkdir(parents=True, exist_ok=True)
jobs = [
    ("hub", root, [sys.executable, "scripts/check.py"]),
    ("website", root, [sys.executable, "website/build.py"]),
    (
        "activity",
        root,
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
    ),
    (
        "community",
        root,
        [sys.executable, "-m", "unittest", "discover", "-s", "community/tests"],
    ),
    ("gateway", root.parent / "grok-gadgets-gateway", ["uv", "run", "pytest"]),
    (
        "mcp-demo",
        root.parent / "grok-gadgets-gateway",
        ["uv", "run", "python", "-m", "grok_gadgets_gateway.demo"],
    ),
    (
        "linux",
        root.parent / "grok-gadgets-linux-sdk",
        ["uv", "run", "python", "-m", "unittest", "discover", "-s", "tests", "-v"],
    ),
    (
        "home-assistant",
        root.parent / "grok-gadgets-home-assistant",
        ["uv", "run", "python", "-m", "unittest", "discover", "-s", "tests", "-v"],
    ),
    (
        "installed-custom-onboarding",
        root,
        [sys.executable, "scripts/check-installed-onboarding.py"],
    ),
    ("esp32-host", root.parent / "grok-gadgets-esp32-sdk", ["sh", "tools/check.sh"]),
    (
        "esp32-contract",
        root.parent / "grok-gadgets-esp32-sdk",
        [".venv/bin/python", "tools/check_contract.py"],
    ),
    (
        "esp32-usb-integration",
        root.parent / "grok-gadgets-esp32-sdk",
        ["../grok-gadgets-gateway/.venv/bin/python", "tools/check_gateway.py"],
    ),
]

results = []
for name, cwd, command in jobs:
    env = os.environ.copy()
    env["GROK_GATEWAY_SOURCE"] = str(root.parent / "grok-gadgets-gateway/src")
    started_at = datetime.now(timezone.utc).isoformat()
    status_before = subprocess.check_output(
        ["git", "-C", str(cwd), "status", "--porcelain"], text=True
    ).splitlines()
    tracked_diff = subprocess.check_output(
        ["git", "-C", str(cwd), "diff", "HEAD", "--binary"]
    )
    start = time.monotonic()
    r = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )
    (out / (name + ".log")).write_text(r.stdout)
    commit = subprocess.check_output(
        ["git", "-C", str(cwd), "rev-parse", "HEAD"], text=True
    ).strip()
    results.append(
        dict(
            check=name,
            repository=cwd.name,
            commit=commit,
            command=command,
            started_at_utc=started_at,
            python=sys.version.split()[0],
            status_before=status_before,
            tracked_clean=not any(not line.startswith("??") for line in status_before),
            tracked_diff_sha256=hashlib.sha256(tracked_diff).hexdigest(),
            status_after=subprocess.check_output(
                ["git", "-C", str(cwd), "status", "--porcelain"], text=True
            ).splitlines(),
            exit_code=r.returncode,
            seconds=round(time.monotonic() - start, 2),
            log=str((out / (name + ".log")).relative_to(root)),
        )
    )
    print(f"{name}: " + ("PASS" if r.returncode == 0 else "FAIL"), flush=True)
    if r.returncode:
        print(r.stdout)
(out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
(root / "artifacts/verification/latest.json").write_text(
    json.dumps(
        {"run_id": run_id, "results": str((out / "results.json").relative_to(root))},
        indent=2,
    )
    + "\n"
)
sys.exit(any(x["exit_code"] for x in results))
