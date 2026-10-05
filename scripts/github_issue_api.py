"""Restricted GitHub REST adapter using existing gh authentication.

Writes require explicit opt-in and successful owner/repository preflight. Responses and
credentials are never logged. An uncertain write stops; the marker-based runner resumes.
"""

import json
import os
import re
import subprocess

from issue_migration import (
    ID,
    OWNER,
    REPOSITORIES,
    MigrationError,
    github_url,
    matches_payload,
)


class GitHubIssueAPI:
    PAGE_SIZE = 100
    MAX_PAGES = 1000

    def __init__(self, *, allow_writes=False, request_runner=None):
        self.allow_writes = allow_writes
        self.verified = False
        self.request_runner = request_runner or subprocess.run

    @staticmethod
    def scope(owner, repository):
        if owner != OWNER or repository not in REPOSITORIES:
            raise MigrationError(
                "GitHub migration target is outside the five approved repositories"
            )
        return f"repos/{owner}/{repository}"

    def require_writes(self):
        if not self.allow_writes or not self.verified:
            raise MigrationError(
                "GitHub writes require --apply and verified migration targets"
            )

    def request(self, endpoint, *, method="GET", payload=None, missing_ok=False):
        route = endpoint.partition("?")[0].split("/")
        if endpoint == "user" and method == "GET":
            pass
        elif len(route) in (3, 4, 5) and route[0] == "repos":
            self.scope(route[1], route[2])
            if len(route) > 3 and route[3] not in ("issues", "labels", "milestones"):
                raise MigrationError("API resource is outside issue migration")
            if len(route) == 5 and (
                route[3] != "issues" or not re.fullmatch(r"[1-9][0-9]*", route[4])
            ):
                raise MigrationError("API resource is outside issue migration")
            if method == "POST" and len(route) != 4:
                raise MigrationError("API create target is not a migration collection")
            if method == "PATCH" and len(route) != 5:
                raise MigrationError("API update target is not a mapped issue")
        else:
            raise MigrationError(
                "API endpoint is outside the approved migration targets"
            )
        if method not in ("GET", "POST", "PATCH"):
            raise MigrationError("API method is outside issue migration")
        if method != "GET":
            self.require_writes()
        command = [
            "gh",
            "api",
            endpoint,
            "--hostname",
            "github.com",
            "--method",
            method,
            "--include",
            "--header",
            "Accept: application/vnd.github+json",
            "--header",
            "X-GitHub-Api-Version: 2022-11-28",
        ]
        if payload is not None:
            command.extend(["--input", "-"])
        environment = os.environ.copy()
        environment.pop("GH_DEBUG", None)
        environment.update(GH_PROMPT_DISABLED="1", GH_PAGER="cat")
        try:
            result = self.request_runner(
                command,
                input=json.dumps(payload) if payload is not None else None,
                text=True,
                capture_output=True,
                timeout=60,
                env=environment,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            raise MigrationError(
                "GitHub API transport failed; write outcome may be unknown. Resume from the durable checkpoint."
            ) from None
        # gh --include supplies the HTTP status without depending on stderr wording.
        header, separator, body = result.stdout.replace("\r\n", "\n").partition("\n\n")
        first = header.splitlines()[0] if header else ""
        match = re.fullmatch(r"HTTP/\S+\s+(\d{3})(?:\s+.*)?", first)
        status = int(match[1]) if match else None
        if missing_ok and method == "GET" and status == 404:
            return None
        if (
            result.returncode
            or status is None
            or not 200 <= status < 300
            or not separator
        ):
            suffix = f" (HTTP {status})" if status is not None else ""
            raise MigrationError(
                "GitHub API request failed"
                + suffix
                + "; no automatic retry. Reconcile the durable checkpoint before resuming."
            )
        try:
            return json.loads(body)
        except (ValueError, TypeError):
            raise MigrationError(
                "GitHub API returned an uncertain JSON response; stop and reconcile"
            ) from None

    def pages(self, endpoint):
        values = []
        separator = "&" if "?" in endpoint else "?"
        for page in range(1, self.MAX_PAGES + 1):
            result = self.request(
                f"{endpoint}{separator}per_page={self.PAGE_SIZE}&page={page}"
            )
            if not isinstance(result, list) or any(
                not isinstance(row, dict) for row in result
            ):
                raise MigrationError("GitHub paginated response is not a resource list")
            if len(result) > self.PAGE_SIZE:
                raise MigrationError(
                    "GitHub pagination exceeded its requested page size"
                )
            values.extend(result)
            if len(result) < self.PAGE_SIZE:
                return values
        raise MigrationError(
            "GitHub pagination limit reached; refusing an incomplete inventory"
        )

    def verify_targets(self):
        self.verified = False
        user = self.request("user")
        if not isinstance(user, dict) or user.get("login") != OWNER:
            raise MigrationError("gh must authenticate as the approved owner adidshaft")
        for repository in REPOSITORIES:
            row = self.request(self.scope(OWNER, repository))
            permissions = row.get("permissions") if isinstance(row, dict) else None
            if (
                not isinstance(row, dict)
                or row.get("full_name") != f"{OWNER}/{repository}"
                or row.get("has_issues") is not True
                or row.get("archived") is not False
                or row.get("disabled", False) is not False
                or not isinstance(permissions, dict)
                or permissions.get("push") is not True
            ):
                raise MigrationError(
                    "Repository issue availability/write permissions require review: "
                    + repository
                )
        self.verified = True

    @staticmethod
    def positive_number(value):
        if type(value) is not int or value <= 0:
            raise MigrationError("GitHub returned an invalid resource number")
        return value

    def list_labels(self, owner, repository):
        rows = self.pages(self.scope(owner, repository) + "/labels")
        names = []
        for row in rows:
            name = row.get("name")
            if not isinstance(name, str) or not name:
                raise MigrationError("GitHub returned an invalid label")
            names.append(name.casefold())
        if len(names) != len(set(names)):
            raise MigrationError("GitHub label inventory is ambiguous")
        return rows

    def create_label(self, owner, repository, label):
        endpoint = self.scope(owner, repository) + "/labels"
        payload = {field: label[field] for field in ("name", "color", "description")}
        row = self.request(endpoint, method="POST", payload=payload)
        if (
            not isinstance(row, dict)
            or row.get("name") != payload["name"]
            or str(row.get("color", "")).casefold() != payload["color"].casefold()
            or row.get("description") != payload["description"]
        ):
            raise MigrationError(
                "Created label response disagrees with the request; reconcile before resuming"
            )
        return row

    def list_milestones(self, owner, repository):
        rows = self.pages(self.scope(owner, repository) + "/milestones?state=all")
        titles, numbers = set(), set()
        for row in rows:
            title = row.get("title")
            number = self.positive_number(row.get("number"))
            if (
                not isinstance(title, str)
                or not title
                or title in titles
                or number in numbers
            ):
                raise MigrationError("GitHub milestone inventory is ambiguous")
            titles.add(title)
            numbers.add(number)
        return rows

    def create_milestone(self, owner, repository, milestone):
        payload = {"title": milestone["title"]}
        description = milestone.get("description") or milestone.get("scope")
        if description:
            payload["description"] = description
        row = self.request(
            self.scope(owner, repository) + "/milestones",
            method="POST",
            payload=payload,
        )
        if not isinstance(row, dict) or row.get("title") != payload["title"]:
            raise MigrationError(
                "Created milestone response disagrees with the request"
            )
        self.positive_number(row.get("number"))
        return row

    def normalize_issue(self, owner, repository, row):
        if not isinstance(row, dict) or "pull_request" in row:
            raise MigrationError("Mapped GitHub resource is not an issue")
        number = self.positive_number(row.get("number"))
        if row.get("html_url") != github_url(owner, repository, number):
            raise MigrationError("GitHub issue HTML URL disagrees with its repository")
        title, labels = row.get("title"), row.get("labels")
        body = "" if row.get("body") is None else row["body"]
        if (
            not isinstance(title, str)
            or not isinstance(body, str)
            or not isinstance(labels, list)
        ):
            raise MigrationError("GitHub issue response has invalid fields")
        label_names = []
        for label in labels:
            name = label.get("name") if isinstance(label, dict) else label
            if not isinstance(name, str) or not name:
                raise MigrationError("GitHub issue has an invalid label")
            label_names.append(name)
        milestone = row.get("milestone")
        if milestone is not None:
            if not isinstance(milestone, dict) or not isinstance(
                milestone.get("title"), str
            ):
                raise MigrationError("GitHub issue has an invalid milestone")
            self.positive_number(milestone.get("number"))
            milestone = milestone["title"]
        if row.get("state") not in ("open", "closed"):
            raise MigrationError("GitHub issue has an invalid state")
        return {
            "number": number,
            "url": row["html_url"],
            "title": title,
            "body": body,
            "state": row["state"],
            "labels": label_names,
            "milestone": milestone,
        }

    def validate_marker(self, owner, repository, value):
        self.scope(owner, repository)
        prefix = f"<!-- grok-gadgets-local-id:{owner}/{repository}/"
        if (
            not isinstance(value, str)
            or not value.startswith(prefix)
            or not value.endswith(" -->")
        ):
            raise MigrationError("Issue marker is outside the approved repository")
        if not ID.fullmatch(value[len(prefix) : -4]):
            raise MigrationError("Issue marker has an invalid local ID")

    def find_issues(self, owner, repository, marker):
        self.validate_marker(owner, repository, marker)
        rows = self.pages(
            self.scope(owner, repository)
            + "/issues?state=all&sort=created&direction=asc"
        )
        matches, numbers = [], set()
        for row in rows:
            if "pull_request" in row:
                continue
            issue = self.normalize_issue(owner, repository, row)
            if issue["number"] in numbers:
                raise MigrationError(
                    "GitHub issue pagination returned duplicate numbers"
                )
            numbers.add(issue["number"])
            if marker in issue["body"]:
                if (
                    issue["body"].splitlines()[0] != marker
                    or issue["body"].count(marker) != 1
                ):
                    raise MigrationError(
                        "Local-ID marker is misplaced or repeated; review before migration"
                    )
                matches.append(issue)
        return matches

    def get_issue(self, owner, repository, number):
        number = self.positive_number(number)
        row = self.request(
            self.scope(owner, repository) + f"/issues/{number}", missing_ok=True
        )
        return None if row is None else self.normalize_issue(owner, repository, row)

    def issue_payload(self, owner, repository, payload):
        if set(payload) != {"title", "body", "state", "labels", "milestone"}:
            raise MigrationError("Issue payload has unsupported fields")
        if (
            not isinstance(payload["title"], str)
            or not payload["title"]
            or not isinstance(payload["body"], str)
            or not payload["body"]
            or payload["state"] not in ("open", "closed")
            or not isinstance(payload["labels"], list)
            or any(
                not isinstance(label, str) or not label for label in payload["labels"]
            )
        ):
            raise MigrationError("Issue payload has invalid fields")
        self.validate_marker(owner, repository, payload["body"].splitlines()[0])
        labels = {row["name"] for row in self.list_labels(owner, repository)}
        if not set(payload["labels"]) <= labels:
            raise MigrationError("Issue labels must exist before issue writes")
        milestones = [
            row
            for row in self.list_milestones(owner, repository)
            if row["title"] == payload["milestone"]
        ]
        if len(milestones) != 1:
            raise MigrationError(
                "Issue milestone must resolve to exactly one remote number"
            )
        return {**payload, "milestone": milestones[0]["number"]}

    def create_issue(self, owner, repository, payload):
        self.require_writes()
        if payload.get("state") != "open":
            raise MigrationError("Create identities open before the final state phase")
        request = self.issue_payload(owner, repository, payload)
        matches = self.find_issues(owner, repository, payload["body"].splitlines()[0])
        if len(matches) > 1:
            raise MigrationError("Multiple issues carry the same local-ID marker")
        if matches:
            return matches[0]
        request.pop(
            "state"
        )  # GitHub creation always starts open; state belongs to PATCH.
        issue = self.normalize_issue(
            owner,
            repository,
            self.request(
                self.scope(owner, repository) + "/issues",
                method="POST",
                payload=request,
            ),
        )
        if not matches_payload(issue, payload):
            raise MigrationError(
                "Created issue response disagrees with the request; reconcile before resuming"
            )
        return issue

    def update_issue(self, owner, repository, number, payload):
        self.require_writes()
        request = self.issue_payload(owner, repository, payload)
        existing = self.get_issue(owner, repository, number)
        marker = payload["body"].splitlines()[0]
        if (
            not existing
            or not existing["body"].splitlines()
            or existing["body"].splitlines()[0] != marker
        ):
            raise MigrationError("Refusing to update an unrelated or missing issue")
        issue = self.normalize_issue(
            owner,
            repository,
            self.request(
                self.scope(owner, repository) + f"/issues/{number}",
                method="PATCH",
                payload=request,
            ),
        )
        if not matches_payload(issue, payload):
            raise MigrationError(
                "Updated issue response disagrees with the request; reconcile before resuming"
            )
        return issue
