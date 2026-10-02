"""Build a verified, unpublished candidate from committed sources; no external actions."""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
REPOSITORIES = (
    "grok-gadgets",
    "grok-gadgets-gateway",
    "grok-gadgets-linux-sdk",
    "grok-gadgets-esp32-sdk",
    "grok-gadgets-home-assistant",
)
PYTHON_REPOSITORIES = (
    "grok-gadgets-gateway",
    "grok-gadgets-linux-sdk",
    "grok-gadgets-home-assistant",
)


def run(args, *, cwd=None):
    return subprocess.check_output(
        args, cwd=cwd, text=True, stderr=subprocess.PIPE
    ).strip()


def git(repo, *args):
    return run(["git", "-C", str(repo), *args])


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def verifier():
    spec = importlib.util.spec_from_file_location(
        "publication_verifier", ROOT / "scripts/verify-publication.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inspect_sources(root):
    sources = {}
    for name in REPOSITORIES:
        repo = root if name == "grok-gadgets" else root.parent / name
        # Preserve the user's untracked brand assets, but never include them in Git archives.
        dirty = git(repo, "status", "--porcelain").splitlines()
        unexpected = [
            line
            for line in dirty
            if not (name == "grok-gadgets" and line == "?? assets/")
        ]
        if unexpected:
            raise ValueError(f"{name}: commit intended source changes before packaging")
        sources[name] = {
            "source_commit": git(repo, "rev-parse", "HEAD"),
            "branch": git(repo, "branch", "--show-current"),
            "source_dirty": False,
        }
    return sources


def add_record(records, destination, *, repository, kind, source_commit, **extra):
    records.append(
        {
            "repository": repository,
            "kind": kind,
            "source_commit": source_commit,
            "file": destination.name,
            "bytes": destination.stat().st_size,
            "sha256": sha256(destination),
            **extra,
        }
    )


def build_python(repo, source, archive, out, records, validator):
    """Ignore old dist outputs: build wheel and sdist from the exact archived HEAD."""
    python = repo / ".venv/bin/python"
    if not python.is_file():
        raise ValueError(f"{repo.name}: existing pinned Python environment required")
    with tempfile.TemporaryDirectory(prefix="grok-candidate-build-") as temporary:
        temporary = Path(temporary)
        with tarfile.open(archive) as source_archive:
            source_archive.extractall(temporary, filter="data")
        extracted = temporary / repo.name
        built = temporary / "dist"
        command = [
            "uv",
            "build",
            "--offline",
            "--no-python-downloads",
            "--python",
            str(python),
            "--out-dir",
            str(built),
            str(extracted),
        ]
        run(command, cwd=extracted)
        packages = sorted(built.glob("*.whl")) + sorted(built.glob("*.tar.gz"))
        if len(packages) != 2:
            raise ValueError(f"{repo.name}: expected exactly one wheel and one sdist")
        for package in packages:
            validator.validate_python_package(package, repo, source)
            destination = out / package.name
            shutil.copy2(package, destination)
            add_record(
                records,
                destination,
                repository=repo.name,
                kind="python_package",
                source_commit=source,
            )
        environment = json.loads(
            run(
                [
                    str(python),
                    "-c",
                    "import json,platform; print(json.dumps({'python':platform.python_version(),'platform':platform.platform()}))",
                ]
            )
        )
        provenance = {
            "source_commit": source,
            "source_dirty": False,
            "build_command": "uv build --offline --no-python-downloads --python <existing-pinned-env> <exact-Git-archive>",
            "built_at_utc": datetime.now(timezone.utc).isoformat(),
            "environment": environment,
            "uv": run(["uv", "--version"]),
            "build_configuration_sha256": hashlib.sha256(
                subprocess.check_output(
                    ["git", "-C", str(repo), "show", source + ":pyproject.toml"]
                )
            ).hexdigest(),
            "artifacts": {p.name: sha256(p) for p in packages},
        }
        destination = out / (repo.name + "-build-provenance.json")
        write_json(destination, provenance)
        add_record(
            records,
            destination,
            repository=repo.name,
            kind="build_provenance",
            source_commit=source,
        )


def copy_firmware(repo, head, out, records, validator):
    directory = repo / "artifacts/c124-usb"
    manifest = json.loads((directory / "manifest.json").read_text())
    validator.validate_firmware_provenance(manifest, repo, head)
    source = manifest["source_commit"]
    required = {"firmware.bin", "firmware.elf", "bootloader.bin", "partitions.bin"}
    if set(manifest["files"]) != required:
        raise ValueError(
            "Firmware provenance must identify exactly the four supported build files"
        )
    for name, evidence in manifest["files"].items():
        path = directory / name
        if (
            sha256(path) != evidence["sha256"]
            or path.stat().st_size != evidence["bytes"]
        ):
            raise ValueError(f"Firmware provenance hash/size mismatch: {name}")
        destination = out / ("c124-" + name)
        shutil.copy2(path, destination)
        add_record(
            records,
            destination,
            repository=repo.name,
            kind="firmware",
            source_commit=source,
            repository_head=head,
            status="Build verified; physical/Grok pending; unpublished",
        )
    destination = out / "c124-manifest.json"
    write_json(destination, manifest)
    add_record(
        records,
        destination,
        repository=repo.name,
        kind="firmware_provenance",
        source_commit=source,
        repository_head=head,
    )


def prepare(root=ROOT, output=None):
    validator = verifier()
    sources = inspect_sources(root)
    # Validate firmware before any candidate output is created; stale source must fail closed.
    firmware_repo = root.parent / "grok-gadgets-esp32-sdk"
    firmware = json.loads(
        (firmware_repo / "artifacts/c124-usb/manifest.json").read_text()
    )
    validator.validate_firmware_provenance(
        firmware, firmware_repo, sources[firmware_repo.name]["source_commit"]
    )
    output = output or root / "artifacts/publication"
    output.mkdir(parents=True, exist_ok=True)
    run_id = (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + str(time.time_ns())
    )
    final = output / run_id
    # Unique staging output avoids overwriting any earlier successful candidate.
    staging = Path(tempfile.mkdtemp(prefix=".candidate-", dir=output))
    records = []
    try:
        for name, evidence in sources.items():
            repo = root if name == "grok-gadgets" else root.parent / name
            source = evidence["source_commit"]
            archive = staging / (name + "-" + source[:12] + ".tar.gz")
            run(
                [
                    "git",
                    "-C",
                    str(repo),
                    "archive",
                    "--format=tar.gz",
                    "--prefix=" + name + "/",
                    "-o",
                    str(archive),
                    source,
                ]
            )
            add_record(
                records,
                archive,
                repository=name,
                kind="source_archive",
                source_commit=source,
            )
            bundle = staging / (name + ".bundle")
            run(["git", "-C", str(repo), "bundle", "create", str(bundle), "--all"])
            run(["git", "-C", str(repo), "bundle", "verify", str(bundle)])
            add_record(
                records,
                bundle,
                repository=name,
                kind="git_bundle",
                source_commit=source,
            )
            if name in PYTHON_REPOSITORIES:
                build_python(repo, source, archive, staging, records, validator)
        copy_firmware(
            firmware_repo,
            sources[firmware_repo.name]["source_commit"],
            staging,
            records,
            validator,
        )
        # Rebuild the website after its source is committed, rather than reusing an old dist tree.
        run([sys.executable, str(root / "website/build.py")], cwd=root)
        site = staging / "website-static.tar.gz"
        with tarfile.open(site, "w:gz") as archive:
            archive.add(root / "website/dist", arcname="website")
        add_record(
            records,
            site,
            repository="grok-gadgets",
            kind="website",
            source_commit=sources["grok-gadgets"]["source_commit"],
            build_command="python3 website/build.py",
        )
        if inspect_sources(root) != sources:
            raise ValueError(
                "Repository source changed while candidate was being built"
            )
        write_json(
            staging / "manifest.json",
            {
                "format_version": 2,
                "run_id": run_id,
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "status": "unpublished local candidate",
                "version": "0.1.0-alpha.1",
                "repositories": sources,
                "artifacts": records,
                "limitations": [
                    "Actual Grok, physical hardware and independent human testing pending",
                    "No public repositories, release uploads or public gateway/site deployment performed; separately authorized Grok simulator Bot setup recorded",
                ],
            },
        )
        # Manifest's digest lives outside itself, avoiding future commit/hash self-reference.
        sums = [(r["file"], r["sha256"]) for r in records] + [
            ("manifest.json", sha256(staging / "manifest.json"))
        ]
        (staging / "SHA256SUMS").write_text(
            "".join(digest + "  " + name + "\n" for name, digest in sorted(sums))
        )
        validator.verify_candidate(staging, root)
        staging.rename(final)
        pointer = output / (".latest-" + run_id + ".json")
        write_json(
            pointer,
            {
                "run_id": run_id,
                "directory": run_id,
                "manifest_sha256": sha256(final / "manifest.json"),
            },
        )
        pointer.replace(output / "latest.json")
        print(f"Prepared and verified {len(records)} unpublished files at {final}")
        return final
    except Exception:
        shutil.rmtree(staging)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        help="Candidate history directory (default artifacts/publication)",
    )
    args = parser.parse_args()
    try:
        prepare(output=args.output.resolve() if args.output else None)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        if isinstance(exc, subprocess.CalledProcessError):
            print(
                f"Candidate preparation failed: {exc.cmd[0]} exited {exc.returncode}",
                file=sys.stderr,
            )
        else:
            print(f"Candidate preparation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
