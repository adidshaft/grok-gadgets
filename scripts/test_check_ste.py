"""The plain-language check fails long sentences and ignores code and tables."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load():
    spec = importlib.util.spec_from_file_location(
        "check_ste", ROOT / "scripts/check_ste.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PlainLanguageTests(unittest.TestCase):
    def check(self, text):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "README.md"
            path.write_text(text)
            return load().main([str(path)])

    def test_long_sentence_fails_and_short_ones_pass(self):
        self.assertEqual(self.check("Run the gateway. It lists your gadgets.\n"), 0)
        long = " ".join(["word"] * 26) + "."
        self.assertEqual(self.check(long + "\n"), 1)

    def test_code_tables_headings_and_link_targets_are_ignored(self):
        text = (
            "# " + " ".join(["Heading"] * 30) + "\n\n"
            "| " + " ".join(["cell"] * 30) + " |\n\n"
            "```sh\n" + " ".join(["code"] * 40) + "\n```\n\n"
            "Read the [guide](https://example.com/" + "a/" * 40 + ").\n"
        )
        self.assertEqual(self.check(text), 0)

    def test_quoted_prompt_ends_a_sentence(self):
        quote = "Ask: \u201c" + " ".join(["word"] * 15) + ".\u201d"
        self.assertEqual(
            self.check(quote + " " + "Then " + " ".join(["check"] * 15) + ".\n"), 0
        )


if __name__ == "__main__":
    unittest.main()
