import unittest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timezone
from urllib.error import URLError
from activity import summarize, refresh


class ActivityTests(unittest.TestCase):
    def test_counts_and_deduplication(self):
        now = datetime(2026, 10, 4, tzinfo=timezone.utc)
        r = dict(
            name="fixture",
            stars=3,
            issues=[{}, {"pull_request": {}}],
            contributors=[{"id": 1}, {"id": 2, "type": "Bot"}],
            pulls=[
                {"merged_at": "2026-10-01T00:00:00Z", "user": {"id": 1}},
                {"merged_at": None, "user": {"id": 3}},
                {"merged_at": "2025-01-01T00:00:00Z", "user": {"id": 4}},
            ],
            releases=[],
        )
        result = summarize([r, r], now)
        self.assertEqual(
            (
                result["aggregate_stars"],
                result["open_issues"],
                result["contributors"],
                result["active_contributors"],
            ),
            (6, 2, 1, 1),
        )

    def test_failed_refresh_and_owner_isolation(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "cache.json"
            p.write_text(
                json.dumps(
                    dict(
                        state="live",
                        owner="old",
                        last_successful_refresh="2020-01-01T00:00:00+00:00",
                        data={},
                    )
                )
            )

            def fail(*args):
                raise URLError("no")

            self.assertEqual(refresh("new", p, fail)["state"], "unavailable")
            self.assertEqual(refresh("old", p, fail)["state"], "cached")

    def test_invalid_owner(self):
        with self.assertRaises(ValueError):
            refresh("../private", Path("/tmp/unused"))


if __name__ == "__main__":
    unittest.main()
