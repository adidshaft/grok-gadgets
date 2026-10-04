import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from documents import Documents, PageLinks, check_links, static_diagram

ROOT = Path(__file__).resolve().parents[1]


class DocumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # A selected test file must not depend on activity-test execution order.
        if not (ROOT / "website/dist/index.html").is_file():
            env = dict(os.environ)
            env.pop("GROK_ACTIVITY_FILE", None)
            subprocess.run(
                [sys.executable, "website/build.py"],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
            )

    def render_fixture(self, text):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "fixture.md"
            path.write_text(text)
            return Documents(ROOT).render(
                dict(
                    repository="grok-gadgets",
                    source="README.md",
                    snapshot=str(path),
                    page="fixture.html",
                )
            )

    def test_semantics_anchors_code_and_unsafe_content(self):
        html = self.render_fixture("""# Guide

## Install

A paragraph with [jump](#install), **emphasis** and [unsafe](javascript:alert(1)).

- First
- Second

| Device | Status |
| --- | --- |
| C124 | Pending |

```python
print("<script>code only</script>")
```

<script>alert("raw")</script>
[bad](data:text/html,evil)
[bad](file:///private/file)
""")
        for value in [
            '<h1 id="guide">',
            '<h2 id="install">',
            "<p>",
            "<ul>",
            "<table>",
            '<pre><code class="language-python">',
            'href="#install"',
        ]:
            self.assertIn(value, html)
        self.assertNotIn("<script>", html)
        parser = PageLinks()
        parser.feed(html)
        self.assertFalse(
            any(
                link.startswith(("javascript:", "data:", "file:"))
                for link in parser.links
            )
        )

    def test_original_component_source_relative_links(self):
        documents = Documents(ROOT)
        record = next(
            r
            for r in documents.records
            if r["repository"] == "grok-gadgets-esp32-sdk"
            and r["source"] == "README.md"
        )
        html = documents.render(record)
        self.assertIn(
            'href="doc-docs-components-grok-gadgets-esp32-sdk-build-flash.html"', html
        )
        self.assertIn(
            'href="doc-docs-components-grok-gadgets-esp32-sdk-sdk.html"', html
        )
        self.assertNotIn('<pre class="document">', html)
        # Missing source files cannot acquire fabricated site or GitHub links.
        checkout = ROOT.parent / record["repository"]
        if (checkout / ".git").exists():
            with self.assertRaises(subprocess.CalledProcessError):
                documents.resolve("not-a-real-guide.md", record)
        else:
            with self.assertRaisesRegex(ValueError, "Unverified component"):
                documents.resolve("not-a-real-guide.md", record)
        self.assertEqual(
            documents.resolve("../grok-gadgets/CONTRIBUTING.md", record),
            "doc-CONTRIBUTING.html",
        )
        with self.assertRaises(ValueError):
            documents.resolve("../../outside/private", record)

    def test_diagram_accessibility_and_rejection(self):
        html = static_diagram(
            "flowchart LR\nG[Grok Bot] --> W[Gateway]\nW --> E[ESP32 SDK]"
        )
        self.assertIn('role="img"', html)
        self.assertIn("<desc>Grok Bot to Gateway; Gateway to ESP32 SDK</desc>", html)
        self.assertIn("<figcaption>", html)
        for content in [
            "flowchart LR\nA[<script>] --> B",
            'flowchart LR\nclick A "javascript:alert(1)"',
            '%%{init: {"securityLevel":"loose"}}%%\nflowchart LR',
            "flowchart LR\nA --> B\nB --> A",
            "flowchart LR\n" + "A --> B\n" * 81,
        ]:
            with self.subTest(content=content), self.assertRaises(ValueError):
                static_diagram(content)

    def test_source_archive_bundles_only_allowlisted_hub_references(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "website").mkdir()
            (root / "compatibility").mkdir()
            (root / "compatibility/documentation-sources.json").write_text("[]")
            (root / "compatibility/source-inventory.json").write_text("[]")
            (root / "website/documents.json").write_text(
                json.dumps(
                    {
                        "hub": [],
                        "component_sources": [],
                        "aliases": [],
                        "hub_references": ["LICENSE", "alias"],
                    }
                )
            )
            (root / "LICENSE").write_text("Public license fixture")
            (root / "private.txt").write_text("excluded")
            (root / "alias").symlink_to(root / "LICENSE")
            documents = Documents(root)
            record = {
                "repository": "grok-gadgets",
                "source": "README.md",
                "page": "index.html",
            }
            output = documents.resolve("LICENSE", record)
            self.assertTrue(output.startswith("source/"))
            self.assertEqual(documents.bundled_references[output]["source"], "LICENSE")
            with self.assertRaises(ValueError):
                documents.resolve("private.txt", record)
            with self.assertRaisesRegex(ValueError, "Unsafe bundled"):
                documents.resolve("alias", record)

    def test_quoted_pending_and_bidirectional_diagram_meaning(self):
        html = static_diagram(
            'flowchart LR\nA["SDK library + agent"] <-->|"Loopback ACK"| G["Gateway"]\nB["Grok pending"] -.-> G'
        )
        self.assertIn("exchanges with Gateway", html)
        self.assertIn("(pending)", html)
        self.assertIn('stroke-dasharray="6 5"', html)
        self.assertIn("Loopback ACK", html)

    def test_failed_build_keeps_previous_site(self):
        preview = ROOT / "website/dist/index.html"
        before = preview.read_bytes()
        # Invalid activity intentionally becomes an unavailable state. Challenge
        # promotion with a real validation failure after staging the new site.
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import runpy,sys; from unittest.mock import patch; "
                "sys.path.insert(0, 'website'); "
                "patcher=patch('documents.check_links', side_effect=ValueError('injected broken link')); "
                "patcher.start(); runpy.run_path('website/build.py', run_name='__main__')",
            ],
            cwd=ROOT,
            env=os.environ.copy(),
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"injected broken link", result.stderr)
        self.assertEqual(preview.read_bytes(), before)

    def test_fragment_checker(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d)
            (output / "a.html").write_text('<a href="b.html#setup">Setup</a>')
            (output / "b.html").write_text('<h1 id="setup">Setup</h1>')
            check_links(output)
            (output / "b.html").write_text('<h1 id="renamed">Setup</h1>')
            with self.assertRaisesRegex(ValueError, "Broken fragment"):
                check_links(output)

    def test_actual_build_cleans_stale_output_and_excludes_private_records(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "website") as d:
            preserved = Path(d) / "unrelated.txt"
            preserved.write_text("preserve this")
            stale = ROOT / "website/dist/doc-deleted-source.html"
            stale.write_text("obsolete")
            env = dict(os.environ)
            env.pop("GROK_ACTIVITY_FILE", None)
            subprocess.run(
                [sys.executable, "website/build.py"],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
            )
            self.assertFalse(stale.exists())
            self.assertEqual(preserved.read_text(), "preserve this")
            output = ROOT / "website/dist"
            self.assertFalse(
                (output / "doc-docs-verification-hardening-journal.html").exists()
            )
            self.assertFalse((output / "doc-docs-implementation-plan.html").exists())
            for path in output.glob("*.html"):
                self.assertNotIn("/Users/", path.read_text())
            architecture = (output / "doc-docs-architecture-overview.html").read_text()
            self.assertIn('<svg role="img"', architecture)
            self.assertIn('src="media/grok-gadgets-icon.png"', architecture)
            config = json.loads((ROOT / "website/documents.json").read_text())
            self.assertFalse(any("verification/" in s for s in config["hub"]))
