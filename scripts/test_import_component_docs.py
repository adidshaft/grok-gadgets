"""Check that help and invalid arguments cannot import or delete snapshots."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("import-component-docs.py")


class ImportArgumentsTests(unittest.TestCase):
    def test_arguments_leave_snapshots_unchanged(self):
        for argument, expected_code in [("--help", 0), ("--invalid", 2)]:
            with self.subTest(argument=argument), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                scripts = root / "scripts"
                scripts.mkdir()
                shutil.copyfile(SCRIPT, scripts / SCRIPT.name)
                docs = root / "docs/components"
                docs.mkdir(parents=True)
                snapshot = docs / "retained.md"
                snapshot.write_text("Keep this snapshot.\n")
                compatibility = root / "compatibility"
                compatibility.mkdir()
                manifest = compatibility / "documentation-sources.json"
                manifest.write_text('[{"snapshot": "docs/components/retained.md"}]\n')
                before = {
                    str(p.relative_to(root)): p.read_bytes()
                    for p in root.rglob("*")
                    if p.is_file()
                }
                result = subprocess.run(
                    [sys.executable, str(scripts / SCRIPT.name), argument],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, expected_code, result.stderr)
                self.assertIn("usage:", result.stdout + result.stderr)
                after = {
                    str(p.relative_to(root)): p.read_bytes()
                    for p in root.rglob("*")
                    if p.is_file()
                }
                self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
