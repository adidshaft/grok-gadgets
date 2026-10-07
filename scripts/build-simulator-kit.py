"""Build an inspectable offline-shareable kit from exact committed gateway source."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
GATEWAY = ROOT.parent / "grok-gadgets-gateway"
ARCHIVE = "grok-gadgets-simulator-kit.zip"
# Gateway paths that shape the kit. CI-only or planning commits leave the kit current.
GATEWAY_INPUTS = (
    "LICENSE",
    "NOTICE",
    "README.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
    "protocol",
    "pyproject.toml",
    "src",
    "tests",
    "uv.lock",
)


def run(args, cwd=None, env=None):
    return subprocess.check_output(args, cwd=cwd, env=env, text=True).strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs():
    paths = [
        Path(__file__).resolve(),
        *sorted(
            path
            for path in (ROOT / "scripts/simulator-kit").iterdir()
            if path.suffix in {".py", ".md"}
        ),
    ]
    return {str(path.relative_to(ROOT)): digest(path) for path in paths}


def gateway_inputs(revision="HEAD"):
    """Hash the committed gateway files that the kit is built from."""
    listing = run(
        ["git", "ls-tree", "-r", "--full-tree", revision, "--", *GATEWAY_INPUTS],
        cwd=GATEWAY,
    )
    return hashlib.sha256(listing.encode()).hexdigest()


def verify_download(output, expected_gateway_inputs=None):
    record = json.loads((output / "simulator-kit-manifest.json").read_text())
    if (
        not isinstance(record, dict)
        or not isinstance(record.get("files"), list)
        or not all(
            isinstance(entry, dict)
            and set(entry) == {"file", "bytes", "sha256"}
            and isinstance(entry["file"], str)
            and isinstance(entry["bytes"], int)
            and isinstance(entry["sha256"], str)
            for entry in record["files"]
        )
    ):
        raise ValueError("Malformed simulator kit manifest")
    if record.get("build_inputs") != inputs():
        raise ValueError("Simulator kit inputs changed; rebuild required")
    if (
        expected_gateway_inputs
        and record.get("gateway_inputs") != expected_gateway_inputs
    ):
        raise ValueError("Simulator kit gateway source changed; rebuild required")
    if record.get("verification") != {
        "gateway_tests": "passed",
        "installed_mcp_default": "passed",
        "installed_mcp_custom": "passed",
    }:
        raise ValueError("Simulator kit lacks successful build acceptance")
    archive = output / ARCHIVE
    if digest(archive) != record["archive_sha256"]:
        raise ValueError("Simulator kit archive checksum mismatch")
    with zipfile.ZipFile(archive) as bundle:
        prefix = "grok-gadgets-simulator-kit/"
        manifest = json.loads(bundle.read(prefix + "manifest.json"))
        if not isinstance(manifest, dict):
            raise ValueError("Malformed simulator kit inner manifest")
        if any(
            manifest.get(key) != record.get(key)
            for key in [
                "files",
                "gateway_commit",
                "gateway_inputs",
                "package_version",
                "build_inputs",
                "verification",
            ]
        ):
            raise ValueError("Simulator kit inner provenance mismatch")
        expected_names = {prefix + entry["file"] for entry in record["files"]} | {
            prefix + "manifest.json",
            prefix + "SHA256SUMS",
        }
        if set(bundle.namelist()) != expected_names or len(bundle.namelist()) != len(
            expected_names
        ):
            raise ValueError("Simulator kit archive inventory mismatch")
        for entry in record["files"]:
            content = bundle.read(prefix + entry["file"])
            if (
                len(content) != entry["bytes"]
                or hashlib.sha256(content).hexdigest() != entry["sha256"]
            ):
                raise ValueError("Simulator kit inner checksum mismatch")
    return record


def assert_source_unchanged(expected_gateway_inputs, captured_inputs):
    if inputs() != captured_inputs:
        raise ValueError(
            "Simulator kit inputs changed during verification; retry the build"
        )
    if (GATEWAY / ".git").exists() and gateway_inputs() != expected_gateway_inputs:
        raise ValueError("Gateway source changed during verification; retry the build")


def ensure_current(output, rebuild=True):
    """Verify the kit against the sibling gateway's HEAD, rebuilding when allowed.

    Without a gateway checkout only the download's own integrity is checked.
    """
    captured_inputs = inputs()
    expected = gateway_inputs() if (GATEWAY / ".git").exists() else None
    try:
        record = verify_download(output, expected)
    except (ValueError, OSError, KeyError, zipfile.BadZipFile):
        if not rebuild or expected is None:
            raise ValueError(
                "Current verified simulator kit unavailable; "
                "run python3 scripts/build-simulator-kit.py with the gateway beside the hub"
            ) from None
        build(output)
        record = verify_download(output, expected)
    assert_source_unchanged(record["gateway_inputs"], captured_inputs)
    return record


def promote_download(output, staged_archive, record):
    """Validate a complete pair first; restore the previous pair on write errors."""
    output.mkdir(parents=True, exist_ok=True)
    names = [ARCHIVE, "simulator-kit-manifest.json"]
    with tempfile.TemporaryDirectory(
        prefix="kit-promotion-", dir=output.parent
    ) as directory:
        directory = Path(directory)
        candidate = directory / "candidate"
        backup = directory / "backup"
        candidate.mkdir()
        backup.mkdir()
        shutil.copyfile(staged_archive, candidate / ARCHIVE)
        (candidate / names[1]).write_text(json.dumps(record, indent=2) + "\n")
        verify_download(candidate, record["gateway_inputs"])
        assert_source_unchanged(record["gateway_inputs"], record["build_inputs"])
        previous = set()
        for name in names:
            if (output / name).exists():
                shutil.copyfile(output / name, backup / name)
                previous.add(name)
        promoted = []
        try:
            for name in names:
                (candidate / name).replace(output / name)
                promoted.append(name)
        except Exception:
            for name in promoted:
                if name in previous:
                    (backup / name).replace(output / name)
                else:
                    (output / name).unlink(missing_ok=True)
            raise


def build(output):
    captured_inputs = inputs()
    if run(["git", "status", "--porcelain"], cwd=GATEWAY):
        raise ValueError(
            "Gateway must have a clean committed checkout before kit generation"
        )
    commit = run(["git", "rev-parse", "HEAD"], cwd=GATEWAY)
    source_inputs = gateway_inputs(commit)
    epoch = run(["git", "show", "-s", "--format=%ct", "HEAD"], cwd=GATEWAY)
    with tempfile.TemporaryDirectory(prefix="grok-simulator-kit-") as tmp:
        work = Path(tmp)
        source = work / "source"
        source.mkdir()
        # Only the committed kit inputs; no .git, CI, planning or untracked files.
        archive = work / "source.tar"
        present = run(
            ["git", "ls-tree", "--name-only", commit, "--", *GATEWAY_INPUTS],
            cwd=GATEWAY,
        ).splitlines()
        subprocess.run(
            ["git", "archive", "--format=tar", f"--output={archive}", commit, *present],
            cwd=GATEWAY,
            check=True,
        )
        import tarfile

        with tarfile.open(archive) as tar:
            tar.extractall(source, filter="data")
        kit = work / "kit"
        kit.mkdir()
        shutil.copy(archive, kit / "source.tar")
        env = {**os.environ, "SOURCE_DATE_EPOCH": epoch}
        subprocess.run(
            ["uv", "run", "--locked", "--python", "3.11", "pytest", "-q"],
            cwd=source,
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["uv", "build", "--no-sources", "--out-dir", str(work / "packages")],
            cwd=source,
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        for path in (work / "packages").iterdir():
            if path.suffix == ".whl" or path.name.endswith(".tar.gz"):
                shutil.copy(path, kit / path.name)
        requirements = run(
            [
                "uv",
                "export",
                "--frozen",
                "--no-dev",
                "--no-emit-project",
                "--format",
                "requirements-txt",
            ],
            cwd=source,
        )
        (kit / "requirements.txt").write_text(
            "# Hashed runtime dependencies exported from the included uv.lock.\n"
            + "\n".join(
                line for line in requirements.splitlines() if not line.startswith("#")
            )
            + "\n"
        )
        for name in ["LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md"]:
            if (source / name).is_file():
                shutil.copy(source / name, kit / name)
        for name in ["simulator-config.json", "simulator-config.schema.json"]:
            shutil.copy(source / "src/grok_gadgets_gateway" / name, kit / name)
        for path in (ROOT / "scripts/simulator-kit").iterdir():
            if path.suffix in [".py", ".md"]:
                shutil.copy(path, kit / path.name)
        records = [
            {"file": path.name, "bytes": path.stat().st_size, "sha256": digest(path)}
            for path in sorted(kit.iterdir())
        ]
        manifest = {
            "format_version": 1,
            "gateway_commit": commit,
            "gateway_commit_epoch": int(epoch),
            "gateway_inputs": source_inputs,
            "package_version": tomllib.loads((source / "pyproject.toml").read_text())[
                "project"
            ]["version"],
            "build_inputs": captured_inputs,
            "verification": {
                "gateway_tests": "passed",
                "installed_mcp_default": "passed",
                "installed_mcp_custom": "passed",
            },
            "status": "Public simulator kit built from gateway main; software simulation only, no hardware or Grok Bot verification",
            "files": records,
        }
        (kit / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        (kit / "SHA256SUMS").write_text(
            "".join(
                f"{digest(path)}  {path.name}\n"
                for path in sorted(kit.iterdir())
                if path.name != "SHA256SUMS"
            )
        )
        # Exercise the actual installer/wheel in an extracted copy, never the checkout environment.
        acceptance = work / "acceptance"
        shutil.copytree(kit, acceptance)
        source_python = (
            source
            / ".venv"
            / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        )
        clean_env = {
            key: value
            for key, value in env.items()
            if key not in {"PYTHONPATH", "PYTHONHOME"}
        }
        subprocess.run(
            [str(source_python), str(acceptance / "install.py"), "--install"],
            cwd=acceptance,
            env=clean_env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        installed_python = (
            acceptance
            / ".venv"
            / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        )
        subprocess.run(
            [str(installed_python), "try_simulator.py"],
            cwd=acceptance,
            env=clean_env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        custom = {
            "schema_version": 1,
            "device_id": "kit-check",
            "display_name": "Kit check",
            "initial_rgb": {"r": 26, "g": 51, "b": 128, "on": True},
            "response_delay_ms": 25,
            "start_disconnected": True,
        }
        (acceptance / "custom.json").write_text(json.dumps(custom))
        subprocess.run(
            [str(installed_python), "try_simulator.py", "--config", "custom.json"],
            cwd=acceptance,
            env=clean_env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        staging = work / ARCHIVE
        with zipfile.ZipFile(
            staging, "w", zipfile.ZIP_DEFLATED, compresslevel=9
        ) as bundle:
            for path in sorted(kit.iterdir()):
                info = zipfile.ZipInfo(
                    "grok-gadgets-simulator-kit/" + path.name,
                    date_time=(2020, 1, 1, 0, 0, 0),
                )
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                bundle.writestr(info, path.read_bytes())
        assert_source_unchanged(source_inputs, captured_inputs)
        record = {
            **manifest,
            "archive": ARCHIVE,
            "archive_bytes": staging.stat().st_size,
            "archive_sha256": digest(staging),
        }
        promote_download(output, staging, record)
        print(
            json.dumps(
                {
                    "archive": str(output / ARCHIVE),
                    "sha256": record["archive_sha256"],
                    "gateway_commit": commit,
                },
                indent=2,
            )
        )
        return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "website/downloads")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="Fail if the kit is stale, unverified or corrupt; do not rebuild",
    )
    mode.add_argument(
        "--ensure",
        action="store_true",
        help="Keep a current kit; rebuild only when the gateway inputs changed",
    )
    args = parser.parse_args()
    if args.check or args.ensure:
        record = ensure_current(args.output.resolve(), rebuild=args.ensure)
        print(
            "Simulator kit is current, verified and hash checked (gateway "
            + record["gateway_commit"][:8]
            + ")"
        )
    else:
        build(args.output.resolve())
