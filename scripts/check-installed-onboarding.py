"""Fresh installed-wheel custom example acceptance; bounded local gateway, no source imports."""

from pathlib import Path
import os
import subprocess
import tempfile
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SDK = ROOT.parent / "grok-gadgets-linux-sdk"
GATEWAY = ROOT.parent / "grok-gadgets-gateway"
with tempfile.TemporaryDirectory(prefix="grok-installed-") as directory:
    envdir = Path(directory) / "venv"
    command_env = dict(os.environ)
    command_env.pop("PYTHONPATH", None)
    command_env.pop("PYTHONHOME", None)
    subprocess.run(
        ["uv", "venv", str(envdir), "--python", str(SDK / ".venv/bin/python")],
        check=True,
        env=command_env,
        capture_output=True,
    )
    python = envdir / "bin/python"
    wheels = [next(repo.glob("dist/*.whl")) for repo in [SDK, GATEWAY]]
    subprocess.run(
        [
            "uv",
            "pip",
            "install",
            "--offline",
            "--python",
            str(python),
            *map(str, wheels),
        ],
        check=True,
        env=command_env,
        capture_output=True,
    )
    result = subprocess.run(
        [
            str(python),
            "-I",
            str(SDK / "scripts/check_onboarding.py"),
            str(SDK / "docs/development.md"),
        ],
        check=True,
        env=command_env,
        cwd=directory,
        capture_output=True,
        text=True,
        timeout=30,
    )
    print(result.stdout)
    print(
        json.dumps(
            {
                "installed_wheels": [
                    dict(file=p.name, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                    for p in wheels
                ]
            }
        )
    )
