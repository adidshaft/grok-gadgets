"""Offline migration/recovery regressions. The fixture API cannot make network calls."""

import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import issue_migration as migration


class FakeAPI:
    def __init__(self):
        self.issues = {}
        self.labels = {}
        self.milestones = {}
        self.writes = []
        self.fail_after_create = False
        self.fail_after_update = False

    def list_labels(self, owner, repository):
        return list(self.labels.get((owner, repository), {}).values())

    def create_label(self, owner, repository, label):
        self.labels.setdefault((owner, repository), {})[label["name"]] = copy.deepcopy(
            label
        )
        self.writes.append(("label", repository, label["name"]))

    def list_milestones(self, owner, repository):
        return list(self.milestones.get((owner, repository), {}).values())

    def create_milestone(self, owner, repository, milestone):
        self.milestones.setdefault((owner, repository), {})[milestone["title"]] = (
            copy.deepcopy(milestone)
        )
        self.writes.append(("milestone", repository, milestone["title"]))

    def find_issues(self, owner, repository, marker):
        return [
            copy.deepcopy(issue)
            for (o, repo, _), issue in self.issues.items()
            if o == owner and repo == repository and marker in issue["body"]
        ]

    def get_issue(self, owner, repository, number):
        return copy.deepcopy(self.issues.get((owner, repository, number)))

    def create_issue(self, owner, repository, payload):
        labels = self.labels.get((owner, repository), {})
        assert set(payload["labels"]) <= set(labels), "Issue created before labels"
        assert payload["milestone"] in self.milestones.get((owner, repository), {}), (
            "Issue created before milestone"
        )
        number = (
            max([n for o, r, n in self.issues if o == owner and r == repository] or [0])
            + 1
        )
        issue = {
            **copy.deepcopy(payload),
            "number": number,
            "url": migration.github_url(owner, repository, number),
        }
        self.issues[(owner, repository, number)] = issue
        self.writes.append(("create", repository, number))
        if self.fail_after_create:
            self.fail_after_create = False
            raise OSError("fixture response lost after server create")
        return copy.deepcopy(issue)

    def update_issue(self, owner, repository, number, payload):
        assert len(self.issues) >= 5, "Dependency links/state written before identities"
        self.issues[(owner, repository, number)].update(copy.deepcopy(payload))
        self.writes.append(("update", repository, number))
        if self.fail_after_update:
            self.fail_after_update = False
            raise OSError("fixture response lost after update")


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.root = self.workspace / "grok-gadgets"
        self.ledgers = {}
        for index, repository in enumerate(migration.REPOSITORIES):
            repo = self.workspace / repository
            (repo / "planning").mkdir(parents=True)
            issue = {
                "id": f"TEST-{index}",
                "problem": "Fixture " + repository,
                "acceptance": ["Works in software"],
                "evidence": ["fixture"],
                "commits": ["fixture-commit"],
                "labels": ["docs"],
                "milestone": "M0",
                "stage": "done" if index == 0 else "blocked" if index == 1 else "ready",
                "dependencies": ["grok-gadgets#TEST-0"] if index == 2 else [],
                "blocker": "Fixture prerequisite" if index == 1 else None,
            }
            self.ledgers[repository] = [issue]
            migration.atomic_json(repo / "planning/issues.json", [issue])
        (self.root / "publication").mkdir()
        self.labels = [
            {"name": "docs", "description": "Documentation", "color": "abcdef"}
        ]
        self.milestones = [{"id": "M0", "title": "Foundations"}]
        migration.atomic_json(self.root / "publication/labels.json", self.labels)
        migration.atomic_json(self.root / "planning/milestones.json", self.milestones)
        self.api = FakeAPI()
        self.checkpoints = []

    def prepare(self, existing=None):
        return migration.prepare(self.root, existing)

    def run_fixture(self, plan, checkpoint=None):
        return migration.FixtureMigrator(
            self.api, checkpoint or self.checkpoints.append
        ).run(plan)

    def change_issue(self, repository, **values):
        self.ledgers[repository][0].update(values)
        migration.atomic_json(
            self.workspace / repository / "planning/issues.json",
            self.ledgers[repository],
        )

    def test_preparation_preserves_mappings_unknown_rows_and_extensions(self):
        plan = self.prepare()
        row = plan["records"][0]
        row.update(
            github_number=8,
            github_url=migration.github_url(row["owner"], row["repository"], 8),
            private_extra={"opaque": 1},
        )
        unknown = {
            "owner": "adidshaft",
            "repository": "grok-gadgets",
            "local_id": "OLD-99",
            "github_number": 99,
            "github_url": "https://github.com/adidshaft/grok-gadgets/issues/99",
            "source": "grok-gadgets/planning/issues.json",
            "opaque": "keep",
            "record": {"stage": "done"},
        }
        plan["records"].append(unknown)
        plan["custom_top_level"] = "keep"
        regenerated = self.prepare(plan)
        known = next(
            r for r in regenerated["records"] if r["mapping_key"] == row["mapping_key"]
        )
        self.assertEqual(known["github_number"], 8)
        self.assertEqual(known["github_url"], row["github_url"])
        self.assertEqual(known["private_extra"], {"opaque": 1})
        retained = next(r for r in regenerated["records"] if r["local_id"] == "OLD-99")
        self.assertEqual(retained["opaque"], "keep")
        self.assertFalse(retained["source_present"])
        self.assertEqual(regenerated["custom_top_level"], "keep")
        self.assertTrue(regenerated["validation"]["ready"])
        self.assertEqual({r["owner"] for r in regenerated["records"]}, {"adidshaft"})

    def test_successful_rerun_has_zero_creates_or_updates(self):
        result = self.run_fixture(self.prepare())
        before = list(self.api.writes)
        resumed = self.run_fixture(self.prepare(result))
        self.assertEqual(self.api.writes, before)
        self.assertTrue(resumed["migration_complete"])
        self.assertEqual(len(self.api.issues), 5)
        self.assertEqual(
            self.api.issues[("adidshaft", "grok-gadgets", 1)]["state"], "closed"
        )
        self.assertEqual(
            self.api.issues[("adidshaft", "grok-gadgets-gateway", 1)]["state"], "open"
        )
        for issue in self.api.issues.values():
            self.assertIn("<!-- grok-gadgets-local-id:", issue["body"])
        body = self.api.issues[("adidshaft", "grok-gadgets-linux-sdk", 1)]["body"]
        self.assertIn("https://github.com/adidshaft/grok-gadgets/issues/1", body)
        self.assertTrue(
            all(row["github_number"] for row in self.checkpoints[-6]["records"])
        )

    def test_interrupted_create_response_reconciles_before_new_create(self):
        self.api.fail_after_create = True
        with self.assertRaises(OSError):
            self.run_fixture(self.prepare())
        self.assertEqual(len(self.api.issues), 1)
        result = self.run_fixture(self.checkpoints[-1])
        self.assertEqual(len(self.api.issues), 5)
        self.assertEqual(sum(write[0] == "create" for write in self.api.writes), 5)
        self.assertTrue(result["migration_complete"])

    def test_interrupted_checkpoint_recovers_unsaved_number_by_marker(self):
        saved = []

        def checkpoint(plan):
            if plan["fixture_phase"] == "identities":
                raise OSError("fixture checkpoint unavailable")
            saved.append(plan)

        with self.assertRaises(OSError):
            self.run_fixture(self.prepare(), checkpoint)
        self.assertEqual(len(self.api.issues), 1)
        self.run_fixture(saved[-1])
        self.assertEqual(sum(write[0] == "create" for write in self.api.writes), 5)

    def test_interrupted_phase_two_preserves_ids_and_resumes(self):
        self.api.fail_after_update = True
        with self.assertRaises(OSError):
            self.run_fixture(self.prepare())
        self.assertTrue(
            all(row["github_number"] for row in self.checkpoints[-1]["records"])
        )
        self.run_fixture(self.checkpoints[-1])
        self.assertEqual(sum(write[0] == "create" for write in self.api.writes), 5)

    def test_stale_mapping_to_unrelated_issue_blocks_all_writes(self):
        plan = self.prepare()
        row = plan["records"][0]
        row.update(
            github_number=7,
            github_url=migration.github_url(row["owner"], row["repository"], 7),
        )
        self.api.issues[(row["owner"], row["repository"], 7)] = {
            "number": 7,
            "url": row["github_url"],
            "body": "Unrelated issue",
            "state": "open",
        }
        with self.assertRaisesRegex(migration.MigrationError, "unrelated"):
            self.run_fixture(plan)
        self.assertEqual(self.api.writes, [])
        self.assertEqual(
            self.api.issues[(row["owner"], row["repository"], 7)]["state"], "open"
        )

    def test_stale_deleted_mapping_with_correct_marker_repairs_and_keeps_history(self):
        plan = self.prepare()
        row = plan["records"][0]
        row.update(
            github_number=7,
            github_url=migration.github_url(row["owner"], row["repository"], 7),
        )
        self.api.issues[(row["owner"], row["repository"], 9)] = {
            "number": 9,
            "url": migration.github_url(row["owner"], row["repository"], 9),
            "body": row["marker"],
            "state": "open",
        }
        result = self.run_fixture(plan)
        repaired = result["records"][0]
        self.assertEqual(repaired["github_number"], 9)
        self.assertEqual(repaired["mapping_history"][0]["github_number"], 7)
        self.assertEqual(sum(write[0] == "create" for write in self.api.writes), 4)

    def test_deleted_mapping_without_marker_requires_review(self):
        plan = self.prepare()
        plan["records"][0].update(github_number=7, github_url=None)
        with self.assertRaisesRegex(migration.MigrationError, "no longer exists"):
            self.run_fixture(plan)
        self.assertFalse(self.api.writes)

    def test_duplicate_markers_and_stored_number_collisions_fail_closed(self):
        plan = self.prepare()
        row = plan["records"][0]
        for number in (1, 2):
            self.api.issues[(row["owner"], row["repository"], number)] = {
                "number": number,
                "url": migration.github_url(row["owner"], row["repository"], number),
                "body": row["marker"],
            }
        with self.assertRaisesRegex(migration.MigrationError, "Multiple issues"):
            self.run_fixture(plan)
        self.assertEqual(self.api.writes, [])
        row.update(github_number=1)
        duplicate = {
            **row,
            "local_id": "COLLISION-1",
            "mapping_key": "adidshaft/grok-gadgets/COLLISION-1",
        }
        with self.assertRaisesRegex(migration.MigrationError, "same GitHub issue"):
            migration.validate_mappings([row, duplicate])

    def test_two_markers_on_one_issue_fail_before_prerequisite_writes(self):
        plan = self.prepare()
        first = next(
            row for row in plan["records"] if row["repository"] == "grok-gadgets"
        )
        other = copy.deepcopy(first)
        other.update(
            local_id="OTHER-1",
            mapping_key="adidshaft/grok-gadgets/OTHER-1",
            marker=migration.marker("adidshaft/grok-gadgets/OTHER-1"),
        )
        plan["records"].append(other)
        self.api.issues[("adidshaft", "grok-gadgets", 1)] = {
            "number": 1,
            "url": "https://github.com/adidshaft/grok-gadgets/issues/1",
            "body": first["marker"] + other["marker"],
        }
        with self.assertRaisesRegex(migration.MigrationError, "markers collide"):
            self.run_fixture(plan)
        self.assertFalse(self.api.writes)

    def test_manifest_label_gap_description_and_combined_milestone_block(self):
        self.change_issue("grok-gadgets", labels=["simulator"], milestone="M5/M8")
        plan = self.prepare()
        self.assertFalse(plan["validation"]["ready"])
        self.assertTrue(
            any(
                "Undeclared label simulator" in error
                for error in plan["validation"]["errors"]
            )
        )
        self.assertTrue(any("M5/M8" in error for error in plan["validation"]["errors"]))
        with self.assertRaisesRegex(migration.MigrationError, "validation must pass"):
            self.run_fixture(plan)
        self.assertFalse(self.api.writes)
        self.labels[0].pop("description")
        self.assertFalse(
            migration.check_manifests(self.labels, self.milestones, [])["ready"]
        )

    def test_missing_ambiguous_and_explicit_dependencies(self):
        self.change_issue("grok-gadgets-linux-sdk", dependencies=["MISSING-99"])
        self.assertFalse(self.prepare()["validation"]["ready"])
        self.change_issue("grok-gadgets", id="SHARED-1")
        self.change_issue("grok-gadgets-gateway", id="SHARED-1")
        self.change_issue("grok-gadgets-linux-sdk", dependencies=["SHARED-1"])
        self.assertFalse(self.prepare()["validation"]["ready"])
        self.change_issue(
            "grok-gadgets-linux-sdk",
            dependencies=["grok-gadgets#SHARED-1", "authorized hardware"],
        )
        plan = self.prepare()
        self.assertTrue(plan["validation"]["ready"])
        row = next(
            r for r in plan["records"] if r["repository"] == "grok-gadgets-linux-sdk"
        )
        self.assertIn("authorized hardware (external prerequisite)", row["issue_body"])

    def test_unknown_retained_issue_is_verified_but_never_updated(self):
        plan = self.prepare()
        unknown = migration.normalize_record(
            {
                "repository": "grok-gadgets",
                "local_id": "OLD-1",
                "github_number": 20,
                "record": {"stage": "done"},
                "source_present": False,
            },
            "adidshaft",
        )
        plan["records"].append(unknown)
        self.api.issues[("adidshaft", "grok-gadgets", 20)] = {
            "number": 20,
            "url": unknown["github_url"],
            "body": unknown["marker"] + "\nUnchanged historical content",
            "state": "open",
        }
        self.run_fixture(plan)
        self.assertNotIn(("update", "grok-gadgets", 20), self.api.writes)
        self.assertEqual(
            self.api.issues[("adidshaft", "grok-gadgets", 20)]["state"], "open"
        )

    def test_wrong_url_and_duplicate_source_ids_are_rejected(self):
        plan = self.prepare()
        plan["records"][0].update(
            github_number=1, github_url="https://github.com/wrong/repo/issues/1"
        )
        with self.assertRaisesRegex(migration.MigrationError, "URL disagrees"):
            self.prepare(plan)
        issues = self.ledgers["grok-gadgets"] * 2
        migration.atomic_json(self.root / "planning/issues.json", issues)
        with self.assertRaisesRegex(migration.MigrationError, "Duplicate source"):
            self.prepare()

    def test_legacy_mapping_source_becomes_portable(self):
        row = migration.normalize_record(
            {
                "repository": "grok-gadgets",
                "local_id": "OLD-1",
                "source": "/private/workspace/grok-gadgets/planning/issues.json",
            },
            "adidshaft",
        )
        self.assertEqual(row["source"], "grok-gadgets/planning/issues.json")

    def test_checkout_directory_name_does_not_affect_source_identity(self):
        renamed = self.workspace / "arbitrary-hub-checkout"
        self.root.rename(renamed)
        self.root = renamed
        plan = self.prepare()
        self.assertTrue(plan["validation"]["ready"])
        self.assertTrue(
            all(
                row["source"] == row["repository"] + "/planning/issues.json"
                for row in plan["records"]
            )
        )

    def test_changed_manifest_is_revalidated_before_fake_writes(self):
        plan = self.prepare()
        plan["labels"] = []
        with self.assertRaisesRegex(
            migration.MigrationError, "Current manifest validation"
        ):
            self.run_fixture(plan)
        self.assertFalse(self.api.writes)

    def test_readback_detects_ignored_label_update(self):
        original = self.api.update_issue

        def ignored_labels(owner, repository, number, payload):
            original(owner, repository, number, payload)
            self.api.issues[(owner, repository, number)]["labels"] = []

        self.api.update_issue = ignored_labels
        with self.assertRaisesRegex(migration.MigrationError, "verification failed"):
            self.run_fixture(self.prepare())
        self.assertFalse(self.checkpoints[-1].get("migration_complete", False))

    def test_cli_scratch_preview_preserves_canonical_file_and_recovery_snapshot(self):
        script = Path(__file__).with_name("prepare-issue-migration.py")
        spec = importlib.util.spec_from_file_location("prepare_issue_migration", script)
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
        existing = self.prepare()
        row = existing["records"][0]
        row.update(
            github_number=31,
            github_url=migration.github_url(row["owner"], row["repository"], 31),
        )
        canonical = self.root / "publication/issue-migration.json"
        migration.atomic_json(canonical, existing)
        before = canonical.read_bytes()
        output = self.root / "scratch-preview.json"
        reports = self.root / "private-reports"
        with (
            patch.object(cli, "ROOT", self.root),
            patch(
                "sys.argv",
                [str(script), "--output", str(output), "--report-dir", str(reports)],
            ),
            patch("sys.stdout", io.StringIO()),
        ):
            self.assertEqual(cli.main(), 0)
        self.assertEqual(canonical.read_bytes(), before)
        preview = json.loads(output.read_text())
        restored = json.loads(next(reports.glob("*.json")).read_text())
        self.assertEqual(preview["records"][0]["github_number"], 31)
        self.assertEqual(restored["previous_mapping_snapshot"], existing)
        self.assertEqual(restored["remote_actions"], 0)

    def test_completed_migration_refuses_apply_without_force(self):
        script = Path(__file__).with_name("migrate-github-issues.py")
        spec = importlib.util.spec_from_file_location("migrate_github_issues", script)
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
        plan = self.root / "completed.json"
        plan.write_text(
            json.dumps(
                {"owner": "adidshaft", "activated": True, "migration_complete": True}
            )
        )
        stderr = io.StringIO()
        with (
            patch.object(cli, "ROOT", self.root),
            patch.object(cli, "GitHubIssueAPI", side_effect=AssertionError("no API")),
            patch("sys.stderr", stderr),
        ):
            self.assertEqual(cli.main(["--plan", str(plan), "--apply"]), 1)
        self.assertIn("already completed", stderr.getvalue())
        with self.assertRaises(migration.MigrationError):
            cli.refuse_completed(plan, force=False)
        cli.refuse_completed(plan, force=True)

    def test_duplicate_milestone_id_and_title_reconciles_once(self):
        local = [
            {
                "id": "M0",
                "title": "Foundations",
                "scope": "Historical acceptance",
                "stage": "done",
            }
        ]
        public = [
            {
                "id": "M0",
                "title": "Foundations",
                "description": "Remote readable description",
            }
        ]
        migration.atomic_json(self.root / "planning/milestones.json", local)
        migration.atomic_json(self.root / "publication/milestones.json", public)
        plan = self.prepare()
        self.assertTrue(plan["validation"]["ready"])
        self.assertEqual(
            plan["milestones"], [{**local[0], "description": public[0]["description"]}]
        )
        self.assertEqual(self.prepare(plan)["milestones"], plan["milestones"])
        self.run_fixture(plan)
        self.assertEqual(
            sum(operation[0] == "milestone" for operation in self.api.writes), 5
        )

    def test_duplicate_milestone_id_with_different_title_rejected(self):
        migration.atomic_json(
            self.root / "publication/milestones.json",
            [{"id": "M0", "title": "Different scope"}],
        )
        with self.assertRaisesRegex(
            migration.MigrationError, "Conflicting milestone titles"
        ):
            self.prepare()

    def test_duplicate_milestone_scope_conflict_rejected(self):
        migration.atomic_json(
            self.root / "planning/milestones.json",
            [{"id": "M0", "title": "Foundations", "scope": "Software only"}],
        )
        migration.atomic_json(
            self.root / "publication/milestones.json",
            [
                {
                    "id": "M0",
                    "title": "Foundations",
                    "scope": "Physical acceptance required",
                }
            ],
        )
        with self.assertRaisesRegex(
            migration.MigrationError, "Conflicting milestone scope"
        ):
            self.prepare()

    def test_atomic_write_failure_keeps_existing_checkpoint(self):
        path = self.root / "publication/checkpoint.json"
        migration.atomic_json(path, {"known": 12})
        with patch.object(
            migration.os, "replace", side_effect=OSError("fixture interruption")
        ):
            with self.assertRaises(OSError):
                migration.atomic_json(path, {"known": None})
        self.assertEqual(json.loads(path.read_text()), {"known": 12})
        self.assertFalse(list(path.parent.glob(".checkpoint.json-*")))


if __name__ == "__main__":
    unittest.main()
