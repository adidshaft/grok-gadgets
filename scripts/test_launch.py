"""Launch safety and exact-pin regressions; no network or publication."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_"), ROOT / "scripts" / (name + ".py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LaunchTests(unittest.TestCase):
    def test_candidate_sha_is_bounded_and_other_pins_are_retained(self):
        pins = load("ci-component-pins")
        baseline = pins.selected()
        chosen = pins.selected("grok-gadgets-gateway", "a" * 40)
        self.assertEqual(chosen["gateway"], "a" * 40)
        self.assertEqual(
            {k: v for k, v in chosen.items() if k != "gateway"},
            {k: v for k, v in baseline.items() if k != "gateway"},
        )
        for repo, sha in [
            ("other/repo", "a" * 40),
            ("grok-gadgets-gateway", "main"),
            ("grok-gadgets-gateway", "$(printenv)"),
            ("", "a" * 40),
            ("grok-gadgets-gateway", ""),
        ]:
            with self.subTest(repo=repo, sha=sha), self.assertRaises(ValueError):
                pins.selected(repo, sha)

    def test_branch_sources_resolve_exact_refs_and_reject_missing_or_bad_heads(self):
        pins = load("ci-component-pins")
        for source in ("main", "dev"):
            with (
                self.subTest(source=source),
                patch.object(
                    pins.subprocess,
                    "run",
                    return_value=Mock(
                        stdout="a" * 40 + "\trefs/heads/" + source + "\n"
                    ),
                ) as remote,
            ):
                self.assertEqual(set(pins.selected(source=source).values()), {"a" * 40})
                self.assertEqual(remote.call_count, len(pins.REPOSITORIES))
                for call in remote.call_args_list:
                    self.assertEqual(call.args[0][-1], "refs/heads/" + source)
                    self.assertTrue(call.kwargs["check"])
            for output in ("", "invalid\trefs/heads/" + source + "\n"):
                with (
                    self.subTest(source=source, output=output),
                    patch.object(
                        pins.subprocess, "run", return_value=Mock(stdout=output)
                    ),
                    self.assertRaisesRegex(ValueError, "exact forty-character"),
                ):
                    pins.selected(source=source)
        with self.assertRaisesRegex(ValueError, "Source must"):
            pins.selected(source="feature")

    def test_integration_selects_dev_for_schedule_and_dev_events_only(self):
        workflow = yaml.load(
            (ROOT / ".github/workflows/integration.yml").read_text(),
            Loader=yaml.BaseLoader,
        )
        self.assertEqual(
            workflow["on"]["workflow_dispatch"]["inputs"]["components"]["options"],
            ["main", "dev", "pinned"],
        )
        steps = workflow["jobs"]["integration"]["steps"]
        source = next(step for step in steps if step.get("id") == "pins")["env"][
            "COMPONENTS"
        ]
        # Exercise the Actions expression for each release/integration event.
        expression = source.removeprefix("${{ ").removesuffix(" }}")
        expression = expression.replace("||", "or").replace("&&", "and")
        cases = [
            ("schedule", "", "refs/heads/dev", "", "dev"),
            ("schedule", "", "refs/heads/main", "", "dev"),
            ("push", "", "refs/heads/dev", "", "dev"),
            ("push", "", "refs/heads/main", "", "main"),
            ("pull_request", "dev", "refs/pull/1/merge", "", "dev"),
            ("pull_request", "main", "refs/pull/2/merge", "", "main"),
            ("workflow_dispatch", "", "refs/heads/dev", "main", "main"),
            ("workflow_dispatch", "", "refs/heads/main", "dev", "dev"),
            ("workflow_dispatch", "", "refs/heads/main", "pinned", "pinned"),
        ]
        for event, base, ref, manual, expected in cases:
            with self.subTest(event=event, base=base, ref=ref, manual=manual):
                values = {
                    "github.event_name": repr(event),
                    "github.base_ref": repr(base),
                    "github.ref": repr(ref),
                    "inputs.components": repr(manual),
                }
                chosen = expression
                for name, value in values.items():
                    chosen = chosen.replace(name, value)
                self.assertEqual(eval(chosen, {"__builtins__": {}}), expected)

    def test_workflows_are_readonly_except_manual_deployment_and_use_verified_pins(
        self,
    ):
        approved = {
            item["repository"]: item["sha"]
            for item in json.loads((ROOT / "publication/action-pins.json").read_text())[
                "actions"
            ]
        }
        for file in (ROOT / ".github/workflows").glob("*.yml"):
            workflow = yaml.load(file.read_text(), Loader=yaml.BaseLoader)
            self.assertEqual(workflow["permissions"], {"contents": "read"})
            self.assertNotIn("pull_request_target", workflow["on"])
            # Only the deploy and nightly integration run on a schedule.
            if file.name not in {"pages.yml", "integration.yml"}:
                self.assertNotIn("schedule", workflow["on"])
            for name, job in workflow["jobs"].items():
                self.assertIn("timeout-minutes", job)
                for step in job["steps"]:
                    if "uses" not in step:
                        continue
                    repo, sha = step["uses"].split("@")
                    self.assertRegex(sha, r"^[a-f0-9]{40}$")
                    self.assertEqual(sha, approved[repo])
                    if repo == "actions/checkout":
                        self.assertEqual(step["with"]["persist-credentials"], "false")
                self.assertNotIn("pages", job.get("permissions", {}))
                self.assertNotIn("id-token", job.get("permissions", {}))
        pages = yaml.load(
            (ROOT / ".github/workflows/pages.yml").read_text(), Loader=yaml.BaseLoader
        )
        self.assertEqual(
            set(pages["on"]), {"workflow_run", "schedule", "workflow_dispatch"}
        )
        self.assertEqual(
            pages["on"]["workflow_run"]["workflows"], ["Integrated acceptance"]
        )
        self.assertEqual(pages["on"]["schedule"][0]["cron"], "17 6 * * *")
        self.assertEqual(pages["jobs"]["deploy"]["needs"], "build")
        self.assertIn("head_branch == 'main'", pages["jobs"]["build"]["if"])
        self.assertIn("conclusion == 'success'", pages["jobs"]["build"]["if"])
        self.assertIn("Hub checks", str(pages["jobs"]["build"]["steps"]))
        self.assertIn("Integrated acceptance", str(pages["jobs"]["build"]["steps"]))
        self.assertIn(
            "scripts/refresh-github-snapshot.py", str(pages["jobs"]["build"]["steps"])
        )
        self.assertIn(
            "website/activity.py --live", str(pages["jobs"]["build"]["steps"])
        )
        self.assertIn(
            "scripts/check-pages-prefix.py", str(pages["jobs"]["build"]["steps"])
        )
        self.assertIn("https://grokgadgets.org/", str(pages["jobs"]["build"]["steps"]))
        self.assertEqual(
            pages["jobs"]["deploy"]["permissions"],
            {"contents": "read", "deployments": "write"},
        )
        self.assertEqual(
            pages["jobs"]["deploy"]["environment"]["name"],
            "cloudflare-pages-production",
        )
        self.assertIn("CLOUDFLARE_API_TOKEN", str(pages["jobs"]["deploy"]))
        self.assertNotIn("CLOUDFLARE_API_TOKEN", str(pages["jobs"]["build"]))
        self.assertIn(
            "pages deploy website/dist --project-name=grok-gadgets --branch=main",
            str(pages["jobs"]["deploy"]),
        )

    def test_rules_preserve_history_and_solo_maintainer_can_merge(self):
        repositories = json.loads((ROOT / "publication/repositories.json").read_text())
        for file in (ROOT / "publication/rulesets").glob("*.json"):
            rules = json.loads(file.read_text())
            self.assertIn(rules["enforcement"], {"disabled", "active"})
            if rules["enforcement"] == "active":
                self.assertTrue(repositories["activated"])
            self.assertEqual(rules["bypass_actors"], [])
            kinds = {
                rule["type"]: rule.get("parameters", {}) for rule in rules["rules"]
            }
            self.assertTrue(
                {
                    "deletion",
                    "non_fast_forward",
                    "pull_request",
                    "required_status_checks",
                }
                <= set(kinds)
            )
            self.assertNotIn("required_linear_history", kinds)
            self.assertEqual(
                kinds["pull_request"]["required_approving_review_count"], 0
            )
            self.assertTrue(kinds["pull_request"]["required_review_thread_resolution"])
            self.assertEqual(
                kinds["pull_request"]["allowed_merge_methods"], ["merge", "rebase"]
            )
            self.assertFalse(
                kinds["pull_request"]["require_extra_approval_for_unattributed_changes"]
            )
            self.assertTrue(
                kinds["required_status_checks"]["strict_required_status_checks_policy"]
            )
            for check in kinds["required_status_checks"]["required_status_checks"]:
                self.assertEqual(check["integration_id"], 15368)

    def test_project_prefix_rejects_root_and_deep_missing_assets(self):
        checker = load("check-pages-prefix")
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "index.html").write_text('<a href="/style.css">bad root</a>')
            (root / "style.css").write_text("")
            with self.assertRaisesRegex(ValueError, "prefix"):
                checker.check(root, base="https://adidshaft.github.io/grok-gadgets/")
            (root / "index.html").write_text("")
            (root / "404.html").write_text('<a href="another.html">deep link</a>')
            with self.assertRaisesRegex(ValueError, "deep link"):
                checker.check(root, base="https://adidshaft.github.io/grok-gadgets/")

    def test_extensionless_page_urls_resolve_like_cloudflare_pages(self):
        checker = load("check-pages-prefix")
        site = "https://grokgadgets.org/"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "index.html").write_text(f'<a href="{site}status">status</a>')
            with self.assertRaisesRegex(ValueError, "deep link"):
                checker.check(root, base=site)
            (root / "status.html").write_text("")
            # The page now exists; the check moves on to the kit download manifest.
            with self.assertRaises(FileNotFoundError):
                checker.check(root, base=site)
