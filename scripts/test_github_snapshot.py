"""Offline snapshot acceptance through the existing paginated GitHub REST adapter."""

import copy
from datetime import datetime, timezone
import importlib.util
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from github_issue_api import GitHubIssueAPI
import github_snapshot as snapshot
from issue_migration import OWNER, REPOSITORIES, MigrationError, github_url, marker

spec = importlib.util.spec_from_file_location(
    "refresh_github_snapshot", Path(__file__).with_name("refresh-github-snapshot.py")
)
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)
NOW = datetime(2026, 10, 5, 12, 0, tzinfo=timezone.utc)


def raw_issue(repository, number=1, *, body="", state="open"):
    return {
        "number": number,
        "html_url": github_url(OWNER, repository, number),
        "title": "Issue from GitHub",
        "body": body,
        "state": state,
        "labels": [{"name": "gateway"}, {"name": "P1"}],
        "milestone": None,
    }


class FakeGH:
    def __init__(self):
        self.rows = {repo: [raw_issue(repo)] for repo in REPOSITORIES}
        self.calls = []
        self.failure = None

    def __call__(self, command, **kwargs):
        self.calls.append(command)
        method = command[command.index("--method") + 1]
        if method != "GET":
            raise AssertionError("Snapshot attempted a GitHub mutation")
        self.assert_endpoint(command, kwargs)
        parsed = urlsplit(command[2])
        repository = parsed.path.split("/")[2]
        query = parse_qs(parsed.query)
        page, size = int(query["page"][0]), int(query["per_page"][0])
        failed = self.failure == (repository, page)
        rows = self.rows[repository][(page - 1) * size : page * size]
        return SimpleNamespace(
            returncode=1 if failed else 0,
            stdout="HTTP/2.0 "
            + ("503 Failure" if failed else "200 OK")
            + "\r\nContent-Type: application/json\r\n\r\n"
            + json.dumps(
                {"message": "fixture response is private"} if failed else rows
            ),
            stderr="fixture transport diagnostics must not be printed"
            if failed
            else "",
        )

    @staticmethod
    def assert_endpoint(command, kwargs):
        parsed = urlsplit(command[2])
        pieces = parsed.path.split("/")
        assert pieces[0:2] == ["repos", OWNER]
        assert pieces[2] in REPOSITORIES and pieces[3:] == ["issues"]
        assert parse_qs(parsed.query)["state"] == ["all"]
        assert command[command.index("--hostname") + 1] == "github.com"
        assert kwargs["input"] is None
        assert "GH_DEBUG" not in kwargs["env"]


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "github-issues.json"
        self.server = FakeGH()
        self.api = GitHubIssueAPI(request_runner=self.server)
        self.api.PAGE_SIZE = 2
        self.api.verify_targets = lambda: self.fail(
            "Read-only snapshot used write preflight"
        )

    def refresh(self):
        return snapshot.refresh_snapshot(self.path, self.api, now=NOW)

    def assert_previous_preserved(self):
        self.path.write_bytes(b"previous public snapshot\n")
        before = self.path.read_bytes()
        with self.assertRaises(MigrationError):
            self.refresh()
        self.assertEqual(self.path.read_bytes(), before)

    def test_complete_paginated_read_only_inventory_includes_new_issues_not_prs(self):
        repo = REPOSITORIES[0]
        migrated = raw_issue(
            repo,
            body=marker(f"{OWNER}/{repo}/HUB-001") + "\nStatus: **blocked**",
        )
        migrated["milestone"] = {"number": 1, "title": "ML — Launch"}
        pull = raw_issue(repo, 2)
        pull.update(
            html_url=f"https://github.com/{OWNER}/{repo}/pull/2", pull_request={}
        )
        contribution = raw_issue(
            repo, 3, body="A new contribution without a local ledger."
        )
        contribution["title"] = "A new <component> report"
        self.server.rows[repo] = [migrated, pull, contribution]
        result = self.refresh()
        self.assertEqual(result["source"], "GitHub Issues")
        self.assertEqual(result["refreshed_at"], "2026-10-05T12:00:00Z")
        self.assertEqual(len(result["issues"]), 6)
        rows = [row for row in result["issues"] if row["repository"] == repo]
        self.assertEqual([row["id"] for row in rows], ["HUB-001", f"{repo}#3"])
        self.assertEqual(rows[0]["milestone"], "ML — Launch")
        self.assertEqual(rows[0]["stage"], "blocked")
        self.assertEqual(rows[1]["stage"], "proposed")
        self.assertEqual(rows[1]["milestone"], "Unscheduled")
        self.assertEqual(rows[1]["problem"], "A new <component> report")
        self.assertEqual(snapshot.load_snapshot(self.path), result)
        self.assertTrue(any("page=2" in command[2] for command in self.server.calls))
        self.assertEqual(
            {urlsplit(command[2]).path.split("/")[2] for command in self.server.calls},
            set(REPOSITORIES),
        )
        self.assertFalse(self.api.allow_writes)
        self.assertFalse(self.api.verified)
        self.assertNotIn("local ledger", self.path.read_text())

    def test_page_failure_and_exhaustion_preserve_previous_snapshot(self):
        repo = REPOSITORIES[0]
        self.server.rows[repo] = [raw_issue(repo, 1), raw_issue(repo, 2)]
        self.server.failure = (repo, 2)
        self.assert_previous_preserved()
        self.server.failure = None
        self.api.MAX_PAGES = 1
        self.assert_previous_preserved()

    def test_fifth_repository_failure_never_persists_partial_success(self):
        self.server.failure = (REPOSITORIES[-1], 1)
        self.assert_previous_preserved()
        self.assertEqual(len(self.server.calls), 5)

    def test_closed_state_overrides_body_and_open_done_is_neutralized(self):
        repo = REPOSITORIES[0]
        cases = [
            (
                "Status: **blocked**\n### Blocked by\nWaiting for review",
                "closed",
                "done",
            ),
            ("Status: **done**", "open", "proposed"),
            ("Status: **review**", "open", "review"),
            ("Status: something new", "open", "proposed"),
            ("Status: ready\nStatus: blocked", "open", "proposed"),
            (
                "~~~\nStatus: done\n~~~\n> Status: done\nStatus: blocked",
                "open",
                "blocked",
            ),
            ("~~~~\n~~~\nStatus: done\n~~~~\nStatus: ready", "open", "ready"),
            ("    Status: done\nStatus: review", "open", "review"),
        ]
        for body, state, stage in cases:
            with self.subTest(body=body, state=state):
                self.server.rows[repo] = [raw_issue(repo, body=body, state=state)]
                row = next(
                    row for row in self.refresh()["issues"] if row["repository"] == repo
                )
                self.assertEqual(row["stage"], stage)
                if stage != "blocked":
                    self.assertIsNone(row["blocker"])

    def test_malformed_markers_and_duplicate_ids_preserve_previous_snapshot(self):
        repo = REPOSITORIES[0]
        valid = marker(f"{OWNER}/{repo}/HUB-001")
        malformed = [
            "Quoted marker\n" + valid,
            valid + "\n" + valid,
            marker(f"other/{repo}/HUB-001"),
            marker(f"{OWNER}/{REPOSITORIES[1]}/HUB-001"),
            marker(f"{OWNER}/{repo}/../bad"),
            valid[:-3],
            "\n" + valid,
        ]
        for body in malformed:
            with self.subTest(body=body):
                self.server.rows[repo] = [raw_issue(repo, body=body)]
                self.assert_previous_preserved()
        self.server.rows[repo] = [
            raw_issue(repo, 1, body=valid),
            raw_issue(repo, 2, body=valid),
        ]
        self.assert_previous_preserved()

    def test_wrong_or_malformed_urls_and_duplicate_numbers_preserve_snapshot(self):
        repo = REPOSITORIES[0]
        for url in [
            "https://github.com/other/grok-gadgets/issues/1",
            github_url(OWNER, repo, 1) + "?redirect=1",
            "http://github.com/adidshaft/grok-gadgets/issues/1",
            "javascript:fixture",
        ]:
            with self.subTest(url=url):
                row = raw_issue(repo)
                row["html_url"] = url
                self.server.rows[repo] = [row]
                self.assert_previous_preserved()
        self.server.rows[repo] = [raw_issue(repo), raw_issue(repo)]
        self.assert_previous_preserved()

    def test_only_short_safe_blocker_sections_are_exported_without_raw_bodies(self):
        repo = REPOSITORIES[0]
        for text, expected in [
            (
                "Supported scoped connector reload is unavailable.",
                "Supported scoped connector reload is unavailable.",
            ),
            ("password=fixture-only", None),
            ("Read the report in /home/sample/private", None),
            ("Endpoint http://127.0.0.1:8123 needs access", None),
            ("Endpoint https://device.local needs access", None),
            ("Ask person@example.com for access", None),
            ("x" * 501, None),
        ]:
            with self.subTest(text=text):
                body = (
                    "Status: **blocked**\n\n### Evidence\n"
                    "fixture raw report must not be copied\n\n### Blocked by\n"
                    + text
                    + "\n\n### Dependencies\nprivate report context"
                )
                self.server.rows[repo] = [raw_issue(repo, body=body)]
                row = next(
                    row for row in self.refresh()["issues"] if row["repository"] == repo
                )
                self.assertEqual(row["blocker"], expected)
                self.assertNotIn("fixture raw report", self.path.read_text())
                self.assertNotIn("private report context", self.path.read_text())
                self.assertNotIn('"body"', self.path.read_text())

    def test_atomic_replace_failure_preserves_old_bytes_and_cleans_staging(self):
        self.path.write_bytes(b"previous public snapshot\n")
        with patch(
            "issue_migration.os.replace", side_effect=OSError("fixture write failure")
        ):
            with self.assertRaises(OSError):
                self.refresh()
        self.assertEqual(self.path.read_bytes(), b"previous public snapshot\n")
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_offline_loader_rejects_tampering_and_never_constructs_transport(self):
        result = self.refresh()
        with patch.object(
            snapshot, "GitHubIssueAPI", side_effect=AssertionError("network")
        ):
            self.assertEqual(snapshot.load_snapshot(self.path), result)
            with patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(cli.main(["--check", "--output", str(self.path)]), 0)
        for changed in [
            {"github_url": "https://github.com/other/grok-gadgets/issues/1"},
            {"stage": "done", "state": "open"},
            {"stage": "blocked", "state": "closed"},
            {"stage": []},
            {"body": "raw body must not enter the public snapshot"},
        ]:
            bad = copy.deepcopy(result)
            bad["issues"][0].update(changed)
            self.path.write_text(json.dumps(bad))
            with self.assertRaises(snapshot.SnapshotError):
                snapshot.load_snapshot(self.path)

    def test_cli_error_does_not_print_transport_response_or_body(self):
        with (
            patch.object(
                cli,
                "refresh_snapshot",
                side_effect=MigrationError("fixture private response"),
            ),
            patch("sys.stderr", new_callable=io.StringIO) as stderr,
        ):
            self.assertEqual(cli.main(["--output", str(self.path)]), 1)
        self.assertIn("previous snapshot preserved", stderr.getvalue())
        self.assertNotIn("fixture private response", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
