"""Bounded GitHub activity refresh; explicit unavailable/fixture/cached/live states.
No network performed unless the caller explicitly selects --live after publication.
"""

import argparse
import json
import os
import re
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
from datetime import datetime, timezone, timedelta

REPOS = [
    "grok-gadgets",
    "grok-gadgets-gateway",
    "grok-gadgets-linux-sdk",
    "grok-gadgets-esp32-sdk",
    "grok-gadgets-home-assistant",
]


def summarize(records, now):
    contributors = set()
    active = set()
    stars = 0
    opened = 0
    releases = []
    cutoff = now - timedelta(days=90)
    for repo in records:
        stars += repo["stars"]
        opened += sum("pull_request" not in x for x in repo["issues"])
        for c in repo["contributors"]:
            if c.get("type") != "Bot":
                contributors.add(c["id"])
        for pr in repo["pulls"]:
            if (
                pr.get("merged_at")
                and datetime.fromisoformat(pr["merged_at"].replace("Z", "+00:00"))
                >= cutoff
                and pr["user"].get("type") != "Bot"
            ):
                active.add(pr["user"]["id"])
        releases.extend(
            {
                "repository": repo["name"],
                "name": x["tag_name"],
                "date": x["published_at"],
            }
            for x in repo["releases"]
        )
    return dict(
        aggregate_stars=stars,
        aggregate_stars_definition="Sum of repository stars; not unique people",
        open_issues=opened,
        contributors=len(contributors),
        active_contributors=len(active),
        active_definition="Non-bot contributors with an eligible merged PR in the previous 90 days",
        releases=releases,
    )


def fetch(owner, token=None):
    # Each endpoint is capped at 3 pages; incomplete results are never shown as complete counts.
    def get(path, paged=False):
        result = []
        for page in range(1, 4):
            req = Request(
                "https://api.github.com/repos/"
                + owner
                + "/"
                + path
                + ("?" if "?" not in path else "&")
                + f"per_page=100&page={page}",
                headers={
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "GrokGadgets-local-release-preparation",
                    **({"Authorization": "Bearer " + token} if token else {}),
                },
            )
            with urlopen(req, timeout=10) as res:
                data = json.load(res)
                more = 'rel="next"' in res.headers.get("Link", "")
            if not paged:
                return data
            result.extend(data)
            if not more:
                return result
        raise ValueError(
            "Pagination cap reached; activity unavailable rather than incomplete"
        )

    records = []
    for name in REPOS:
        metadata = get(name)
        # Closed PR summaries do not include merged_at; retrieve details boundedly.
        pulls = get(name + "/pulls?state=closed", True)
        if len(pulls) > 100:
            raise ValueError("PR detail cap reached")
        pulls = [
            get(name + "/pulls/" + str(x["number"]))
            for x in pulls
            if datetime.fromisoformat(x["updated_at"].replace("Z", "+00:00"))
            >= datetime.now(timezone.utc) - timedelta(days=90)
        ]
        records.append(
            dict(
                name=name,
                stars=metadata["stargazers_count"],
                issues=get(name + "/issues?state=open", True),
                contributors=get(name + "/contributors", True),
                pulls=pulls,
                releases=get(name + "/releases", True),
            )
        )
    return records


def refresh(owner, cache, requester=fetch, now=None):
    now = now or datetime.now(timezone.utc)
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", owner):
        raise ValueError("Invalid GitHub owner")
    old = json.loads(cache.read_text()) if cache.exists() else None
    if (
        old
        and old.get("owner") == owner
        and old.get("state") == "live"
        and (
            now - datetime.fromisoformat(old["last_successful_refresh"])
        ).total_seconds()
        < 3600
    ):
        return old
    try:
        result = dict(
            state="live",
            owner=owner,
            last_successful_refresh=now.isoformat(),
            data=summarize(requester(owner, os.environ.get("GITHUB_TOKEN")), now),
        )
    except (URLError, ValueError, KeyError, TimeoutError):
        if old and old.get("owner") == owner and old.get("state") in ["live", "cached"]:
            return {
                **old,
                "state": "cached",
                "refresh_error": "Refresh failed; timestamped cached data",
            }
        return dict(
            state="unavailable", reason="Refresh failed or exceeded bounded limits"
        )
    cache.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--live", action="store_true")
    p.add_argument("--owner")
    p.add_argument("--cache", type=Path, default=Path("artifacts/activity-cache.json"))
    args = p.parse_args()
    if args.live:
        if not args.owner:
            p.error("--live requires the approved public owner")
        args.cache.parent.mkdir(parents=True, exist_ok=True)
        print(json.dumps(refresh(args.owner, args.cache)))
    else:
        print(
            json.dumps(
                dict(
                    state="unavailable",
                    reason="Publication not authorized; no public repositories exist",
                )
            )
        )
