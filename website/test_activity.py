import unittest
import tempfile
import json
import os
import subprocess
import sys
from unittest.mock import patch
from pathlib import Path
from datetime import datetime, timedelta, timezone
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
                        data=dict(
                            aggregate_stars=17,
                            open_issues=2,
                            contributors=3,
                            active_contributors=1,
                            releases=[],
                        ),
                    )
                )
            )

            def fail(*args):
                raise URLError("no")

            self.assertEqual(refresh("old", p, fail)["state"], "cached")
            self.assertEqual(json.loads(p.read_text())["state"], "cached")
            self.assertEqual(refresh("new", p, fail)["state"], "unavailable")
            self.assertNotIn("data", json.loads(p.read_text()))

    def test_persisted_failure_build_and_owner_switch(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as d:
            cache = Path(d) / "cache.json"
            stamp = "2020-01-01T00:00:00+00:00"
            cache.write_text(
                json.dumps(
                    dict(
                        state="live",
                        owner="old",
                        last_successful_refresh=stamp,
                        data=dict(
                            aggregate_stars=1739,
                            open_issues=2,
                            contributors=3,
                            active_contributors=1,
                            releases=[
                                dict(
                                    repository="old",
                                    name="<script>evil</script>",
                                    date="2020",
                                )
                            ],
                        ),
                    )
                )
            )

            def fail(*args):
                raise URLError("private failure detail must not be stored")

            try:
                for owner, state in [("old", "cached"), ("new", "unavailable")]:
                    result = refresh(owner, cache, fail)
                    self.assertEqual(result, json.loads(cache.read_text()))
                    self.assertNotIn("private failure", cache.read_text())
                    env = {**os.environ, "GROK_ACTIVITY_FILE": str(cache)}
                    subprocess.run(
                        [sys.executable, "website/build.py"],
                        cwd=root,
                        env=env,
                        check=True,
                        capture_output=True,
                    )
                    html = (root / "website/dist/activity.html").read_text()
                    self.assertIn(state.upper(), html)
                    self.assertNotIn("<script>evil", html)
                    if state == "cached":
                        self.assertIn(stamp, html)
                        self.assertIn("1739", html)
                        self.assertNotIn("LIVE —", html)
                    else:
                        self.assertNotIn("1739", html)
            finally:
                env = dict(os.environ)
                env.pop("GROK_ACTIVITY_FILE", None)
                subprocess.run(
                    [sys.executable, "website/build.py"],
                    cwd=root,
                    env=env,
                    check=True,
                    capture_output=True,
                )

    def test_corrupt_cache_and_atomic_failure(self):
        with tempfile.TemporaryDirectory() as d:
            cache = Path(d) / "cache.json"
            for content in [
                "{",
                "[]",
                '{"state":"live","owner":"old"}',
                '{"state":"live","owner":"old","data":false}',
            ]:
                cache.write_text(content)
                result = refresh(
                    "old", cache, lambda *a: (_ for _ in ()).throw(URLError("no"))
                )
                self.assertEqual(result["state"], "unavailable")
                self.assertEqual(result, json.loads(cache.read_text()))
            prior = cache.read_bytes()
            with patch("activity.os.replace", side_effect=OSError("replace failed")):
                with self.assertRaises(OSError):
                    refresh("old", cache, lambda *a: [])
            self.assertEqual(cache.read_bytes(), prior)
            self.assertEqual(list(Path(d).glob(".activity-*")), [])

    def test_success_throttle_and_cached_retry(self):
        now = datetime(2026, 10, 4, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as d:
            cache = Path(d) / "new" / "cache.json"
            calls = []

            def success(*args):
                calls.append(1)
                return []

            first = refresh("owner", cache, success, now)
            self.assertEqual(first, json.loads(cache.read_text()))
            self.assertEqual(refresh("owner", cache, success, now), first)
            self.assertEqual(len(calls), 1)
            saved = {**first, "state": "cached"}
            cache.write_text(json.dumps(saved))
            self.assertEqual(refresh("owner", cache, success, now)["state"], "live")
            self.assertEqual(len(calls), 2)

    def test_build_stale_live_fixture_and_corrupt_input(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as d:
            cache = Path(d) / "cache.json"
            data = dict(
                aggregate_stars=41,
                open_issues=2,
                contributors=3,
                active_contributors=1,
                releases=[
                    dict(
                        repository="fixture",
                        name="<script>fixture</script>",
                        date="synthetic",
                    )
                ],
            )
            cases = [
                (
                    dict(
                        state="live",
                        owner="old",
                        last_successful_refresh="2020-01-01T00:00:00+00:00",
                        data=data,
                    ),
                    "CACHED",
                ),
                (dict(state="fixture", data=data), "FIXTURE"),
                (
                    dict(
                        state="live",
                        owner="old",
                        last_successful_refresh="2999-01-01T00:00:00+00:00",
                        data=data,
                    ),
                    "UNAVAILABLE",
                ),
                (None, "UNAVAILABLE"),
            ]
            try:
                for record, state in cases:
                    cache.write_text(
                        json.dumps(record) if record is not None else "{broken"
                    )
                    subprocess.run(
                        [sys.executable, "website/build.py"],
                        cwd=root,
                        env={**os.environ, "GROK_ACTIVITY_FILE": str(cache)},
                        check=True,
                        capture_output=True,
                    )
                    html = (root / "website/dist/activity.html").read_text()
                    self.assertIn(state, html)
                    self.assertNotIn("LIVE —", html)
                    self.assertNotIn("<script>fixture", html)
                    if state == "CACHED":
                        self.assertIn("2020-01-01", html)
                    if state == "UNAVAILABLE":
                        self.assertNotIn(
                            "Aggregate stars (sum, not unique people): 41", html
                        )
            finally:
                env = dict(os.environ)
                env.pop("GROK_ACTIVITY_FILE", None)
                subprocess.run(
                    [sys.executable, "website/build.py"],
                    cwd=root,
                    env=env,
                    check=True,
                    capture_output=True,
                )

    def test_snapshot_wording_before_and_after_expiry_and_failed_refresh(self):
        root = Path(__file__).resolve().parents[1]
        now = datetime.now(timezone.utc)
        data = dict(
            aggregate_stars=1,
            open_issues=2,
            contributors=3,
            active_contributors=1,
            releases=[],
        )

        def record(minutes_old, **extra):
            stamp = (now - timedelta(minutes=minutes_old)).isoformat()
            return dict(
                owner="adidshaft", last_successful_refresh=stamp, data=data, **extra
            )

        cases = [
            # Just before the one-hour expiry: a dated snapshot, never "live".
            (record(59, state="live"), "SNAPSHOT —"),
            # Just after expiry, with no new refresh: cached.
            (record(61, state="live"), "CACHED —"),
            # A failed refresh keeps the old data as cached.
            (
                record(
                    5,
                    state="cached",
                    refresh_error="Refresh failed; timestamped cached data",
                ),
                "CACHED —",
            ),
        ]
        with tempfile.TemporaryDirectory() as d:
            cache = Path(d) / "cache.json"
            try:
                for item, label in cases:
                    cache.write_text(json.dumps(item))
                    subprocess.run(
                        [sys.executable, "website/build.py"],
                        cwd=root,
                        env={**os.environ, "GROK_ACTIVITY_FILE": str(cache)},
                        check=True,
                        capture_output=True,
                    )
                    html = (root / "website/dist/activity.html").read_text()
                    self.assertIn(label, html)
                    self.assertNotIn("LIVE", html)
                    stamp = datetime.fromisoformat(item["last_successful_refresh"])
                    self.assertIn("Fetched at: <time datetime=", html)
                    self.assertIn(stamp.strftime("%Y-%m-%d %H:%M UTC"), html)
                    self.assertIn("This is a snapshot, not a live feed.", html)
                    self.assertIn("once a day at 06:17 UTC", html)
            finally:
                env = dict(os.environ)
                env.pop("GROK_ACTIVITY_FILE", None)
                subprocess.run(
                    [sys.executable, "website/build.py"],
                    cwd=root,
                    env=env,
                    check=True,
                    capture_output=True,
                )

    def test_invalid_owner(self):
        with self.assertRaises(ValueError):
            refresh("../private", Path("/tmp/unused"))


if __name__ == "__main__":
    unittest.main()
