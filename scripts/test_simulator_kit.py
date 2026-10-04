"""Inspect the actual downloadable archive and its readable verifier."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[1]


class KitTests(unittest.TestCase):
    @contextmanager
    def mocked_source(self, module, commit):
        # Exercise clean-source rebuild branches in a standalone hub checkout too.
        with (
            patch.object(module, "GATEWAY", ROOT),
            patch.object(
                module,
                "run",
                side_effect=lambda args, **kwargs: commit
                if args[1] == "rev-parse"
                else "",
            ),
        ):
            yield

    def builder(self):
        spec = importlib.util.spec_from_file_location(
            "kit_builder", ROOT / "scripts/build-simulator-kit.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_freshness_and_refresh_failure_gate(self):
        module = self.builder()
        output = ROOT / "website/downloads"
        record = module.ensure_current(output, rebuild=False)
        with self.assertRaisesRegex(ValueError, "source changed"):
            module.verify_download(output, "0" * 40)
        with tempfile.TemporaryDirectory() as temporary:
            import shutil

            scratch = Path(temporary)
            for path in output.iterdir():
                shutil.copy(path, scratch / path.name)
            changed = {**record, "build_inputs": {}}
            (scratch / "simulator-kit-manifest.json").write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError, "unavailable"):
                module.ensure_current(scratch, rebuild=False)
        with patch.object(module, "GATEWAY", ROOT / "absent-gateway"):
            self.assertEqual(module.ensure_current(output, rebuild=False), record)
        with tempfile.TemporaryDirectory() as temporary:
            scratch = Path(temporary)
            (scratch / "simulator-kit-manifest.json").write_text("null")
            with self.assertRaisesRegex(ValueError, "Malformed"):
                module.verify_download(scratch)
            with (
                self.mocked_source(module, record["gateway_commit"]),
                patch.object(module, "build") as build,
                patch.object(
                    module,
                    "verify_download",
                    side_effect=[ValueError("Malformed"), record],
                ),
            ):
                self.assertEqual(module.ensure_current(scratch), record)
                build.assert_called_once_with(scratch)
        with (
            self.mocked_source(module, record["gateway_commit"]),
            patch.object(
                module, "verify_download", side_effect=[ValueError("stale"), record]
            ),
            patch.object(module, "build") as build,
        ):
            self.assertEqual(module.ensure_current(output), record)
            build.assert_called_once_with(output)
        with (
            self.mocked_source(module, record["gateway_commit"]),
            patch.object(module, "verify_download", side_effect=ValueError("stale")),
            patch.object(module, "build", side_effect=RuntimeError("tests failed")),
        ):
            with self.assertRaisesRegex(RuntimeError, "tests failed"):
                module.ensure_current(output)
        with (
            patch.object(module, "GATEWAY", ROOT),
            patch.object(module, "run", return_value=" M src/change.py"),
        ):
            with self.assertRaisesRegex(ValueError, "uncommitted"):
                module.ensure_current(output)

    def test_clean_source_advancing_during_verification_is_rejected(self):
        module = self.builder()
        commit = "a" * 40
        record = {"gateway_commit": commit}
        with (
            patch.object(module, "GATEWAY", ROOT),
            patch.object(module, "run", side_effect=["", commit, "", "b" * 40]),
            patch.object(module, "verify_download", return_value=record),
        ):
            with self.assertRaisesRegex(ValueError, "changed during verification"):
                module.ensure_current(ROOT / "website/downloads", rebuild=False)
        with (
            patch.object(module, "GATEWAY", ROOT),
            patch.object(module, "inputs", side_effect=[{}, {"changed": "digest"}]),
            patch.object(module, "run", side_effect=["", commit]),
            patch.object(module, "verify_download", return_value=record),
        ):
            with self.assertRaisesRegex(ValueError, "inputs changed during"):
                module.ensure_current(ROOT / "website/downloads", rebuild=False)

    def test_download_integrity_contents_and_tamper_detection(self):
        directory = ROOT / "website/downloads"
        record = json.loads((directory / "simulator-kit-manifest.json").read_text())
        archive = directory / record["archive"]
        self.assertEqual(
            hashlib.sha256(archive.read_bytes()).hexdigest(), record["archive_sha256"]
        )
        with tempfile.TemporaryDirectory() as temporary:
            with zipfile.ZipFile(archive) as bundle:
                for name in bundle.namelist():
                    self.assertTrue(name.startswith("grok-gadgets-simulator-kit/"))
                    self.assertNotIn("..", Path(name).parts)
                    self.assertFalse(
                        any(
                            part in name
                            for part in [".venv/", ".git/", "artifacts/", ".env"]
                        )
                    )
                bundle.extractall(temporary)
            kit = Path(temporary) / "grok-gadgets-simulator-kit"
            result = subprocess.run(
                [sys.executable, str(kit / "install.py")],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Nothing installed or started", result.stdout)
            valid_manifest = json.loads((kit / "manifest.json").read_text())
            for patch in [
                {"format_version": 999},
                {"gateway_commit": "not-a-commit"},
                {"files": []},
                {
                    "files": [
                        r
                        for r in valid_manifest["files"]
                        if r["file"] != "requirements.txt"
                    ]
                },
                {"files": valid_manifest["files"] + [valid_manifest["files"][0]]},
            ]:
                (kit / "manifest.json").write_text(
                    json.dumps({**valid_manifest, **patch})
                )
                invalid = subprocess.run(
                    [sys.executable, str(kit / "install.py")],
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(invalid.returncode, 0)
                self.assertFalse((kit / ".venv").exists())
            (kit / "manifest.json").write_text(json.dumps(valid_manifest))
            self.assertFalse((kit / ".venv").exists())
            for name in [
                "LICENSE",
                "NOTICE",
                "source.tar",
                "README.md",
                "requirements.txt",
                "simulator-config.schema.json",
                "try_simulator.py",
            ]:
                self.assertTrue((kit / name).is_file(), name)
            self.assertNotIn("/Users/", (kit / "requirements.txt").read_text())
            self.assertIn("--hash=sha256:", (kit / "requirements.txt").read_text())
            manifest = json.loads((kit / "manifest.json").read_text())
            self.assertEqual(manifest["gateway_commit"], record["gateway_commit"])
            (kit / "requirements.txt").write_text("tampered")
            failure = subprocess.run(
                [sys.executable, str(kit / "install.py")],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(failure.returncode, 0)
            self.assertIn("Hash mismatch", failure.stderr)

    def test_browser_export_into_extracted_kit_preserves_default_integrity(self):
        # Run the same export function used by the website, not a hand-renamed fixture.
        export = json.loads(
            subprocess.check_output(
                [
                    "node",
                    "-e",
                    "const s=require('./website/simulator.js'); console.log(JSON.stringify(s.exportConfiguration({...s.defaults, device_id:'studio-light', display_name:'Studio light', initial_rgb:{r:26,g:51,b:128,on:true}, response_delay_ms:250, start_disconnected:true})));",
                ],
                cwd=ROOT,
                text=True,
            )
        )
        with tempfile.TemporaryDirectory() as temporary:
            with zipfile.ZipFile(
                ROOT / "website/downloads/grok-gadgets-simulator-kit.zip"
            ) as bundle:
                bundle.extractall(temporary)
            kit = Path(temporary) / "grok-gadgets-simulator-kit"
            default = kit / "simulator-config.json"
            original = default.read_bytes()
            (kit / export["filename"]).write_text(export["content"])
            result = subprocess.run(
                [
                    sys.executable,
                    str(kit / "install.py"),
                    "--config",
                    str(kit / export["filename"]),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(default.read_bytes(), original)
            self.assertEqual(export["filename"], "my-light.json")
            config = json.loads((kit / "my-light.json").read_text())
            self.assertEqual(config["device_id"], "studio-light")
            self.assertTrue(config["start_disconnected"])
            # Protect the integrity boundary: the old overwrite must still fail.
            default.write_text(export["content"])
            rejected = subprocess.run(
                [sys.executable, str(kit / "install.py")],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("Hash mismatch: simulator-config.json", rejected.stderr)

    def test_verifier_rejects_traversal_and_symlink(self):
        spec = importlib.util.spec_from_file_location(
            "kit_install", ROOT / "scripts/simulator-kit/install.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            kit = Path(temporary)
            manifest = json.loads(
                (ROOT / "website/downloads/simulator-kit-manifest.json").read_text()
            )
            item = manifest["files"][0]
            item["file"] = "../outside"
            (kit / "manifest.json").write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "Unsafe"):
                module.verify(kit)
            (kit / "target").write_text("data")
            (kit / "alias").symlink_to(kit / "target")
            item["file"] = "alias"
            (kit / "manifest.json").write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "unsafe"):
                module.verify(kit)


if __name__ == "__main__":
    unittest.main()
