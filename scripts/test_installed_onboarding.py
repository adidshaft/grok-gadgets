"""Offline installed-wheel acceptance invariants and bounded failure diagnostics."""

import importlib.util
import io
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "check_installed_onboarding",
    Path(__file__).with_name("check-installed-onboarding.py"),
)
onboarding = importlib.util.module_from_spec(spec)
spec.loader.exec_module(onboarding)


class InstalledOnboardingTests(unittest.TestCase):
    def test_failure_retains_dependency_diagnostic_without_private_details_or_retry(
        self,
    ):
        details = (
            "unrelated output\n" * 1000
            + "Registry https://user:private-fixture@example.invalid/simple?key=private-query\n"
            + "Authorization: Bearer private-authorization\n"
            + "api_key=private-api-key\n"
            + str(Path.home())
            + "/private-cache\n"
            + "jsonschema==4.26.0 was not found in the cache"
        )
        failure = subprocess.CalledProcessError(
            1, ["uv", "pip", "install"], output="private stdout", stderr=details
        )
        with patch.object(onboarding.subprocess, "run", side_effect=failure) as run:
            with self.assertRaisesRegex(
                RuntimeError, "Offline runtime failed"
            ) as caught:
                onboarding.run_checked(["uv"], step="Offline runtime", env={})
        message = str(caught.exception)
        self.assertIn("jsonschema==4.26.0 was not found in the cache", message)
        self.assertIn("[stderr truncated]", message)
        self.assertLessEqual(len(message), onboarding.STDERR_LIMIT + 50)
        for value in (
            "private-fixture",
            "private-query",
            "private-authorization",
            "private-api-key",
            "private stdout",
            str(Path.home()),
        ):
            self.assertNotIn(value, message)
        run.assert_called_once()

    def test_timeout_reports_redacted_bytes_and_stops(self):
        failure = subprocess.TimeoutExpired(
            ["uv"], 60, stderr=b"api_key=private-api-key\nRuntime installation stalled"
        )
        with patch.object(onboarding.subprocess, "run", side_effect=failure) as run:
            with self.assertRaisesRegex(RuntimeError, "timed out") as caught:
                onboarding.run_checked(["uv"], step="Offline runtime", env={})
        self.assertIn("Runtime installation stalled", str(caught.exception))
        self.assertNotIn("private-api-key", str(caught.exception))
        run.assert_called_once()

    def test_acceptance_uses_frozen_offline_pins_and_isolated_wheel_installs(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            root = workspace / "grok-gadgets"
            root.mkdir()
            for repository in ("grok-gadgets-linux-sdk", "grok-gadgets-gateway"):
                dist = workspace / repository / "dist"
                dist.mkdir(parents=True)
                (dist / (repository + ".whl")).write_bytes(b"fixture wheel")
            commands = []

            def run(command, **kwargs):
                commands.append(command)
                self.assertNotIn("PYTHONPATH", kwargs["env"])
                self.assertNotIn("PYTHONHOME", kwargs["env"])
                if command[:2] == ["uv", "export"]:
                    self.assertIn("--offline", command)
                    self.assertIn("--frozen", command)
                    self.assertIn("--no-dev", command)
                    self.assertIn("--no-emit-project", command)
                    output = Path(command[command.index("--output-file") + 1])
                    output.write_text("jsonschema==4.26.0\n")
                if command[:3] == ["uv", "pip", "install"]:
                    self.assertIn("--offline", command)
                    self.assertIn("--strict", command)
                    requirements = Path(command[command.index("--requirements") + 1])
                    self.assertEqual(requirements.read_text(), "jsonschema==4.26.0\n")
                    self.assertEqual(
                        len([value for value in command if value.endswith(".whl")]), 2
                    )
                    self.assertNotIn("--editable", command)
                return SimpleNamespace(stdout="fixture acceptance")

            with (
                patch.dict(
                    os.environ, PYTHONPATH="private-source", PYTHONHOME="private-python"
                ),
                patch.object(onboarding.subprocess, "run", side_effect=run),
                patch("sys.stdout", new_callable=io.StringIO),
            ):
                onboarding.check_installed(root)
            self.assertEqual(len(commands), 5)
            checks = [command for command in commands if "-I" in command]
            self.assertEqual(len(checks), 2)
            self.assertEqual(sum("--dataclass" in command for command in checks), 1)
            self.assertTrue(all("venv/bin/python" in command[0] for command in checks))


if __name__ == "__main__":
    unittest.main()
