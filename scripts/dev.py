"""One entry point for hub development.

python3 scripts/dev.py setup   create .venv and install pinned tools
python3 scripts/dev.py check   run every hub check (same as CI)
python3 scripts/dev.py site    build the website and serve it on 127.0.0.1:4173
"""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / ".venv"
PY = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
RUFF = "ruff==0.14.14"


def run(*command):
    result = subprocess.run([str(c) for c in command], cwd=ROOT)
    if result.returncode:
        raise SystemExit(result.returncode)


def setup():
    # One hub Python everywhere (README, CI, deploy): 3.13. uv fetches it when missing.
    uv = shutil.which("uv")
    if not uv and sys.version_info < (3, 13):
        raise SystemExit(
            "Python 3.13 or newer is required (or install uv, which fetches it)"
        )
    if not PY.exists():
        if uv:
            run(uv, "venv", VENV, "--python", "3.13")
        else:
            run(sys.executable, "-m", "venv", VENV)
    requirements = ROOT / "website/requirements.txt"
    if uv:
        run(uv, "pip", "install", "--python", PY, "-r", requirements, RUFF)
    else:
        run(PY, "-m", "pip", "install", "-r", requirements, RUFF)
    if not shutil.which("node"):
        print("Optional: install Node.js 22+ to run the browser simulator tests.")
    print("Ready. Next: python3 scripts/dev.py check")


def check():
    if not PY.exists():
        setup()
    run(PY, "scripts/check.py")


def site(port):
    if not PY.exists():
        setup()
    run(PY, "website/build.py")
    print(f"Open http://127.0.0.1:{port}/ (Ctrl+C to stop)")
    try:
        run(
            PY,
            "-m",
            "http.server",
            port,
            "--bind",
            "127.0.0.1",
            "--directory",
            "website/dist",
        )
    except KeyboardInterrupt:
        pass


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("setup", help="create .venv and install pinned tools")
    sub.add_parser("check", help="run every hub check")
    serve = sub.add_parser("site", help="build and serve the website locally")
    serve.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()
    if args.command == "setup":
        setup()
    elif args.command == "check":
        check()
    else:
        site(args.port)


if __name__ == "__main__":
    main()
