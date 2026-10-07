"""Read-only local launch audit. JSON contains identifiers/counts, never matching values.

Heuristics cannot prove absence of secrets. History/identity are preserved. No remote API.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile
import zipfile

REPOSITORIES = (
    "grok-gadgets",
    "grok-gadgets-gateway",
    "grok-gadgets-linux-sdk",
    "grok-gadgets-esp32-sdk",
    "grok-gadgets-home-assistant",
)
PATTERNS = {
    "private_key": rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "github_token": rb"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b",
    "aws_access_key": rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "xai_key": rb"\bxai-[A-Za-z0-9_-]{24,}\b",
    "credential_assignment": rb"(?i)(?:api[_-]?key|access[_-]?token|secret[_-]?key)\s*[=:]\s*[\"']?[A-Za-z0-9+/_.-]{24,}",
    "bearer_literal": rb"(?i)\bBearer\s+[A-Za-z0-9_+-]{32,}",
    "private_host_path": rb"(?:/Users/[^/\s\"'<>]+/|/home/[^/\s\"'<>]+/|[A-Za-z]:\\Users\\[^\\\s\"'<>]+\\)",
    "official_mark_wording": rb"(?i)\b(?:official (?:grok|xai)|SpaceXAI|inspired by Grok)\b",
}
SECRET_KINDS = set(PATTERNS) - {"private_host_path", "official_mark_wording"}
LARGE_BYTES = 1024 * 1024
ARCHIVE_LIMIT = 128 * 1024 * 1024
PUBLIC_EMAIL = b"adidshaft@kyokasuigetsu.xyz"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(repo: Path, *args: str, input_data: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    ).stdout


def scan(data: bytes) -> dict[str, int]:
    return {
        kind: len(re.findall(pattern, data))
        for kind, pattern in PATTERNS.items()
        if re.search(pattern, data)
    }


def blob_payloads(repo: Path, ids: list[str]) -> dict[str, bytes]:
    # File-backed batch input/output also avoids platform pipe-buffer deadlocks.
    with tempfile.TemporaryFile() as requests, tempfile.TemporaryFile() as responses:
        requests.write(("\n".join(ids) + "\n").encode())
        requests.seek(0)
        subprocess.run(
            ["git", "-C", str(repo), "cat-file", "--batch"],
            stdin=requests,
            stdout=responses,
            stderr=subprocess.PIPE,
            check=True,
        )
        responses.seek(0)
        output = responses.read()
    result = {}
    cursor = 0
    while cursor < len(output):
        end = output.index(b"\n", cursor)
        oid, kind, size = output[cursor:end].split()
        cursor = end + 1
        length = int(size)
        if kind != b"blob":
            raise ValueError("Expected blob inventory")
        result[oid.decode()] = output[cursor : cursor + length]
        cursor += length + 1
    return result


def archive_review(data: bytes, depth: int = 0) -> dict:
    """Inspect without extraction, with an explicit ceiling and no path execution."""
    members = []
    skipped = []
    if zipfile.is_zipfile(io.BytesIO(data)):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                if (
                    member.file_size > ARCHIVE_LIMIT
                    or sum(m[1] for m in members) + member.file_size > ARCHIVE_LIMIT
                ):
                    skipped.append(member.filename)
                    continue
                members.append(
                    (member.filename, member.file_size, archive.read(member))
                )
    elif data.startswith(b"\x1f\x8b") or data[257:262] == b"ustar":
        try:
            with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as archive:
                for member in archive:
                    if not member.isfile():
                        continue
                    if (
                        member.size > ARCHIVE_LIMIT
                        or sum(m[1] for m in members) + member.size > ARCHIVE_LIMIT
                    ):
                        skipped.append(member.name)
                        continue
                    stream = archive.extractfile(member)
                    if stream is not None:
                        members.append((member.name, member.size, stream.read()))
        except tarfile.ReadError:
            return {}
    else:
        return {}
    findings = [
        {"member": name, "kinds": scan(payload)}
        for name, _, payload in members
        if scan(payload)
    ]
    license_files = [
        {"member": name, "sha256": sha(payload)}
        for name, _, payload in members
        if Path(name).name in {"LICENSE", "NOTICE"}
    ]
    metadata = [
        {
            "member": name,
            "apache_expression": b"License-Expression: Apache-2.0" in payload,
        }
        for name, _, payload in members
        if Path(name).name == "METADATA"
    ]
    nested_reviews = [
        {"member": name, "review": archive_review(payload, depth + 1)}
        for name, _, payload in members
        if depth < 3
        and (
            zipfile.is_zipfile(io.BytesIO(payload))
            or payload.startswith(b"\x1f\x8b")
            or payload[257:262] == b"ustar"
        )
    ]
    return {
        "members_scanned": len(members),
        "bytes_scanned": sum(m[1] for m in members),
        "skipped_members": skipped,
        "findings": findings,
        "license_files": license_files,
        "metadata": metadata,
        "nested_archives": [
            name
            for name, _, payload in members
            if zipfile.is_zipfile(io.BytesIO(payload))
            or payload.startswith(b"\x1f\x8b")
            or payload[257:262] == b"ustar"
        ],
        "nested_archive_contents_scanned": depth < 3,
        "nested_reviews": nested_reviews,
    }


def tree(repo: Path, commit: str) -> dict[str, str]:
    result = {}
    for record in git(repo, "ls-tree", "-rz", commit).split(b"\0"):
        if record:
            fields, name = record.split(b"\t", 1)
            _, kind, oid = fields.split()
            if kind == b"blob":
                result[name.decode("utf-8", "replace")] = oid.decode()
    return result


def audit_repository(repo: Path) -> dict:
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    head_commits = git(repo, "rev-list", "HEAD").decode().splitlines()
    commits = git(repo, "rev-list", "--all").decode().splitlines()
    head_set = set(head_commits)
    paths = defaultdict(set)
    head_history = set()
    for commit in commits:
        for path, oid in tree(repo, commit).items():
            paths[oid].add(path)
            if commit in head_set:
                head_history.add(oid)
    refs = []
    for line in (
        git(repo, "for-each-ref", "--format=%(refname) %(objectname)")
        .decode()
        .splitlines()
    ):
        ref, oid = line.split(" ", 1)
        peeled = git(repo, "rev-parse", ref + "^{}").decode().strip()
        kind = git(repo, "cat-file", "-t", peeled).decode().strip()
        refs.append(
            {
                "ref": ref,
                "object": oid,
                "peeled_object": peeled,
                "object_type": kind,
                "commit_in_head_history": peeled in head_set,
            }
        )
        # Agent checkpoint refs can point directly to trees, not commits.
        if kind == "tree":
            for path, blob in tree(repo, peeled).items():
                paths[blob].add(path)
        elif kind == "blob":
            paths[peeled].add("[direct-ref blob]")
    current = tree(repo, head)
    current_ids = set(current.values())
    payloads = blob_payloads(repo, sorted(paths))
    blobs = []
    for oid, payload in payloads.items():
        archive = archive_review(payload)
        entry = {
            "object": oid,
            "paths": sorted(paths[oid]),
            "bytes": len(payload),
            "sha256": sha(payload),
            "binary": b"\0" in payload,
            "large": len(payload) >= LARGE_BYTES,
            "in_head_tree": oid in current_ids,
            "in_head_history": oid in head_history,
            "kinds": scan(payload),
        }
        if archive:
            entry["archive"] = archive
        blobs.append(entry)
    metadata = []
    for commit in commits:
        values = git(
            repo, "show", "-s", "--format=%an%x00%ae%x00%cn%x00%ce%x00%B", commit
        ).split(b"\0", 4)
        author_name, author_email, committer_name, committer_email, message = values
        metadata.append(
            {
                "commit": commit,
                "in_head_history": commit in head_set,
                "author_name_sha256": sha(author_name),
                "author_email_sha256": sha(author_email),
                "committer_name_sha256": sha(committer_name),
                "committer_email_sha256": sha(committer_email),
                "author_email_disposition": email_disposition(author_email),
                "committer_email_disposition": email_disposition(committer_email),
                "message_sha256": sha(message),
                "message_kinds": scan(message),
                "identity_kinds": scan(b"\n".join(values[:4])),
            }
        )
    working = []
    for raw_path in git(repo, "ls-files", "-z").split(b"\0"):
        if not raw_path:
            continue
        path = raw_path.decode("utf-8", "replace")
        file = repo / path
        if file.is_symlink():
            payload = file.readlink().as_posix().encode()
        elif file.is_file():
            payload = file.read_bytes()
        else:
            working.append({"path": path, "missing": True})
            continue
        entry = {
            "path": path,
            "sha256": sha(payload),
            "bytes": len(payload),
            "binary": b"\0" in payload,
            "kinds": scan(payload),
        }
        archive = archive_review(payload)
        if archive:
            entry["archive"] = archive
        working.append(entry)
    licenses = {}
    for name in ("LICENSE", "NOTICE"):
        versions = [
            {
                "object": b["object"],
                "sha256": b["sha256"],
                "in_head_history": b["in_head_history"],
            }
            for b in blobs
            if name in b["paths"]
        ]
        licenses[name] = {
            "working_sha256": sha((repo / name).read_bytes())
            if (repo / name).is_file()
            else None,
            "head_sha256": sha(payloads[current[name]]) if name in current else None,
            "versions": versions,
        }
    head_after = git(repo, "rev-parse", "HEAD").decode().strip()
    return {
        "repository": repo.name,
        "head": head,
        "branch": git(repo, "branch", "--show-current").decode().strip(),
        "head_unchanged_during_scan": head == head_after,
        "tracked_worktree_dirty": bool(
            git(repo, "status", "--porcelain", "--untracked-files=no")
        ),
        "untracked_paths": [
            p.decode("utf-8", "replace")
            for p in git(
                repo, "ls-files", "--others", "--exclude-standard", "-z"
            ).split(b"\0")
            if p
        ],
        "commits_head": len(head_commits),
        "commits_all_refs": len(commits),
        "extra_commits": sorted(set(commits) - head_set),
        "refs": refs,
        "licenses": licenses,
        "working_tracked": working,
        "blobs": blobs,
        "commit_metadata": metadata,
        "summary": {
            "tracked_files": len(working),
            "head_blobs": len(current_ids),
            "all_history_blobs": len(blobs),
            "deleted_or_replaced_blobs": sum(
                not b["in_head_tree"] and b["in_head_history"] for b in blobs
            ),
            "extra_ref_only_blobs": sum(not b["in_head_history"] for b in blobs),
            "binary_blobs": sum(b["binary"] for b in blobs),
            "large_blobs": sum(b["large"] for b in blobs),
            "working_findings": dict(
                Counter(kind for entry in working for kind in entry.get("kinds", {}))
            ),
            "history_findings": dict(
                Counter(kind for entry in blobs for kind in entry["kinds"])
            ),
            "message_findings": dict(
                Counter(kind for entry in metadata for kind in entry["message_kinds"])
            ),
            "personal_email_commits": sum(
                entry["author_email_disposition"] == "personal_review_required"
                or entry["committer_email_disposition"] == "personal_review_required"
                for entry in metadata
            ),
        },
    }


def email_disposition(email: bytes) -> str:
    if email == PUBLIC_EMAIL:
        return "approved_public_contact"
    if email.endswith(b"@users.noreply.github.com"):
        return "github_noreply"
    return "personal_review_required"


def local_assets(root: Path) -> list[dict]:
    """Explicit local candidates/evidence roots, excluding venv/tool caches and .git."""
    result = []
    for folder in (
        "assets",
        "docs/visuals",
        "website/assets",
        "website/downloads",
        "artifacts/grok-launch",
    ):
        directory = root / folder
        if not directory.is_dir():
            continue
        for file in sorted(directory.rglob("*")):
            if not file.is_file() or file.is_symlink():
                continue
            payload = file.read_bytes()
            result.append(
                {
                    "path": file.relative_to(root).as_posix(),
                    "bytes": len(payload),
                    "sha256": sha(payload),
                    "kinds": scan(payload),
                    "default_disposition": "exclude_private_evidence"
                    if folder.startswith("artifacts/")
                    else "explicit_allowlist_review_required",
                }
            )
    for name in REPOSITORIES[1:]:
        for file in sorted((root.parent / name / "dist").glob("*")):
            if file.suffix not in {".whl", ".gz"} or not file.is_file():
                continue
            payload = file.read_bytes()
            result.append(
                {
                    "path": f"{name}/dist/{file.name}",
                    "bytes": len(payload),
                    "sha256": sha(payload),
                    "archive": archive_review(payload),
                    "default_disposition": "candidate_provenance_and_license_review_required",
                }
            )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument(
        "--repo",
        type=Path,
        action="append",
        help="Explicit repositories for bounded local fixtures",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="JSON destination; default is an ignored timestamped inventory",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    repos = args.repo or [
        root if name == "grok-gadgets" else root.parent / name for name in REPOSITORIES
    ]
    records = [audit_repository(repo.resolve()) for repo in repos]
    inventory = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "All current index-tracked worktree files, HEAD-reachable commit trees, all local-ref-reachable commit trees plus direct tree/blob refs (including agent checkpoints), and author/committer/message metadata. No reflog-only, dangling or unreachable object scan. Binary bytes and archive members are heuristic-scanned; nested archive members are recursively scanned to depth 3 with a 128 MiB expanded-data ceiling per archive; skipped members/depth are explicit. Images are not OCR/privacy inspected. No secret-proof or legal clearance claim.",
        "pattern_kinds": sorted(PATTERNS),
        "repositories": records,
        "local_assets_and_packages": local_assets(root),
        "private_recovery": "All --all Git bundles are private recovery only. Publish only an explicitly reviewed branch and selected artifacts; never bundle agent checkpoint refs, other local refs, account evidence or raw logs wholesale.",
    }
    output = args.output or root / "artifacts/launch-audit" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ") + ".json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(inventory, indent=2) + "\n").encode()
    output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "inventory": output.name,
                "sha256": sha(encoded),
                "repositories": [
                    {
                        "repository": r["repository"],
                        "head": r["head"],
                        "commits_head": r["commits_head"],
                        "commits_all_refs": r["commits_all_refs"],
                        **r["summary"],
                    }
                    for r in records
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
