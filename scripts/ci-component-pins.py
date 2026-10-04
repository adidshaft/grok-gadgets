"""Export validated exact component pins for read-only integration CI."""

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REPOSITORIES = {
    "grok-gadgets-gateway": "gateway",
    "grok-gadgets-linux-sdk": "linux",
    "grok-gadgets-esp32-sdk": "esp32",
    "grok-gadgets-home-assistant": "ha",
}


def selected(candidate_repository="", candidate_commit=""):
    if bool(candidate_repository) != bool(candidate_commit):
        raise ValueError("Candidate repository and SHA must be supplied together")
    if candidate_repository and candidate_repository not in REPOSITORIES:
        raise ValueError("Unsupported candidate repository")
    manifest = json.loads((ROOT / "compatibility/tested-components.json").read_text())
    pins = {
        item["repository"]: item["commit"]
        for item in manifest["components"]
        if item["repository"] in REPOSITORIES
    }
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
    args = parser.parse_args()
    for name, sha in selected(args.candidate_repository, args.candidate_commit).items():
        print(name + "=" + sha)
