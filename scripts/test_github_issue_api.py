"""Offline REST/CLI migration tests; the fake gh transport makes no network calls."""

import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from github_issue_api import GitHubIssueAPI
import issue_migration as migration

spec = importlib.util.spec_from_file_location(
    "migrate_github_issues", Path(__file__).with_name("migrate-github-issues.py")
)
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class FakeGH:
    def __init__(self):
        self.calls = []
        self.labels, self.milestones, self.issues = {}, {}, {}
        self.login = migration.OWNER
        self.can_push = True
        self.fail_after_create = False
        self.failure_status = None

    @staticmethod
    def response(value, status=200):
        return SimpleNamespace(
            returncode=0 if status < 400 else 1,
            stdout=f"HTTP/2.0 {status} Response\r\nContent-Type: application/json\r\n\r\n"
            + json.dumps(value),
            stderr="",
        )

    def raw_issue(self, owner, repository, number, payload):
        milestone = self.milestones[(owner, repository)][payload["milestone"]]
        return {
            "number": number,
            "html_url": migration.github_url(owner, repository, number),
            "url": f"https://api.github.com/repos/{owner}/{repository}/issues/{number}",
            "title": payload["title"],
            "body": payload["body"],
            "state": payload.get("state", "open"),
            "labels": [{"name": name} for name in sorted(payload["labels"])],
            "milestone": copy.deepcopy(milestone),
        }

    def __call__(self, command, **kwargs):
        endpoint = command[2]
        method = command[command.index("--method") + 1]
        payload = json.loads(kwargs["input"]) if kwargs.get("input") else None
        self.calls.append((method, endpoint, payload))
        assert command[command.index("--hostname") + 1] == "github.com"
        assert "GH_DEBUG" not in kwargs["env"]
        assert "--verbose" not in command
        if self.failure_status:
            return self.response(
                {"message": "fixture secret should never be displayed"},
                self.failure_status,
            )
        if endpoint == "user":
            return self.response({"login": self.login})
        parsed = urlsplit(endpoint)
        pieces = parsed.path.split("/")
        owner, repository = pieces[1:3]
        key = owner, repository
        if len(pieces) == 3:
            return self.response(
                {
                    "full_name": owner + "/" + repository,
                    "has_issues": True,
                    "archived": False,
                    "disabled": False,
                    "permissions": {"push": self.can_push},
                }
            )
        resource = pieces[3]
        if method == "GET":
            if resource == "labels":
                rows = list(self.labels.get(key, {}).values())
            elif resource == "milestones":
                rows = list(self.milestones.get(key, {}).values())
                assert parse_qs(parsed.query)["state"] == ["all"]
            elif len(pieces) == 5:
                row = self.issues.get((*key, int(pieces[4])))
                return (
                    self.response(copy.deepcopy(row), 200)
                    if row
                    else self.response({"message": "Not Found"}, 404)
                )
            else:
                rows = [row for (o, r, _), row in self.issues.items() if (o, r) == key]
                assert parse_qs(parsed.query)["state"] == ["all"]
            query = parse_qs(parsed.query)
            size, page = int(query["per_page"][0]), int(query["page"][0])
            return self.response(copy.deepcopy(rows[(page - 1) * size : page * size]))
        if resource == "labels":
            self.labels.setdefault(key, {})[payload["name"]] = copy.deepcopy(payload)
            return self.response(payload, 201)
        if resource == "milestones":
            items = self.milestones.setdefault(key, {})
            row = {**payload, "number": max(items, default=0) + 1, "state": "open"}
            items[row["number"]] = row
            return self.response(row, 201)
        if method == "POST":
            assert "state" not in payload
            number = max([n for o, r, n in self.issues if (o, r) == key], default=0) + 1
            row = self.raw_issue(owner, repository, number, payload)
            self.issues[(*key, number)] = row
            if self.fail_after_create:
                self.fail_after_create = False
                raise subprocess.TimeoutExpired(
                    command, 60, output="fixture transport secret"
                )
            return self.response(copy.deepcopy(row), 201)
        # All identities must exist before cross-repository links or closed states.
        assert len(self.issues) >= len(migration.REPOSITORIES)
        number = int(pieces[4])
        row = self.raw_issue(owner, repository, number, payload)
        self.issues[(*key, number)] = row
        return self.response(copy.deepcopy(row))

    @property
    def writes(self):
        return [call for call in self.calls if call[0] != "GET"]


class GitHubIssueAPITests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        workspace = Path(self.temporary.name)
        self.root = workspace / "grok-gadgets"
        for index, repository in enumerate(migration.REPOSITORIES):
            repo = workspace / repository
            (repo / "planning").mkdir(parents=True)
            migration.atomic_json(
                repo / "planning/issues.json",
                [
                    {
                        "id": f"TEST-{index}",
                        "problem": "Offline fixture",
                        "stage": "done" if index == 0 else "ready",
                        "acceptance": ["Fixture acceptance"],
                        "evidence": ["Fixture evidence"],
                        "commits": ["fixture"],
                        "labels": ["zeta", "docs"],
                        "milestone": "M0",
                        "dependencies": ["grok-gadgets#TEST-0"] if index == 2 else [],
                    }
                ],
            )
        (self.root / "publication").mkdir()
        migration.atomic_json(
            self.root / "publication/labels.json",
            [
                {"name": name, "color": "abcdef", "description": "Fixture " + name}
                for name in ("docs", "zeta")
            ],
        )
        migration.atomic_json(
            self.root / "planning/milestones.json",
            [{"id": "M0", "title": "Foundations"}],
        )
        self.plan = migration.prepare(self.root)
        self.path = self.root / "publication/issue-migration.json"
        migration.atomic_json(self.path, self.plan)
        self.server = FakeGH()
        self.api = GitHubIssueAPI(allow_writes=True, request_runner=self.server)
        self.api.verify_targets()
        self.saved = []

    def migrate(self, plan=None, checkpoint=None):
        return migration.MigrationRunner(
            self.api, checkpoint or self.saved.append, fixture_only=False
        ).run(plan or self.plan)

    def test_live_mode_uses_remote_numbers_html_urls_and_idempotent_label_sets(self):
        result = self.migrate()
        self.assertFalse(result["fixture_only"])
        self.assertTrue(result["activated"])
        self.assertTrue(result["migration_complete"])
        self.assertEqual(result["migration_phase"], "verified")
        self.assertNotIn("fixture_phase", result)
        for call in self.server.writes:
            if "/issues" in call[1]:
                self.assertIs(type(call[2]["milestone"]), int)
        raw = self.server.issues[(migration.OWNER, "grok-gadgets", 1)]
        self.assertEqual(raw["state"], "closed")
        linked = self.server.issues[(migration.OWNER, "grok-gadgets-linux-sdk", 1)]
        self.assertIn(
            migration.github_url(migration.OWNER, "grok-gadgets", 1), linked["body"]
        )
        writes = copy.deepcopy(self.server.writes)
        self.migrate(migration.prepare(self.root, result))
        self.assertEqual(self.server.writes, writes)

    def test_lost_create_response_recovers_marker_without_duplicate(self):
        self.server.fail_after_create = True
        with self.assertRaisesRegex(
            migration.MigrationError, "outcome may be unknown"
        ) as caught:
            self.migrate()
        self.assertNotIn("fixture transport secret", str(caught.exception))
        self.assertEqual(len(self.server.issues), 1)
        self.migrate(self.saved[-1])
        creates = [
            call
            for call in self.server.writes
            if call[0] == "POST" and call[1].endswith("/issues")
        ]
        self.assertEqual(len(creates), 5)

    def test_pagination_includes_closed_issues_and_excludes_pull_requests(self):
        self.migrate()
        self.api.PAGE_SIZE = 1
        key = (migration.OWNER, "grok-gadgets", 1)
        pull = copy.deepcopy(self.server.issues[key])
        pull.update(
            number=2,
            html_url="https://github.com/adidshaft/grok-gadgets/pull/2",
            pull_request={},
        )
        self.server.issues[(migration.OWNER, "grok-gadgets", 2)] = pull
        matches = self.api.find_issues(
            *key[:2], migration.marker("adidshaft/grok-gadgets/TEST-0")
        )
        self.assertEqual([row["number"] for row in matches], [1])
        self.assertTrue(any("page=3" in call[1] for call in self.server.calls))

    def test_scope_and_write_opt_in_fail_before_transport(self):
        transport = unittest.mock.Mock()
        api = GitHubIssueAPI(request_runner=transport)
        with self.assertRaises(migration.MigrationError):
            api.list_labels("other", "grok-gadgets")
        with self.assertRaises(migration.MigrationError):
            api.request(
                "repos/adidshaft/grok-gadgets/issues", method="POST", payload={}
            )
        api.allow_writes = True
        with self.assertRaises(migration.MigrationError):
            api.request(
                "repos/adidshaft/grok-gadgets/issues", method="POST", payload={}
            )
        api.verified = True
        with self.assertRaises(migration.MigrationError):
            api.request("repos/other/grok-gadgets/issues", method="POST", payload={})
        with self.assertRaises(migration.MigrationError):
            api.request(
                "repos/adidshaft/grok-gadgets/releases", method="POST", payload={}
            )
        transport.assert_not_called()

    def test_wrong_authenticated_owner_or_permissions_block_all_writes(self):
        for login, can_push in (("other", True), (migration.OWNER, False)):
            server = FakeGH()
            server.login, server.can_push = login, can_push
            api = GitHubIssueAPI(allow_writes=True, request_runner=server)
            with self.assertRaises(migration.MigrationError):
                api.verify_targets()
            self.assertFalse(api.verified)
            self.assertEqual(server.writes, [])

    def test_http_uncertainty_never_becomes_missing_or_logs_response(self):
        self.server.failure_status = 503
        with self.assertRaisesRegex(migration.MigrationError, "HTTP 503") as caught:
            self.api.get_issue(migration.OWNER, "grok-gadgets", 9)
        self.assertNotIn("fixture secret", str(caught.exception))
        self.server.failure_status = None
        self.assertIsNone(self.api.get_issue(migration.OWNER, "grok-gadgets", 9))

    def test_malformed_json_response_fails_closed(self):
        self.api.request_runner = lambda *args, **kwargs: SimpleNamespace(
            returncode=0, stdout="HTTP/2.0 200 OK\n\nfixture secret", stderr=""
        )
        with self.assertRaisesRegex(
            migration.MigrationError, "uncertain JSON"
        ) as caught:
            self.api.request("user")
        self.assertNotIn("fixture secret", str(caught.exception))

    def test_wrong_html_url_and_pull_request_mapping_are_rejected(self):
        self.migrate()
        key = migration.OWNER, "grok-gadgets", 1
        self.server.issues[key]["html_url"] = (
            "https://github.com/other/grok-gadgets/issues/1"
        )
        with self.assertRaisesRegex(migration.MigrationError, "HTML URL"):
            self.api.get_issue(*key)
        self.server.issues[key]["html_url"] = migration.github_url(*key)
        self.server.issues[key]["pull_request"] = {}
        with self.assertRaisesRegex(migration.MigrationError, "not an issue"):
            self.api.get_issue(*key)

    def test_duplicate_and_misplaced_markers_prevent_writes(self):
        result = self.migrate()
        key = migration.OWNER, "grok-gadgets", 1
        copy_issue = copy.deepcopy(self.server.issues[key])
        copy_issue.update(number=2, html_url=migration.github_url(*key[:2], 2))
        self.server.issues[(*key[:2], 2)] = copy_issue
        before = copy.deepcopy(self.server.writes)
        with self.assertRaisesRegex(migration.MigrationError, "Multiple issues"):
            self.migrate(result)
        self.assertEqual(before, self.server.writes)
        del self.server.issues[(*key[:2], 2)]
        self.server.issues[key]["body"] = (
            "Quoted marker\n" + self.server.issues[key]["body"]
        )
        with self.assertRaisesRegex(migration.MigrationError, "misplaced"):
            self.migrate(result)
        self.assertEqual(before, self.server.writes)

    def test_incomplete_pagination_fails_instead_of_returning_partial_inventory(self):
        self.migrate()
        self.api.PAGE_SIZE = 1
        self.api.MAX_PAGES = 1
        with self.assertRaisesRegex(migration.MigrationError, "incomplete inventory"):
            self.api.list_labels(migration.OWNER, "grok-gadgets")

    def test_offline_cli_preview_never_constructs_transport_or_writes_reports(self):
        before = self.path.read_bytes()
        with (
            patch.object(cli, "ROOT", self.root),
            patch.object(cli, "GitHubIssueAPI") as api,
            patch("sys.stdout", new_callable=io.StringIO) as output,
        ):
            self.assertEqual(cli.main(["--plan", str(self.path)]), 0)
        api.assert_not_called()
        self.assertIn("Offline preview", output.getvalue())
        self.assertEqual(before, self.path.read_bytes())
        self.assertFalse((self.root / "artifacts").exists())

    def test_cli_checkpoints_real_mappings_and_resumes_after_checkpoint_failure(self):
        original = cli.atomic_json
        interrupted = False

        def save(path, value):
            nonlocal interrupted
            if (
                Path(path) == self.path
                and value.get("migration_phase") == "identities"
                and not interrupted
            ):
                interrupted = True
                raise OSError("fixture checkpoint unavailable")
            original(path, value)

        with (
            patch.object(cli, "ROOT", self.root),
            patch.object(cli, "GitHubIssueAPI", return_value=self.api),
            patch.object(cli, "atomic_json", side_effect=save),
            patch("sys.stdout", new_callable=io.StringIO),
            patch("sys.stderr", new_callable=io.StringIO),
        ):
            self.assertEqual(cli.main(["--plan", str(self.path), "--apply"]), 1)
        self.assertEqual(len(self.server.issues), 1)
        with (
            patch.object(cli, "ROOT", self.root),
            patch.object(cli, "GitHubIssueAPI", return_value=self.api),
            patch("sys.stdout", new_callable=io.StringIO),
        ):
            self.assertEqual(cli.main(["--plan", str(self.path), "--apply"]), 0)
        result = json.loads(self.path.read_text())
        self.assertTrue(result["migration_complete"])
        self.assertFalse(result["fixture_only"])
        self.assertTrue(all(row["github_number"] for row in result["records"]))
        creates = [
            call
            for call in self.server.writes
            if call[0] == "POST" and call[1].endswith("/issues")
        ]
        self.assertEqual(len(creates), 5)
        self.assertEqual(
            len(
                list(
                    (self.root / "artifacts/issue-migration").glob(
                        "apply-*/previous-mapping.json"
                    )
                )
            ),
            2,
        )

    def test_invalid_scope_and_concurrent_cli_block_before_network(self):
        plan = copy.deepcopy(self.plan)
        plan["owner"] = "other"
        migration.atomic_json(self.path, plan)
        with (
            patch.object(cli, "ROOT", self.root),
            patch.object(cli, "GitHubIssueAPI") as api,
            patch("sys.stderr", new_callable=io.StringIO),
        ):
            self.assertEqual(cli.main(["--plan", str(self.path), "--apply"]), 1)
        api.assert_not_called()
        migration.atomic_json(self.path, self.plan)
        with (
            cli.apply_lock(self.root),
            patch.object(cli, "ROOT", self.root),
            patch.object(cli, "GitHubIssueAPI") as api,
            patch("sys.stderr", new_callable=io.StringIO),
        ):
            self.assertEqual(cli.main(["--plan", str(self.path), "--apply"]), 1)
        api.assert_not_called()


if __name__ == "__main__":
    unittest.main()
