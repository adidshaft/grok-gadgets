"""Publication integrity regressions with temporary repositories; no final candidate writes."""

import hashlib
import importlib.util
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import zipfile


def load(name):
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_"), Path(__file__).with_name(name + ".py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


packager = load("package-local")
verifier = load("verify-publication")


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.root = self.workspace / "grok-gadgets"
        self.sources = {}
        for name in packager.REPOSITORIES:
            repo = self.workspace / name
            repo.mkdir()
            packager.git(repo, "init", "-b", "main")
            packager.git(repo, "config", "user.name", "Local test")
            packager.git(repo, "config", "user.email", "local-test@example.invalid")
            for filename in ("README.md", "LICENSE"):
                (repo / filename).write_text("Local fixture\n")
            if name in packager.PYTHON_REPOSITORIES:
                (repo / "src").mkdir()
                (repo / "src/fixture.py").write_text("VALUE = 1\n")
                (repo / "pyproject.toml").write_text(
                    '[project]\nname="fixture"\nversion="0.1"\n'
                )
            if name == "grok-gadgets":
                (repo / ".gitignore").write_text("artifacts/\nwebsite/dist/\n")
                (repo / "website").mkdir()
                (repo / "website/build.py").write_text(
                    'from pathlib import Path\np=Path("website/dist");p.mkdir(exist_ok=True)\n'
                    '(p/"index.html").write_text("<h1>fixture</h1>")\n'
                )
            elif name == "grok-gadgets-esp32-sdk":
                (repo / ".gitignore").write_text("artifacts/\n")
                (repo / "device.cpp").write_text("// fixture runtime\n")
            packager.git(repo, "add", ".")
            packager.git(repo, "commit", "-m", "fixture")
            self.sources[name] = packager.git(repo, "rev-parse", "HEAD")
        self.firmware_repo = self.workspace / "grok-gadgets-esp32-sdk"
        directory = self.firmware_repo / "artifacts/c124-usb"
        directory.mkdir(parents=True)
        files = {}
        for name in (
            "firmware.bin",
            "firmware.elf",
            "bootloader.bin",
            "partitions.bin",
        ):
            path = directory / name
            path.write_bytes(b"fixture firmware: " + name.encode())
            files[name] = {
                "bytes": path.stat().st_size,
                "sha256": packager.sha256(path),
            }
        self.provenance = {
            "source_commit": self.sources[self.firmware_repo.name],
            "source_tree_clean": True,
            "toolchain": {"fixture": "1"},
            "built_at_utc": "2026-10-04T00:00:00Z",
            "build_command": "fixture",
            "files": files,
        }
        packager.write_json(directory / "manifest.json", self.provenance)

    def fake_python_build(self, repo, source, source_archive, out, records, validator):
        payloads = verifier.source_payloads(repo, source)
        wheel = out / (repo.name + "-0.1-py3-none-any.whl")
        with zipfile.ZipFile(wheel, "w") as archive:
            archive.writestr("fixture.py", payloads["src/fixture.py"])
        with tempfile.TemporaryDirectory() as temporary:
            temporary = Path(temporary)
            with tarfile.open(source_archive) as archive:
                archive.extractall(temporary, filter="data")
            sdist = out / (repo.name + "-0.1.tar.gz")
            with tarfile.open(sdist, "w:gz") as archive:
                archive.add(temporary / repo.name, arcname="fixture-0.1")
        for package in (wheel, sdist):
            validator.validate_python_package(package, repo, source)
            packager.add_record(
                records,
                package,
                repository=repo.name,
                kind="python_package",
                source_commit=source,
            )
        provenance = {
            "source_commit": source,
            "source_dirty": False,
            "environment": {"fixture": True},
            "build_command": "fixture archive build",
            "build_configuration_sha256": hashlib.sha256(
                payloads["pyproject.toml"]
            ).hexdigest(),
            "artifacts": {p.name: packager.sha256(p) for p in (wheel, sdist)},
        }
        path = out / (repo.name + "-build-provenance.json")
        packager.write_json(path, provenance)
        packager.add_record(
            records,
            path,
            repository=repo.name,
            kind="build_provenance",
            source_commit=source,
        )

    def prepare(self):
        with patch.object(packager, "build_python", self.fake_python_build):
            return packager.prepare(self.root)

    def rehash(self, directory):
        # Update outer hashes intentionally to challenge inner source/provenance verification.
        manifest = json.loads((directory / "manifest.json").read_text())
        for record in manifest["artifacts"]:
            path = directory / record["file"]
            record.update(sha256=packager.sha256(path), bytes=path.stat().st_size)
        packager.write_json(directory / "manifest.json", manifest)
        names = [record["file"] for record in manifest["artifacts"]] + ["manifest.json"]
        (directory / "SHA256SUMS").write_text(
            "".join(
                packager.sha256(directory / name) + "  " + name + "\n"
                for name in sorted(names)
            )
        )

    def test_candidate_verifies_and_preserves_history(self):
        output = self.root / "artifacts/publication"
        output.mkdir(parents=True)
        (output / "old-candidate.bin").write_bytes(b"preserved")
        first = self.prepare()
        first_manifest = (first / "manifest.json").read_bytes()
        second = self.prepare()
        self.assertNotEqual(first, second)
        self.assertEqual((first / "manifest.json").read_bytes(), first_manifest)
        self.assertEqual((output / "old-candidate.bin").read_bytes(), b"preserved")
        self.assertEqual(
            json.loads((output / "latest.json").read_text())["directory"], second.name
        )
        self.assertEqual(
            verifier.verify_candidate(second, self.root, require_current=True), 25
        )
        self.assertEqual(len(list(second.glob("*.bundle"))), 5)

    def test_artifact_tampering_fails_hash_check(self):
        candidate = self.prepare()
        next(candidate.glob("*.whl")).write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            verifier.verify_candidate(candidate, self.root)

    def test_malformed_python_provenance_fails_even_when_rehashed(self):
        candidate = self.prepare()
        path = next(candidate.glob("*-build-provenance.json"))
        provenance = json.loads(path.read_text())
        provenance["source_dirty"] = True
        packager.write_json(path, provenance)
        self.rehash(candidate)
        with self.assertRaisesRegex(ValueError, "build provenance source mismatch"):
            verifier.verify_candidate(candidate, self.root)

    def test_wrong_wheel_source_fails_even_when_rehashed(self):
        candidate = self.prepare()
        path = next(candidate.glob("*.whl"))
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("fixture.py", "VALUE = 'obsolete'\n")
        self.rehash(candidate)
        with self.assertRaisesRegex(ValueError, "Wheel source mismatch"):
            verifier.verify_candidate(candidate, self.root)

    def test_firmware_hash_failure_does_not_replace_candidate(self):
        first = self.prepare()
        pointer = self.root / "artifacts/publication/latest.json"
        before = pointer.read_bytes()
        (self.firmware_repo / "artifacts/c124-usb/firmware.bin").write_bytes(b"stale")
        with self.assertRaisesRegex(
            ValueError, "Firmware provenance hash/size mismatch"
        ):
            self.prepare()
        self.assertEqual(pointer.read_bytes(), before)
        self.assertTrue(first.is_dir())
        self.assertFalse(list(pointer.parent.glob(".candidate-*")))

    def test_firmware_runtime_changes_require_rebuild(self):
        (self.firmware_repo / "device.cpp").write_text("// changed runtime\n")
        packager.git(self.firmware_repo, "add", "device.cpp")
        packager.git(self.firmware_repo, "commit", "-m", "changed runtime")
        with self.assertRaisesRegex(ValueError, "runtime/toolchain source changed"):
            verifier.validate_firmware_provenance(
                self.provenance,
                self.firmware_repo,
                packager.git(self.firmware_repo, "rev-parse", "HEAD"),
            )

    def test_firmware_evidence_changes_allow_exact_ancestor_build(self):
        (self.firmware_repo / "planning").mkdir()
        (self.firmware_repo / "planning/issues.json").write_text("[]\n")
        packager.git(self.firmware_repo, "add", "planning/issues.json")
        packager.git(self.firmware_repo, "commit", "-m", "evidence only")
        self.assertEqual(
            verifier.validate_firmware_provenance(
                self.provenance,
                self.firmware_repo,
                packager.git(self.firmware_repo, "rev-parse", "HEAD"),
            ),
            ["planning/issues.json"],
        )

    def test_malformed_firmware_provenance_fails(self):
        with self.assertRaisesRegex(ValueError, "full Git commit"):
            verifier.validate_firmware_provenance(
                {**self.provenance, "source_commit": "missing"},
                self.firmware_repo,
                self.sources[self.firmware_repo.name],
            )
        with self.assertRaisesRegex(ValueError, "committed and clean"):
            verifier.validate_firmware_provenance(
                {**self.provenance, "source_tree_clean": "true"},
                self.firmware_repo,
                self.sources[self.firmware_repo.name],
            )

    def test_dirty_source_rejected_brand_assets_preserved(self):
        (self.root / "assets").mkdir()
        (self.root / "assets/private.bin").write_bytes(b"user work")
        self.assertEqual(len(packager.inspect_sources(self.root)), 5)
        (self.root / "README.md").write_text("uncommitted\n")
        with self.assertRaisesRegex(ValueError, "commit intended source changes"):
            packager.inspect_sources(self.root)

    def test_wrong_source_archive_rejected_even_when_rehashed(self):
        candidate = self.prepare()
        manifest = json.loads((candidate / "manifest.json").read_text())
        sources = [
            record
            for record in manifest["artifacts"]
            if record["repository"] == "grok-gadgets"
            and record["kind"] == "source_archive"
        ]
        self.assertEqual(len(sources), 1)
        archive = candidate / sources[0]["file"]
        with tarfile.open(archive, "w:gz"):
            pass
        self.rehash(candidate)
        with self.assertRaisesRegex(ValueError, "exact source commit"):
            verifier.verify_candidate(candidate, self.root)

    def test_missing_bundle_rejected(self):
        candidate = self.prepare()
        next(candidate.glob("*.bundle")).unlink()
        with self.assertRaisesRegex(ValueError, "missing or unlisted"):
            verifier.verify_candidate(candidate, self.root)


if __name__ == "__main__":
    unittest.main()
