"""Include donation interaction regressions in the standard website checks."""

from pathlib import Path
import subprocess
import unittest


class DonationTests(unittest.TestCase):
    def test_donation_interactions(self):
        result = subprocess.run(
            ["node", "--test", "website/test_donate.cjs"],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
