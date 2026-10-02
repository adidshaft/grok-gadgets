"""Inspect/verify by default. Install only when explicitly passed --install."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parent


def verify(root=ROOT):
    manifest = json.loads((root / "manifest.json").read_text())
    if (
        not isinstance(manifest, dict)
        or manifest.get("format_version") != 1
        or type(manifest.get("format_version")) is not int
    ):
        raise ValueError("Unsupported kit manifest version")
    if not isinstance(manifest.get("gateway_commit"), str) or not re.fullmatch(
        r"[0-9a-f]{40}", manifest["gateway_commit"]
    ):
        raise ValueError("Invalid gateway source commit")
    if (
        not isinstance(manifest.get("files"), list)
        or not 10 <= len(manifest["files"]) <= 20
    ):
        raise ValueError("Invalid kit inventory")
    names = set()
    for record in manifest["files"]:
        if (
            not isinstance(record, dict)
            or set(record) != {"file", "bytes", "sha256"}
            or not isinstance(record["file"], str)
        ):
            raise ValueError("Invalid file record")
        name = PurePosixPath(record["file"])
        if (
            name.is_absolute()
            or len(name.parts) != 1
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", record["file"])
            or ".." in name.parts
            or "\\" in str(name)
        ):
            raise ValueError("Unsafe manifest filename")
        if str(name) in names:
            raise ValueError("Duplicate kit filename")
        names.add(str(name))
        if (
            type(record["bytes"]) is not int
            or record["bytes"] < 0
            or not isinstance(record["sha256"], str)
        ):
            raise ValueError("Invalid file size/hash")
        path = root / str(name)
        if (
            path.is_symlink()
            or not path.is_file()
            or not path.resolve().is_relative_to(root.resolve())
        ):
            raise ValueError(f"Missing/unsafe kit file: {name}")
        if not re.fullmatch(r"[0-9a-f]{64}", record["sha256"]):
            raise ValueError("Invalid SHA256")
        if (
            path.stat().st_size != record["bytes"]
            or hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]
        ):
            raise ValueError(f"Hash mismatch: {name}")
    required = {
        "requirements.txt",
        "LICENSE",
        "NOTICE",
        "README.md",
        "source.tar",
        "install.py",
        "try_simulator.py",
        "simulator-config.json",
        "simulator-config.schema.json",
    }
    wheels = [name for name in names if name.endswith(".whl")]
    if (
        not required <= names
        or len(wheels) != 1
        or not wheels[0].startswith("grok_gadgets_gateway-")
    ):
        raise ValueError("Missing/ambiguous required kit files")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--install",
        action="store_true",
        help="Create .venv and download hashed runtime dependencies",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "simulator-config.json",
        help="Your exported configuration; not executed as code",
    )
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        parser.error("Python 3.11 or newer is required")
    manifest = verify()
    print(
        f"Verified {len(manifest['files'])} kit files. Gateway source: {manifest['gateway_commit']}"
    )
    if not args.install:
        print(
            "Nothing installed or started. Inspect README.md, source.tar, requirements.txt and this script. Then use --install if desired."
        )
        return
    config = args.config.resolve(strict=True)
    env = ROOT / ".venv"
    if env.exists():
        parser.error(
            ".venv already exists. This installer will not modify an existing environment. Use a fresh extracted kit."
        )
    venv.EnvBuilder(with_pip=True).create(env)
    python = env / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "--isolated",
            "install",
            "--only-binary=:all:",
            "--require-hashes",
            "-r",
            str(ROOT / "requirements.txt"),
        ],
        check=True,
    )
    wheel = next(
        record["file"]
        for record in manifest["files"]
        if record["file"].endswith(".whl")
    )
    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "--isolated",
            "install",
            "--no-deps",
            str(ROOT / wheel),
        ],
        check=True,
    )
    command = env / (
        "Scripts/grok-gadgets-gateway.exe"
        if sys.platform == "win32"
        else "bin/grok-gadgets-gateway"
    )
    print(
        "Installed; no server started and no connector registered. Command MCP configuration on THIS host:"
    )
    print(
        json.dumps(
            {
                "command": str(command),
                "args": ["--simulator", "--simulator-config", str(config)],
                "env": {},
            },
            indent=2,
        )
    )
    print(
        "The Grok cloud computer requires its own installation and paths. See README.md."
    )


if __name__ == "__main__":
    main()
