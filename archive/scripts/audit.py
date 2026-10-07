"""Local publication inventory and heuristic secret audit. Never prints matching values."""

import subprocess
import json
import re
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
repos = [root, *sorted(root.parent.glob("grok-gadgets-*"))]
patterns = [
    ("private_key", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ("github_token", r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}\b"),
    ("cloud_key", r"\bAKIA[A-Z0-9]{16}\b"),
]
result = []
for repo in repos:
    if not (repo / ".git").is_dir():
        continue

    def git(*args):
        return subprocess.check_output(
            ["git", "-C", str(repo), *args], text=True
        ).strip()

    findings = []
    tracked = git("ls-files").splitlines()
    for f in tracked:
        data = (repo / f).read_bytes()
        try:
            s = data.decode()
        except UnicodeDecodeError:
            continue
        for kind, pattern in patterns:
            if re.search(pattern, s):
                findings.append({"file": f, "kind": kind})
        if Path(f).name in [".env", "credentials.json"]:
            findings.append({"file": f, "kind": "credential_filename"})
    # Scan every reachable Git object as well, so removed secrets cannot hide in history.
    objects = git("rev-list", "--objects", "--all").splitlines()
    history_matches = []
    object_ids = [line.split(" ", 1)[0] for line in objects]
    import tempfile

    with tempfile.TemporaryFile() as output:
        subprocess.run(
            ["git", "-C", str(repo), "cat-file", "--batch", "--batch-all-objects"],
            stdout=output,
            check=True,
            timeout=30,
        )
        output.seek(0)
        buffer = output.read()
    cursor = 0
    object_paths = {
        line.split(" ", 1)[0]: line.split(" ", 1)[1] if " " in line else None
        for line in objects
    }
    while cursor < len(buffer):
        end = buffer.index(b"\n", cursor)
        header = buffer[cursor:end].decode().split()
        cursor = end + 1
        size = int(header[2])
        payload = buffer[cursor : cursor + size]
        cursor += size + 1
        if header[1] != "blob" or header[0] not in object_ids:
            continue
        try:
            source = payload.decode()
        except UnicodeDecodeError:
            continue
        for kind, pattern in patterns:
            if re.search(pattern, source):
                history_matches.append(
                    {
                        "object": header[0],
                        "file": object_paths.get(header[0]),
                        "kind": kind,
                    }
                )
    findings.extend(history_matches)
    result.append(
        dict(
            repository=repo.name,
            commit=git("rev-parse", "HEAD"),
            branch=git("branch", "--show-current"),
            clean=not git("status", "--porcelain"),
            remotes=git("remote", "-v"),
            tracked_files=len(tracked),
            license_sha256=hashlib.sha256((repo / "LICENSE").read_bytes()).hexdigest(),
            secret_findings=findings,
            history=git("log", "--format=%h %s").splitlines(),
        )
    )
out = root / "artifacts/publication-audit.json"
out.parent.mkdir(exist_ok=True)
out.write_text(
    json.dumps(
        dict(
            scope="Tracked working-tree and all reachable Git blob heuristic scan, not an exhaustive secret guarantee; dependency redistribution review required",
            repositories=result,
        ),
        indent=2,
    )
    + "\n"
)
print(
    json.dumps(
        [
            {
                "repository": r["repository"],
                "clean": r["clean"],
                "commits": len(r["history"]),
                "findings": len(r["secret_findings"]),
                "remotes": r["remotes"],
            }
            for r in result
        ],
        indent=2,
    )
)


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def expected_remotes(record):
    url = "https://github.com/adidshaft/" + record["repository"] + ".git"
    return all(
        line.split()[1] in (url, url.removesuffix(".git"))
        for line in record["remotes"].splitlines()
    )


require(len(result) == 5, "Five repositories required")
require(
    not any(r["secret_findings"] for r in result), "Review redacted secret findings"
)
require(
    all(expected_remotes(r) for r in result),
    "Only the public adidshaft GitHub remote is expected",
)
