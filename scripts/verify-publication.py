"""Verify an unpublished candidate's hashes, exact sources, packages and Git histories."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPOSITORIES = {
    "grok-gadgets",
    "grok-gadgets-gateway",
    "grok-gadgets-linux-sdk",
    "grok-gadgets-esp32-sdk",
    "grok-gadgets-home-assistant",
}
PYTHON_REPOSITORIES = REPOSITORIES - {"grok-gadgets", "grok-gadgets-esp32-sdk"}
FIRMWARE_EVIDENCE_PATHS = {
    "docs/build-checksums.json",
    "planning/issues.json",
    "planning/issues.md",
    "CHANGELOG.md",
}


def git(repo, *args):
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], stderr=subprocess.PIPE
    )


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_commit(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{40}", value):
        raise ValueError("Source provenance requires a full Git commit")
    return value


def safe_filename(value):
    if (
        not isinstance(value, str)
        or Path(value).name != value
        or value in ("", ".", "..")
    ):
        raise ValueError("Artifact filename must be a single safe path component")
    return value


def source_payloads(repo, commit):
    valid_commit(commit)
    files = git(repo, "ls-tree", "-r", "--name-only", commit).decode().splitlines()
    # Every packaged runtime file is compared with the recorded Git source, not a live checkout.
    return {
        name: git(repo, "show", commit + ":" + name)
        for name in files
        if name.startswith(("src/", "protocol/"))
        or name in ("pyproject.toml", "README.md", "LICENSE")
    }


def validate_python_package(package, repo, commit):
    payloads = source_payloads(repo, commit)
    if not any(name.startswith("src/") for name in payloads):
        raise ValueError("Python package has no committed runtime payload")
    if package.suffix == ".whl":
        with zipfile.ZipFile(package) as archive:
            expected = {}
            for name, data in payloads.items():
                if name.startswith("src/"):
                    expected[name.removeprefix("src/")] = data
                elif (
                    name.startswith("protocol/") and repo.name == "grok-gadgets-gateway"
                ):
                    expected["grok_gadgets_gateway/" + name] = data
            for name, data in expected.items():
                if name not in archive.namelist() or archive.read(name) != data:
                    raise ValueError(f"Wheel source mismatch: {repo.name}/{name}")
            actual_runtime = {
                name
                for name in archive.namelist()
                if not name.endswith("/") and ".dist-info/" not in name
            }
            if actual_runtime != set(expected):
                raise ValueError(
                    f"Wheel has unexpected or missing runtime files: {repo.name}"
                )
    elif package.name.endswith(".tar.gz"):
        with tarfile.open(package) as archive:
            roots = {
                PurePosixPath(member.name).parts[0] for member in archive.getmembers()
            }
            if len(roots) != 1:
                raise ValueError("sdist requires one root directory")
            prefix = next(iter(roots)) + "/"
            for name, data in payloads.items():
                member = archive.extractfile(prefix + name)
                if member is None or member.read() != data:
                    raise ValueError(f"sdist source mismatch: {repo.name}/{name}")
    else:
        raise ValueError("Unsupported Python distribution format")


def validate_firmware_provenance(manifest, repo, head):
    if not isinstance(manifest, dict):
        raise ValueError("Malformed firmware provenance")
    source = valid_commit(manifest.get("source_commit"))
    valid_commit(head)
    if manifest.get("source_tree_clean") is not True:
        raise ValueError("Firmware build source must be committed and clean")
    if not isinstance(manifest.get("toolchain"), dict) or not manifest["toolchain"]:
        raise ValueError("Firmware toolchain provenance required")
    if not manifest.get("built_at_utc") or not manifest.get("build_command"):
        raise ValueError("Firmware build time and command provenance required")
    if not isinstance(manifest.get("files"), dict):
        raise ValueError("Firmware file provenance required")
    try:
        git(repo, "merge-base", "--is-ancestor", source, head)
        changed = git(repo, "diff", "--name-only", source, head).decode().splitlines()
    except subprocess.CalledProcessError:
        raise ValueError(
            "Firmware build source must be an ancestor of candidate HEAD"
        ) from None
    unexpected = [
        name
        for name in changed
        if name not in FIRMWARE_EVIDENCE_PATHS
        and not name.startswith("docs/verification/")
    ]
    if unexpected:
        raise ValueError(
            "Firmware runtime/toolchain source changed after build; rebuild required"
        )
    for name, value in manifest["files"].items():
        safe_filename(name)
        if not isinstance(value, dict) or not re.fullmatch(
            r"[a-f0-9]{64}", str(value.get("sha256", ""))
        ):
            raise ValueError("Malformed firmware artifact hash")
        if type(value.get("bytes")) is not int or value["bytes"] <= 0:
            raise ValueError("Malformed firmware artifact size")
    return changed


def verify_candidate(directory, root=ROOT, *, require_current=False):
    directory = directory.resolve()
    manifest = json.loads((directory / "manifest.json").read_text())
    if (
        manifest.get("format_version") != 2
        or set(manifest.get("repositories", {})) != REPOSITORIES
    ):
        raise ValueError(
            "Candidate must identify exactly the five supported repositories"
        )
    records = manifest.get("artifacts")
    if not isinstance(records, list) or not records:
        raise ValueError("Candidate artifact inventory required")
    names = [safe_filename(record["file"]) for record in records]
    if len(set(names)) != len(names):
        raise ValueError("Duplicate candidate artifact filename")
    files = {path.name for path in directory.iterdir()}
    if files != set(names) | {"manifest.json", "SHA256SUMS"}:
        raise ValueError("Candidate has missing or unlisted output files")
    sums = {}
    for line in (directory / "SHA256SUMS").read_text().splitlines():
        digest, separator, name = line.partition("  ")
        if not separator or not re.fullmatch(r"[a-f0-9]{64}", digest) or name in sums:
            raise ValueError("Malformed or duplicate checksum entry")
        sums[safe_filename(name)] = digest
    if set(sums) != set(names) | {"manifest.json"}:
        raise ValueError("Checksum inventory disagrees with manifest")
    for name, digest in sums.items():
        path = directory / name
        if not path.is_file() or path.is_symlink() or sha256(path) != digest:
            raise ValueError(f"Candidate checksum mismatch: {name}")
    for name, evidence in manifest["repositories"].items():
        repo = root if name == "grok-gadgets" else root.parent / name
        commit = valid_commit(evidence["source_commit"])
        if evidence.get("source_dirty") is not False:
            raise ValueError("Candidate source must be committed and clean")
        if git(repo, "cat-file", "-t", commit).strip() != b"commit":
            raise ValueError("Candidate source is not a Git commit")
        if (
            require_current
            and git(repo, "rev-parse", "HEAD").decode().strip() != commit
        ):
            raise ValueError(f"Candidate source is not current HEAD: {name}")
        owned = [record for record in records if record["repository"] == name]
        for kind in ("source_archive", "git_bundle"):
            if sum(record["kind"] == kind for record in owned) != 1:
                raise ValueError(f"Candidate requires exactly one {kind} for {name}")
        if name in PYTHON_REPOSITORIES:
            if sum(record["kind"] == "python_package" for record in owned) != 2:
                raise ValueError(
                    "Candidate requires a fresh wheel and sdist for each Python component"
                )
            if sum(record["kind"] == "build_provenance" for record in owned) != 1:
                raise ValueError("Python build provenance required")
    for record in records:
        name = record["repository"]
        if name not in REPOSITORIES:
            raise ValueError("Unsupported artifact repository")
        repo = root if name == "grok-gadgets" else root.parent / name
        head = manifest["repositories"][name]["source_commit"]
        source = valid_commit(record["source_commit"])
        path = directory / record["file"]
        if path.stat().st_size != record["bytes"] or sha256(path) != record["sha256"]:
            raise ValueError(f"Artifact hash/size mismatch: {path.name}")
        kind = record["kind"]
        if kind not in ("firmware", "firmware_provenance") and source != head:
            raise ValueError("Artifact source differs from archived HEAD")
        if kind == "source_archive":
            expected = git(
                repo, "archive", "--format=tar.gz", "--prefix=" + name + "/", source
            )
            if path.read_bytes() != expected:
                raise ValueError(
                    f"Archive does not represent exact source commit: {name}"
                )
        elif kind == "git_bundle":
            git(repo, "bundle", "verify", str(path))
            heads = git(repo, "bundle", "list-heads", str(path)).decode().splitlines()
            if source not in {line.split()[0] for line in heads}:
                raise ValueError("Git bundle does not expose candidate source HEAD")
            with path.open("rb") as handle:
                header = handle.readline()
                if not header.startswith((b"# v2 git bundle", b"# v3 git bundle")):
                    raise ValueError("Unsupported Git bundle header")
                while line := handle.readline().strip():
                    if line.startswith(b"-"):
                        raise ValueError(
                            "Git bundle must preserve complete history without prerequisites"
                        )
        elif kind == "python_package":
            validate_python_package(path, repo, source)
        elif kind == "build_provenance":
            provenance = json.loads(path.read_text())
            packages = [
                r
                for r in records
                if r["repository"] == name and r["kind"] == "python_package"
            ]
            expected = {r["file"]: r["sha256"] for r in packages}
            if (
                provenance.get("source_commit") != head
                or provenance.get("source_dirty") is not False
            ):
                raise ValueError("Python build provenance source mismatch")
            if (
                provenance.get("artifacts") != expected
                or not provenance.get("environment")
                or not provenance.get("build_command")
            ):
                raise ValueError("Malformed Python build provenance")
            config_hash = hashlib.sha256(
                git(repo, "show", head + ":pyproject.toml")
            ).hexdigest()
            if provenance.get("build_configuration_sha256") != config_hash:
                raise ValueError("Python build configuration provenance mismatch")
        elif kind == "firmware_provenance":
            provenance = json.loads(path.read_text())
            validate_firmware_provenance(provenance, repo, head)
            if provenance["source_commit"] != source:
                raise ValueError("Firmware manifest source mismatch")
            firmware = [r for r in records if r["kind"] == "firmware"]
            if len(firmware) != 4 or set(provenance["files"]) != {
                r["file"].removeprefix("c124-") for r in firmware
            }:
                raise ValueError("Firmware file inventory mismatch")
            for binary in firmware:
                evidence = provenance["files"][binary["file"].removeprefix("c124-")]
                if (
                    binary["source_commit"] != source
                    or binary["sha256"] != evidence["sha256"]
                    or binary["bytes"] != evidence["bytes"]
                ):
                    raise ValueError("Firmware hash/source provenance mismatch")
        elif kind == "firmware":
            if (
                name != "grok-gadgets-esp32-sdk"
                or record.get("repository_head") != head
            ):
                raise ValueError("Firmware repository provenance mismatch")
        elif kind == "website":
            with tarfile.open(path) as archive:
                members = archive.getmembers()
                if not any(member.name == "website/index.html" for member in members):
                    raise ValueError("Website archive lacks its entry point")
                if any(
                    not member.name.startswith("website/") and member.name != "website"
                    for member in members
                ):
                    raise ValueError("Website archive contains an unexpected path")
        else:
            raise ValueError("Unsupported candidate artifact kind")
    if sum(record["kind"] == "firmware_provenance" for record in records) != 1:
        raise ValueError("Exactly one firmware provenance record required")
    if sum(record["kind"] == "website" for record in records) != 1:
        raise ValueError("Exactly one website build required")
    return len(records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        help="Candidate directory (default latest pointer)",
    )
    parser.add_argument(
        "--require-current",
        action="store_true",
        help="Require all archived source commits to match current HEADs",
    )
    args = parser.parse_args()
    directory = args.directory
    try:
        if directory is None:
            output = ROOT / "artifacts/publication"
            pointer = json.loads((output / "latest.json").read_text())
            directory = output / safe_filename(pointer["directory"])
            if sha256(directory / "manifest.json") != pointer["manifest_sha256"]:
                raise ValueError("Latest pointer manifest checksum mismatch")
        count = verify_candidate(directory, require_current=args.require_current)
        print(
            f"Verified {count} unpublished artifacts, five exact source archives and five complete Git bundles at {directory}"
        )
    except (
        ValueError,
        KeyError,
        OSError,
        subprocess.CalledProcessError,
        tarfile.TarError,
        zipfile.BadZipFile,
    ) as exc:
        if isinstance(exc, subprocess.CalledProcessError):
            print(
                f"Candidate verification failed: git exited {exc.returncode}",
                file=sys.stderr,
            )
        else:
            print(f"Candidate verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
