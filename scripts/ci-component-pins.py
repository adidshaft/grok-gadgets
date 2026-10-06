"""Export exact component SHAs for read-only integration CI.

Resolve main or dev heads from GitHub. --source pinned uses the release record
in compatibility/tested-components.json instead.
"""

import argparse
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPOSITORIES = {
    "grok-gadgets-gateway": "gateway",
    "grok-gadgets-linux-sdk": "linux",
    "grok-gadgets-esp32-sdk": "esp32",
    "grok-gadgets-home-assistant": "ha",
}


def branch_heads(branch):
    """Read each component's selected branch SHA from the public repository."""
    heads = {}
    for repository in REPOSITORIES:
        output = subprocess.run(
            [
                "git",
                "ls-remote",
                f"https://github.com/adidshaft/{repository}.git",
                f"refs/heads/{branch}",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        ).stdout.split()
        heads[repository] = output[0] if output else ""
    return heads


def selected(candidate_repository="", candidate_commit="", source="pinned"):
    if bool(candidate_repository) != bool(candidate_commit):
        raise ValueError("Candidate repository and SHA must be supplied together")
    if candidate_repository and candidate_repository not in REPOSITORIES:
        raise ValueError("Unsupported candidate repository")
    if source in {"main", "dev"}:
        pins = branch_heads(source)
    elif source == "pinned":
        manifest = json.loads(
            (ROOT / "compatibility/tested-components.json").read_text()
        )
        pins = {
            item["repository"]: item["commit"]
            for item in manifest["components"]
            if item["repository"] in REPOSITORIES
        }
    else:
        raise ValueError("Source must be main, dev or pinned")
    if set(pins) != set(REPOSITORIES):
        raise ValueError("Missing component pins")
    if candidate_repository:
        pins[candidate_repository] = candidate_commit
    if any(
        not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha)
        for sha in pins.values()
    ):
        raise ValueError("Use exact forty-character lowercase commit SHAs")
    return {REPOSITORIES[repository]: sha for repository, sha in pins.items()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-repository", default="")
    parser.add_argument("--candidate-commit", default="")
    parser.add_argument("--source", choices=["main", "dev", "pinned"], default="main")
    args = parser.parse_args()
    chosen = selected(args.candidate_repository, args.candidate_commit, args.source)
    for name, sha in chosen.items():
        print(name + "=" + sha)
