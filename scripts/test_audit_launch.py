"""Privacy audit fixtures: deleted secrets, extra refs and package attribution."""

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile
import io

SPEC = importlib.util.spec_from_file_location(
    "audit_launch", Path(__file__).with_name("audit-launch.py")
)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "fixture"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Private Fixture")
        self.git("config", "user.email", "private-fixture@example.invalid")
        (self.repo / "LICENSE").write_text("Apache fixture\n")
        (self.repo / "NOTICE").write_text("Original notice\n")

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args])

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD").decode().strip()

    def test_deleted_blob_metadata_and_extra_refs_are_redacted(self):
        secret = "ghp_" + "F" * 36
        (self.repo / "removed.txt").write_text(
            secret + "\n/Users/private-fixture/work\n"
        )
        (self.repo / "binary.bin").write_bytes(b"\0" + b"x" * audit.LARGE_BYTES)
        first = self.commit("initial /Users/private-fixture/project")
        (self.repo / "removed.txt").unlink()
        (self.repo / "binary.bin").unlink()
        current = self.commit("remove old evidence")
        self.git("checkout", "-q", "--detach", first)
        (self.repo / "extra.txt").write_text("private extra ref\n")
        extra = self.commit("recovery checkpoint")
        self.git("update-ref", "refs/codex/turns/fixture", extra)
        self.git("checkout", "-q", "main")
        result = audit.audit_repository(self.repo)
        encoded = json.dumps(result)
        self.assertNotIn(secret, encoded)
        self.assertNotIn("private-fixture@example.invalid", encoded)
        self.assertNotIn("/Users/private-fixture/", encoded)
        self.assertEqual(result["head"], current)
        self.assertEqual(result["commits_head"], 2)
        self.assertEqual(result["commits_all_refs"], 3)
        self.assertIn(extra, result["extra_commits"])
        self.assertEqual(result["summary"]["history_findings"]["github_token"], 1)
        self.assertEqual(result["summary"]["working_findings"], {})
        self.assertEqual(result["summary"]["large_blobs"], 1)
        self.assertEqual(result["summary"]["binary_blobs"], 1)
        self.assertEqual(result["summary"]["extra_ref_only_blobs"], 1)
        self.assertEqual(self.git("rev-parse", "HEAD").decode().strip(), current)
        self.assertIn("refs/codex/turns/fixture", {r["ref"] for r in result["refs"]})

    def test_codex_direct_tree_ref_is_scanned_without_commit(self):
        current = self.commit("baseline")
        secret = "ghp_" + "R" * 36
        (self.repo / "tree-only.txt").write_text(secret)
        self.git("add", "tree-only.txt")
        tree_oid = self.git("write-tree").decode().strip()
        self.git("update-ref", "refs/codex/tree-only", tree_oid)
        self.git("reset", "--hard", current)
        result = audit.audit_repository(self.repo)
        self.assertEqual(result["commits_all_refs"], 1)
        self.assertEqual(result["summary"]["extra_ref_only_blobs"], 1)
        self.assertEqual(result["summary"]["history_findings"]["github_token"], 1)
        self.assertNotIn(secret, json.dumps(result))
        ref = next(r for r in result["refs"] if r["ref"] == "refs/codex/tree-only")
        self.assertEqual(ref["object_type"], "tree")

    def test_large_batch_request_avoids_pipe_deadlock(self):
        self.commit("baseline")
        oid = self.git("rev-parse", "HEAD:LICENSE").decode().strip()
        payloads = audit.blob_payloads(self.repo, [oid] * 600)
        self.assertEqual(payloads, {oid: b"Apache fixture\n"})

    def test_working_change_and_notice_variants_are_identified(self):
        self.commit("baseline")
        (self.repo / "NOTICE").write_text("updated attribution\n")
        self.commit("notice update")
        (self.repo / "README.md").write_text("/Users/private-fixture/run\n")
        self.git("add", "README.md")
        result = audit.audit_repository(self.repo)
        self.assertTrue(result["tracked_worktree_dirty"])
        self.assertEqual(len(result["licenses"]["NOTICE"]["versions"]), 2)
        self.assertEqual(result["summary"]["working_findings"]["private_host_path"], 1)

    def test_archive_attribution_and_nested_contents_are_reviewed(self):
        secret = "xai-" + "z" * 40
        nested = io.BytesIO()
        with zipfile.ZipFile(nested, "w") as z:
            z.writestr("nested.txt", secret)
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("pkg.dist-info/licenses/LICENSE", "Apache fixture")
            z.writestr("pkg.dist-info/licenses/NOTICE", "Original notice")
            z.writestr("pkg.dist-info/METADATA", "License-Expression: Apache-2.0\n")
            z.writestr("evidence.txt", secret)
            z.writestr("nested.zip", nested.getvalue())
        result = audit.archive_review(stream.getvalue())
        self.assertEqual(len(result["license_files"]), 2)
        self.assertTrue(result["metadata"][0]["apache_expression"])
        self.assertIn("nested.zip", result["nested_archives"])
        self.assertTrue(result["nested_archive_contents_scanned"])
        self.assertEqual(
            result["nested_reviews"][0]["review"]["findings"][0]["kinds"],
            {"xai_key": 1},
        )
        self.assertNotIn(secret, json.dumps(result))
        self.assertIn("xai_key", result["findings"][0]["kinds"])


if __name__ == "__main__":
    unittest.main()
