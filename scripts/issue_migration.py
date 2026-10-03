"""Durable local issue preparation and an injected fixture-only migration engine.

No credentials, network client, GitHub adapter or remote execution entry point exists here.
"""

import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import tempfile

OWNER = "adidshaft"
REPOSITORIES = (
    "grok-gadgets",
    "grok-gadgets-gateway",
    "grok-gadgets-linux-sdk",
    "grok-gadgets-esp32-sdk",
    "grok-gadgets-home-assistant",
)
STAGES = {"proposed", "ready", "in progress", "review", "blocked", "done"}
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,63}")
ISSUE_ID = re.compile(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-[0-9]+")


class MigrationError(ValueError):
    """Fail closed without erasing existing mappings or modifying unrelated issues."""


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + "-", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump(value, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def key(owner, repository, local_id):
    if not all(
        isinstance(part, str) and ID.fullmatch(part)
        for part in (owner, repository, local_id)
    ):
        raise MigrationError("Invalid owner/repository/local issue identity")
    return owner + "/" + repository + "/" + local_id


def marker(identity):
    return "<!-- grok-gadgets-local-id:" + identity + " -->"


def github_url(owner, repository, number):
    return f"https://github.com/{owner}/{repository}/issues/{number}"


def normalize_record(record, default_owner):
    result = copy.deepcopy(record)
    owner = result.get("owner") or default_owner
    identity = key(owner, result["repository"], result["local_id"])
    if result.get("mapping_key") not in (None, identity):
        raise MigrationError("Stored mapping key disagrees with its issue identity")
    result.update(owner=owner, mapping_key=identity, marker=marker(identity))
    number = result.get("github_number")
    if number is not None and (type(number) is not int or number <= 0):
        raise MigrationError("GitHub issue numbers must be positive integers")
    url = result.get("github_url")
    if url is not None and (
        number is None or url != github_url(owner, result["repository"], number)
    ):
        raise MigrationError("Stored GitHub URL disagrees with its mapping")
    source = result.get("source")
    if isinstance(source, str) and (
        Path(source).is_absolute() or re.match(r"^[A-Za-z]:", source)
    ):
        expected = result["repository"] + "/planning/issues.json"
        if not source.replace("\\", "/").endswith("/" + expected):
            raise MigrationError(
                "Unknown mapping source path needs portable identity review"
            )
        result["source"] = expected
    result.setdefault("github_number", None)
    result.setdefault("github_url", None)
    if number is not None and result["github_url"] is None:
        result["github_url"] = github_url(owner, result["repository"], number)
    return result


def validate_mappings(records):
    identities, remote = set(), {}
    for record in records:
        identity = record["mapping_key"]
        if identity in identities:
            raise MigrationError("Duplicate local mapping identity: " + identity)
        identities.add(identity)
        number = record["github_number"]
        if number is not None:
            address = (record["owner"], record["repository"], number)
            if address in remote:
                raise MigrationError("Two local IDs map to the same GitHub issue")
            remote[address] = identity


def list_manifest(value, field):
    return value.get(field, []) if isinstance(value, dict) else value


def load_manifests(root):
    labels = list_manifest(
        json.loads((root / "publication/labels.json").read_text()), "labels"
    )
    milestones = []
    for path in (
        root / "planning/milestones.json",
        root / "publication/milestones.json",
    ):
        if path.is_file():
            milestones.extend(list_manifest(json.loads(path.read_text()), "milestones"))
    combined = {}
    for milestone in milestones:
        mid = milestone.get("id")
        if mid not in combined:
            combined[mid] = copy.deepcopy(milestone)
            continue
        previous = combined[mid]
        if previous.get("title") != milestone.get("title"):
            raise MigrationError("Conflicting milestone titles for ID: " + str(mid))
        # The local manifest may carry historical scope/stage while publication adds
        # a remote description. Preserve both, but never silently choose between two
        # contradictory declarations of the same scope field.
        for field in ("scope", "description"):
            old, new = previous.get(field), milestone.get(field)
            if old and new and " ".join(old.split()) != " ".join(new.split()):
                raise MigrationError("Conflicting milestone scope for ID: " + str(mid))
        for field, value in milestone.items():
            if field not in previous or previous[field] in (None, ""):
                previous[field] = copy.deepcopy(value)
    return labels, list(combined.values())


def check_manifests(labels, milestones, records):
    errors, label_names, milestone_ids = [], set(), {}
    for label in labels:
        name = label.get("name")
        if not isinstance(name, str) or not name or name in label_names:
            errors.append("Missing or duplicate label name")
        label_names.add(name)
        if not re.fullmatch(r"[a-fA-F0-9]{6}", str(label.get("color", ""))):
            errors.append(f"Invalid label color: {name}")
        if (
            not isinstance(label.get("description"), str)
            or not label["description"].strip()
        ):
            errors.append(f"Missing label description: {name}")
    titles = {}
    for milestone in milestones:
        mid, title = milestone.get("id"), milestone.get("title")
        if (
            not isinstance(mid, str)
            or not ID.fullmatch(mid)
            or not isinstance(title, str)
            or not title.strip()
        ):
            errors.append("Milestone requires a stable ID and readable title")
            continue
        if mid in milestone_ids:
            errors.append("Duplicate milestone ID: " + mid)
        if title in titles and titles[title] != mid:
            errors.append("Distinct milestone IDs share a remote title: " + title)
        milestone_ids[mid] = milestone
        titles[title] = mid
    for record in records:
        if not record.get("source_present"):
            continue
        issue = record["record"]
        identity = record["mapping_key"]
        if issue.get("stage") not in STAGES:
            errors.append("Invalid issue stage: " + identity)
        declared_labels = issue.get("labels", [])
        if not isinstance(declared_labels, list) or not declared_labels:
            errors.append("Issue labels required: " + identity)
        else:
            for name in declared_labels:
                if name not in label_names:
                    errors.append(f"Undeclared label {name}: {identity}")
        mid = issue.get("milestone")
        if mid not in milestone_ids:
            errors.append(f"Undeclared primary milestone {mid}: {identity}")
    return {"ready": not errors, "errors": sorted(set(errors))}


def dependencies(record, records):
    """Resolve explicit IDs; preserve narrative external gates without inventing issues."""
    by_key = {r["mapping_key"]: r for r in records}
    resolved, external = [], []
    for dependency in record["record"].get("dependencies", []):
        if not isinstance(dependency, str):
            raise MigrationError("Dependencies must be strings")
        if "#" in dependency:
            repository, local_id = dependency.rsplit("#", 1)
            owner = record["owner"]
            if "/" in repository:
                owner, repository = repository.split("/", 1)
            identity = key(owner, repository, local_id)
            matches = [by_key[identity]] if identity in by_key else []
        elif ISSUE_ID.fullmatch(dependency):
            identity = key(record["owner"], record["repository"], dependency)
            matches = (
                [by_key[identity]]
                if identity in by_key
                else [
                    r
                    for r in records
                    if r["owner"] == record["owner"] and r["local_id"] == dependency
                ]
            )
        else:
            external.append(dependency)
            continue
        if len(matches) != 1:
            raise MigrationError("Missing or ambiguous dependency: " + dependency)
        if matches[0]["mapping_key"] == record["mapping_key"]:
            raise MigrationError("Issue cannot depend on itself")
        resolved.append(matches[0])
    return resolved, external


def render_body(record, records, *, linked=False):
    issue = record["record"]
    sections = [
        record["marker"],
        "",
        "Local ID: `" + record["local_id"] + "`",
        "",
        "Status: **" + str(issue.get("stage", "unknown")) + "**",
        "",
        str(issue.get("intended_behaviour") or issue.get("problem", "")),
    ]
    for title, field in (
        ("Acceptance", "acceptance"),
        ("Evidence", "evidence"),
        ("Commits", "commits"),
    ):
        values = issue.get(field, [])
        if isinstance(values, str):
            values = [values]
        if values:
            sections.extend(
                ["", "### " + title, "", *["- " + str(value) for value in values]]
            )
    if issue.get("blocker"):
        sections.extend(["", "### Blocked by", "", str(issue["blocker"])])
    resolved, external = dependencies(record, records)
    if resolved or external:
        sections.extend(["", "### Dependencies", ""])
        for dependency in resolved:
            label = dependency["repository"] + "#" + dependency["local_id"]
            if linked:
                if not dependency.get("github_url"):
                    raise MigrationError("Dependency mapping missing before link phase")
                sections.append("- [" + label + "](" + dependency["github_url"] + ")")
            else:
                sections.append("- `" + label + "` (resolve after issue creation)")
        sections.extend("- " + value + " (external prerequisite)" for value in external)
    return "\n".join(sections) + "\n"


def prepare(root, existing=None, *, owner=OWNER):
    root = Path(root)
    existing = copy.deepcopy(existing or {})
    records = [
        normalize_record(row, existing.get("owner") or owner)
        for row in existing.get("records", [])
    ]
    validate_mappings(records)
    by_key = {row["mapping_key"]: row for row in records}
    for row in records:
        row["source_present"] = False
    seen = set()
    for repository in REPOSITORIES:
        repo = root if repository == "grok-gadgets" else root.parent / repository
        path = repo / "planning/issues.json"
        if not path.is_file():
            raise MigrationError("Required local issue ledger missing: " + repository)
        issues = list_manifest(json.loads(path.read_text()), "issues")
        for issue in issues:
            identity = key(owner, repository, issue["id"])
            if identity in seen:
                raise MigrationError("Duplicate source local issue ID: " + identity)
            seen.add(identity)
            row = by_key.get(
                identity,
                normalize_record(
                    {"repository": repository, "local_id": issue["id"]}, owner
                ),
            )
            row.update(
                record=copy.deepcopy(issue),
                stage=issue.get("stage"),
                source_present=True,
                source=repository + "/planning/issues.json",
            )
            by_key[identity] = row
    records = [by_key[identity] for identity in sorted(by_key)]
    validate_mappings(records)
    labels, milestones = load_manifests(root)
    validation = check_manifests(labels, milestones, records)
    for row in records:
        if row["source_present"]:
            try:
                row["issue_body"] = render_body(row, records)
            except MigrationError as exc:
                validation["ready"] = False
                validation["errors"].append(str(exc) + ": " + row["mapping_key"])
    result = {
        **existing,
        "format_version": 2,
        "activated": existing.get("activated", False),
        "owner": owner,
        "mode": "local dry-run",
        "records": records,
        "labels": labels,
        "milestones": milestones,
        "validation": validation,
        "prepared_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    # An execution-complete checkpoint certifies its old payload, not changed source records.
    if result.get("migration_complete") and existing.get("records") != records:
        result["migration_complete"] = False
    return result


class FixtureMigrator:
    """In-memory/fake API only: no shipped live adapter or executable migration command.

    The injected API implements list/create_label, list/create_milestone, find_issues
    (complete marker matches), get/create/update_issue. Checkpoint must durably save a
    full plan after each accepted mapping and phase. Unknown source rows are read-only.
    """

    def __init__(self, api, checkpoint):
        self.api = api
        self.checkpoint = checkpoint

    def save(self, plan, phase):
        plan["fixture_phase"] = phase
        self.checkpoint(copy.deepcopy(plan))

    def checked_issue(self, row, issue):
        if not issue or row["marker"] not in issue.get("body", ""):
            raise MigrationError("Stale mapping points at an unrelated issue")
        number = issue.get("number")
        if type(number) is not int or number <= 0:
            raise MigrationError("API fixture returned an invalid issue number")
        if issue.get("url") != github_url(row["owner"], row["repository"], number):
            raise MigrationError("API fixture returned the wrong repository URL")
        return issue

    def reconcile(self, row):
        owner, repo = row["owner"], row["repository"]
        matches = self.api.find_issues(owner, repo, row["marker"])
        if len(matches) > 1:
            raise MigrationError("Multiple issues carry the same local-ID marker")
        existing = (
            self.api.get_issue(owner, repo, row["github_number"])
            if row["github_number"]
            else None
        )
        if existing:
            self.checked_issue(row, existing)
            if len(matches) != 1 or matches[0]["number"] != existing["number"]:
                raise MigrationError("Mapped issue and marker reconciliation disagree")
            return existing
        if matches:
            return self.checked_issue(row, matches[0])
        if row["github_number"] is not None:
            # Deleted/missing mapped issues require review, rather than silently recreating history.
            raise MigrationError(
                "Mapped issue no longer exists and has no marker match"
            )
        return None

    def run(self, plan):
        plan = copy.deepcopy(plan)
        if not plan.get("validation", {}).get("ready"):
            raise MigrationError(
                "Manifest/dependency validation must pass before fixture migration"
            )
        plan["records"] = [
            normalize_record(row, plan["owner"]) for row in plan["records"]
        ]
        validate_mappings(plan["records"])
        if not check_manifests(plan["labels"], plan["milestones"], plan["records"])[
            "ready"
        ]:
            raise MigrationError(
                "Current manifest validation must pass before fixture migration"
            )
        for row in plan["records"]:
            if row.get("source_present"):
                render_body(row, plan["records"])
        selected = [r for r in plan["records"] if r.get("source_present")]
        milestones = {m["id"]: m for m in plan["milestones"]}
        # Reconcile EVERY existing mapping before issuing a fake write; collisions fail closed.
        discovered = {}
        for row in plan["records"]:
            if row.get("source_present") or row["github_number"] is not None:
                discovered[row["mapping_key"]] = self.reconcile(row)
        addresses = set()
        for row in plan["records"]:
            issue = discovered.get(row["mapping_key"])
            if issue is not None:
                address = (row["owner"], row["repository"], issue["number"])
                if address in addresses:
                    raise MigrationError(
                        "Reconciled markers collide on one GitHub issue"
                    )
                addresses.add(address)
                if (
                    not row.get("source_present")
                    and row["github_number"] != issue["number"]
                ):
                    raise MigrationError(
                        "Unknown retained mapping needs explicit stale-ID review"
                    )
        for row in selected:
            owner, repo = row["owner"], row["repository"]
            labels = {label["name"] for label in self.api.list_labels(owner, repo)}
            for label in plan["labels"]:
                if label["name"] not in labels:
                    self.api.create_label(owner, repo, copy.deepcopy(label))
                    labels.add(label["name"])
            remote_milestones = {
                milestone["title"]
                for milestone in self.api.list_milestones(owner, repo)
            }
            milestone = milestones[row["record"]["milestone"]]
            if milestone["title"] not in remote_milestones:
                self.api.create_milestone(owner, repo, copy.deepcopy(milestone))
        self.save(plan, "prerequisites")
        # Phase one creates identities only. Reconcile again immediately before each creation.
        for row in selected:
            issue = self.reconcile(row)
            if issue is None:
                issue = self.api.create_issue(
                    row["owner"],
                    row["repository"],
                    {
                        "title": "["
                        + row["local_id"]
                        + "] "
                        + row["record"]["problem"],
                        "body": render_body(row, plan["records"]),
                        "state": "open",
                        "labels": row["record"]["labels"],
                        "milestone": milestones[row["record"]["milestone"]]["title"],
                    },
                )
            self.checked_issue(row, issue)
            if row["github_number"] not in (None, issue["number"]):
                row.setdefault("mapping_history", []).append(
                    {
                        "github_number": row["github_number"],
                        "github_url": row["github_url"],
                        "reason": "stale number reconciled by marker",
                    }
                )
            row.update(github_number=issue["number"], github_url=issue["url"])
            validate_mappings(plan["records"])
            self.save(plan, "identities")
        # Phase two writes dependency links and final state only after every identity is durable.
        for row in selected:
            issue = self.reconcile(row)
            body = render_body(row, plan["records"], linked=True)
            state = "closed" if row["record"]["stage"] == "done" else "open"
            payload = {
                "title": "[" + row["local_id"] + "] " + row["record"]["problem"],
                "body": body,
                "state": state,
                "labels": row["record"]["labels"],
                "milestone": milestones[row["record"]["milestone"]]["title"],
            }
            if any(issue.get(field) != value for field, value in payload.items()):
                self.api.update_issue(
                    row["owner"], row["repository"], row["github_number"], payload
                )
            self.save(plan, "links_and_state")
        for row in plan["records"]:
            if row["github_number"] is not None:
                issue = self.reconcile(row)
                if row.get("source_present"):
                    expected_state = (
                        "closed" if row["record"]["stage"] == "done" else "open"
                    )
                    expected = {
                        "title": "["
                        + row["local_id"]
                        + "] "
                        + row["record"]["problem"],
                        "body": render_body(row, plan["records"], linked=True),
                        "state": expected_state,
                        "labels": row["record"]["labels"],
                        "milestone": milestones[row["record"]["milestone"]]["title"],
                    }
                    if any(
                        issue.get(field) != value for field, value in expected.items()
                    ):
                        raise MigrationError("Mapped fixture issue verification failed")
        plan.update(migration_complete=True, fixture_only=True)
        self.save(plan, "verified")
        return plan
