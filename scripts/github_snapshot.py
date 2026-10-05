"""Explicit read-only GitHub issue export and offline snapshot validation."""

from datetime import datetime, timezone
import ipaddress
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from github_issue_api import GitHubIssueAPI
from issue_migration import (
    ID,
    OWNER,
    REPOSITORIES,
    STAGES,
    MigrationError,
    atomic_json,
    github_url,
)

SOURCE = "GitHub Issues"
MARKER_HINT = "grok-gadgets-local-id"
STATUS = re.compile(r"^ {0,3}(?:\*\*)?Status(?:\*\*)?[ \t]*:[ \t]*(.*)$", re.I)
BLOCKER = re.compile(r"^[ \t]*(?:Blocker|Blocked by)[ \t]*:[ \t]*(.*)$", re.I)
BLOCKER_HEADING = re.compile(
    r"^[ \t]*#{1,6}[ \t]+(?:Blocker|Blocked by)[ \t]*#*[ \t]*$", re.I
)
UNSAFE_BLOCKER = re.compile(
    r"(?:/(?:Users|home)/[^\s]+|[A-Za-z]:\\Users\\|/private/var/"
    r"|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    r"|-----BEGIN .*PRIVATE KEY-----"
    r"|\b(?:gh[pousr]_|github_pat_|xai-)[A-Za-z0-9_-]+"
    r"|\bBearer[ \t]+\S+"
    r"|\b(?:password|token|secret|credential|api[_-]?key)[ \t]*[=:][ \t]*\S+)",
    re.I,
)


class SnapshotError(MigrationError):
    """Invalid or incomplete public issue inventory; retain the previous snapshot."""


def public_text(value, limit=500):
    if (
        not isinstance(value, str)
        or any(ord(char) < 32 and char not in "\n\r\t" for char in value)
        or not value.strip()
    ):
        raise SnapshotError("GitHub snapshot contains invalid public text")
    result = " ".join(value.split())
    if len(result) > limit:
        raise SnapshotError("GitHub snapshot public text exceeds its field limit")
    return result


def prose_lines(body):
    """Ignore quoted examples, comments and fenced code when reading status fields."""
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    fence = None
    result = []
    for line in body.splitlines():
        stripped = line.lstrip()
        opening = re.match(r"(\x60{3,}|~{3,})(.*)", stripped)
        if opening:
            if fence is None:
                fence = (opening[1][0], len(opening[1]))
            elif (
                opening[1][0] == fence[0]
                and len(opening[1]) >= fence[1]
                and not opening[2].strip()
            ):
                fence = None
            continue
        if fence is None and not stripped.startswith(">"):
            result.append(line)
    return result


def issue_stage(issue):
    if issue["state"] == "closed":
        return "done"
    values = {
        " ".join(match[1].strip("*_\x60 ").casefold().split())
        for line in prose_lines(issue["body"])
        if (match := STATUS.fullmatch(line))
    }
    # A reopened issue must never inherit completion from its historical body.
    if len(values) == 1:
        value = values.pop()
        if value in STAGES and value != "done":
            return value
    return "proposed"


def safe_blocker(value):
    if not isinstance(value, str) or UNSAFE_BLOCKER.search(value):
        return None
    if any(ord(char) < 32 and char not in "\n\r\t" for char in value):
        return None
    text = " ".join(re.sub(r"[*_\x60]", "", value).split())
    if not text or len(text) > 500 or text.casefold() in {"none", "none.", "n/a"}:
        return None
    if "<" in text or ">" in text:
        return None
    for match in re.finditer(r"https?://[^\s]+", text, re.I):
        try:
            url = urlsplit(match[0].rstrip(").,]"))
            host = url.hostname or ""
            if url.username or url.password or not host:
                return None
            if host.casefold() == "localhost" or host.endswith((".local", ".internal")):
                return None
            try:
                if not ipaddress.ip_address(host).is_global:
                    return None
            except ValueError:
                pass
        except ValueError:
            return None
    return text


def issue_blocker(issue, stage):
    if stage != "blocked":
        return None
    lines = prose_lines(issue["body"])
    values = []
    for index, line in enumerate(lines):
        inline = BLOCKER.fullmatch(line)
        if inline:
            values.append(inline[1])
        elif BLOCKER_HEADING.fullmatch(line):
            section = []
            for following in lines[index + 1 :]:
                if re.match(r"^[ \t]*#{1,6}[ \t]+", following):
                    break
                section.append(following)
            values.append("\n".join(section))
    return safe_blocker(values[0]) if len(values) == 1 else None


def issue_id(api, repository, issue):
    body = issue["body"]
    if MARKER_HINT not in body:
        return f"{repository}#{issue['number']}"
    lines = body.splitlines()
    if body.count(MARKER_HINT) != 1 or not lines:
        raise SnapshotError("GitHub local-ID marker is repeated or malformed")
    first = lines[0]
    api.validate_marker(OWNER, repository, first)
    prefix = f"<!-- {MARKER_HINT}:{OWNER}/{repository}/"
    return first[len(prefix) : -4]


def validate_snapshot(value):
    if (
        not isinstance(value, dict)
        or type(value.get("schema_version")) is not int
        or value["schema_version"] != 1
        or value.get("owner") != OWNER
        or value.get("source") != SOURCE
        or not isinstance(value.get("refreshed_at"), str)
        or not isinstance(value.get("issues"), list)
    ):
        raise SnapshotError("Invalid GitHub snapshot envelope")
    try:
        refreshed = datetime.fromisoformat(value["refreshed_at"])
    except ValueError:
        raise SnapshotError("GitHub snapshot timestamp is invalid") from None
    if refreshed.utcoffset() is None or refreshed.utcoffset().total_seconds() != 0:
        raise SnapshotError("GitHub snapshot timestamp must be UTC")
    numbers, identities = set(), set()
    for issue in value["issues"]:
        if not isinstance(issue, dict):
            raise SnapshotError("GitHub snapshot issue is invalid")
        repository, number = issue.get("repository"), issue.get("number")
        if repository not in REPOSITORIES or type(number) is not int or number <= 0:
            raise SnapshotError("GitHub snapshot issue target is invalid")
        if issue.get("github_url") != github_url(OWNER, repository, number):
            raise SnapshotError("GitHub snapshot issue URL is invalid")
        identity = issue.get("id")
        if not isinstance(identity, str) or not (
            ID.fullmatch(identity) or identity == f"{repository}#{number}"
        ):
            raise SnapshotError("GitHub snapshot issue identity is invalid")
        if (repository, number) in numbers or (repository, identity) in identities:
            raise SnapshotError("GitHub snapshot issue identities are duplicated")
        numbers.add((repository, number))
        identities.add((repository, identity))
        state, stage = issue.get("state"), issue.get("stage")
        if (
            not isinstance(state, str)
            or not isinstance(stage, str)
            or state not in {"open", "closed"}
            or stage not in STAGES
            or (state == "closed" and stage != "done")
            or (state == "open" and stage == "done")
        ):
            raise SnapshotError("GitHub snapshot issue state/stage disagrees")
        if "body" in issue:
            raise SnapshotError("GitHub snapshot must not contain raw issue bodies")
        for field, limit in (("problem", 500), ("milestone", 256)):
            if public_text(issue.get(field), limit) != issue[field]:
                raise SnapshotError("GitHub snapshot public text is not normalized")
        if "title" in issue and issue["title"] != issue["problem"]:
            raise SnapshotError("GitHub snapshot title disagrees with its problem")
        labels = issue.get("labels")
        if (
            not isinstance(labels, list)
            or any(public_text(label, 128) != label for label in labels)
            or len({label.casefold() for label in labels}) != len(labels)
        ):
            raise SnapshotError("GitHub snapshot labels are invalid")
        blocker = issue.get("blocker")
        if blocker is not None and (
            stage != "blocked" or safe_blocker(blocker) != blocker
        ):
            raise SnapshotError("GitHub snapshot blocker is not safe/relevant")
    return value


def collect_snapshot(api, *, now=None):
    issues = []
    for repository in REPOSITORIES:
        rows = api.pages(
            GitHubIssueAPI.scope(OWNER, repository)
            + "/issues?state=all&sort=created&direction=asc"
        )
        for row in rows:
            if "pull_request" in row:
                continue
            issue = api.normalize_issue(OWNER, repository, row)
            stage = issue_stage(issue)
            title = public_text(issue["title"])
            issues.append(
                {
                    "id": issue_id(api, repository, issue),
                    "repository": repository,
                    "number": issue["number"],
                    "problem": title,
                    "title": title,
                    "state": issue["state"],
                    "stage": stage,
                    "labels": sorted(
                        [public_text(label, 128) for label in issue["labels"]],
                        key=str.casefold,
                    ),
                    "milestone": public_text(issue["milestone"], 256)
                    if issue["milestone"] is not None
                    else "Unscheduled",
                    "blocker": issue_blocker(issue, stage),
                    "github_url": issue["url"],
                }
            )
    timestamp = now if now is not None else datetime.now(timezone.utc)
    if timestamp.utcoffset() is None:
        raise SnapshotError("GitHub snapshot refresh requires an aware timestamp")
    return validate_snapshot(
        {
            "schema_version": 1,
            "owner": OWNER,
            "refreshed_at": timestamp.astimezone(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z"),
            "source": SOURCE,
            "issues": sorted(
                issues, key=lambda issue: (issue["repository"], issue["number"])
            ),
        }
    )


def refresh_snapshot(path, api=None, *, now=None):
    # No preflight requiring owner write access and no GitHub mutations.
    snapshot = collect_snapshot(api if api is not None else GitHubIssueAPI(), now=now)
    atomic_json(path, snapshot)
    return snapshot


def load_snapshot(path):
    """Read the committed file only; never construct or call a network client."""
    try:
        value = json.loads(Path(path).read_text())
    except (OSError, ValueError):
        raise SnapshotError("GitHub snapshot is unavailable or invalid JSON") from None
    return validate_snapshot(value)
