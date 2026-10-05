import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "automation"))
from recognition import apply_with_adapter, award_key, decide, dry_run


class RecognitionTests(unittest.TestCase):
    def record(self):
        return dict(
            consent=True,
            github_proof={"verified": True, "immutable_id": 7},
            reddit_proof={"verified": True, "immutable_id": "t2_r7"},
            contributions=[
                {
                    "repository": "adidshaft/grok-gadgets",
                    "merged": True,
                    "author_id": 7,
                    "kind": "docs",
                }
            ],
        )

    def outcome(self, **change):
        return decide({**self.record(), **change}).outcome

    def test_docs_and_idempotency(self):
        d = decide(self.record())
        self.assertEqual(d.outcome, "would_award")
        self.assertEqual(d.award_key, award_key("t2_r7"))
        self.assertEqual(
            decide(self.record(), {d.award_key}).outcome, "already_awarded"
        )

    def test_reject_unmerged_wrong_repo_identity_and_no_consent(self):
        pr = {"repository": "adidshaft/grok-gadgets", "merged": True, "author_id": 7}
        for change in [
            dict(consent=False),
            dict(revoked=True),
            dict(github_proof={}),
            dict(contributions=[{**pr, "repository": "elsewhere/grok-gadgets"}]),
            dict(contributions=[{**pr, "repository": "grok-gadgets"}]),
            dict(contributions=[{**pr, "merged": False}]),
            dict(contributions=[{**pr, "author_id": 99}]),
            dict(contributions=[{**pr, "author_type": "Bot"}]),
            dict(contributions=[{**pr, "automation": True}]),
            dict(github_proof={"verified": True, "immutable_id": 7, "type": "Bot"}),
        ]:
            with self.subTest(change=change):
                self.assertEqual(self.outcome(**change), "ineligible")

    def test_text_and_number_booleans_never_count_as_true(self):
        pr = {"repository": "adidshaft/grok-gadgets", "author_id": 7}
        for change in [
            dict(consent="false"),
            dict(consent="no"),
            dict(consent=1),
            dict(github_proof={"verified": "false", "immutable_id": 7}),
            dict(reddit_proof={"verified": 1, "immutable_id": "t2_r7"}),
            dict(contributions=[{**pr, "merged": "false"}]),
            dict(contributions=[{**pr, "merged": 1}]),
        ]:
            with self.subTest(change=change):
                self.assertEqual(self.outcome(**change), "ineligible")
        self.assertEqual(self.outcome(revoked="false"), "review")

    def test_ids_must_be_typed(self):
        for change in [
            dict(github_proof={"verified": True, "immutable_id": "7"}),
            dict(github_proof={"verified": True, "immutable_id": "octocat"}),
            dict(github_proof={"verified": True, "immutable_id": True}),
            dict(reddit_proof={"verified": True, "immutable_id": "someuser"}),
        ]:
            with self.subTest(change=change):
                self.assertEqual(self.outcome(**change), "ineligible")
        self.assertEqual(
            self.outcome(
                contributions=[
                    {
                        "repository": "adidshaft/grok-gadgets",
                        "merged": True,
                        "author_id": "7",
                    }
                ]
            ),
            "ineligible",
        )

    def test_changed_accounts_flairs_and_override(self):
        for k in ["renamed", "deleted"]:
            self.assertEqual(self.outcome(**{k: True}), "review")
        for flair in [
            "Maintainer",
            "maintainer",
            "Mod",
            "Hardware tester",
            "Maintainer 🛠",
        ]:
            with self.subTest(flair=flair):
                self.assertEqual(self.outcome(current_flair=flair), "preserve")
        for flair in ["", "Contributor", " contributor "]:
            with self.subTest(flair=flair):
                self.assertEqual(self.outcome(current_flair=flair), "would_award")
        for override in ["deny", "Deny", " DENY "]:
            self.assertEqual(self.outcome(manual_override=override), "ineligible")
        self.assertEqual(self.outcome(manual_override="allow"), "review")

    def test_one_link_per_account(self):
        links = {"github": {7: "t2_other"}, "reddit": {}}
        self.assertEqual(decide(self.record(), active_links=links).outcome, "review")
        links = {"github": {}, "reddit": {"t2_r7": 8}}
        self.assertEqual(decide(self.record(), active_links=links).outcome, "review")
        links = {"github": {7: "t2_r7"}, "reddit": {"t2_r7": 7}}
        self.assertEqual(
            decide(self.record(), active_links=links).outcome, "would_award"
        )

    def test_revocation_after_award_removes(self):
        key = award_key("t2_r7")
        d = decide({**self.record(), "revoked": True}, {key})
        self.assertEqual((d.outcome, d.award_key), ("would_remove", key))

        class Adapter:
            def remove(self, k):
                self.removed = k

        adapter = Adapter()
        self.assertEqual(
            apply_with_adapter(d, adapter, dry_run=False)["outcome"], "removed"
        )
        self.assertEqual(adapter.removed, key)

    def test_dry_run_privacy(self):
        r = dry_run([self.record()], now="2026-10-05T00:00:00Z")
        self.assertNotIn("github_proof", str(r))
        self.assertNotIn("t2_r7", str(r))
        self.assertTrue(r[0]["dry_run"])
        self.assertEqual(len(r[0]["inputs_digest"]), 16)
        self.assertEqual(r[0]["timestamp"], "2026-10-05T00:00:00Z")

    def test_bounded_retry_and_unknown_outcome(self):
        class Adapter:
            def award(self, key):
                raise TimeoutError()

            def was_awarded(self, key):
                return False

        d = decide(self.record())
        self.assertEqual(apply_with_adapter(d, Adapter())["attempts"], 0)
        self.assertEqual(apply_with_adapter(d, Adapter(), dry_run=False)["attempts"], 3)

        class Already(Adapter):
            def was_awarded(self, key):
                return True

        self.assertEqual(apply_with_adapter(d, Already(), dry_run=False)["attempts"], 1)

        class Flaky(Adapter):
            calls = 0

            def award(self, key):
                Flaky.calls += 1
                if Flaky.calls == 1:
                    raise ConnectionError()

        waits = []
        result = apply_with_adapter(d, Flaky(), dry_run=False, sleep=waits.append)
        self.assertEqual(result, {"outcome": "awarded", "attempts": 2})
        self.assertEqual(waits, [1])

    def test_revoked_adapter(self):
        class Adapter:
            def award(self, key):
                raise PermissionError()

        self.assertEqual(
            apply_with_adapter(decide(self.record()), Adapter(), dry_run=False)[
                "outcome"
            ],
            "authorization_revoked",
        )


if __name__ == "__main__":
    unittest.main()
