"""Navigation completeness, context and renderer-compatible heading links."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from documents import Documents
from docs_navigation import DocsNavigation, GROUPS

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = []
        self.ids = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.append(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])


class DocsNavigationTests(unittest.TestCase):
    def setUp(self):
        self.documents = Documents(ROOT)
        self.navigation = DocsNavigation(self.documents)

    def test_catalog_has_every_record_once_and_unique_section_ids(self):
        parsed = Links(self.navigation.index())
        self.assertEqual(
            Counter(link["href"] for link in parsed.links),
            Counter(record["page"] for record in self.documents.records),
        )
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
        self.assertEqual(len(self.navigation.groups), 7)
        for page, (group, _, _) in self.navigation.by_page.items():
            if "verification" in page or "brand-provenance" in page:
                self.assertEqual(group["title"], "Reference and verification")

    def test_missing_unknown_duplicate_records_fail(self):
        self.documents.records.pop()
        with self.assertRaisesRegex(ValueError, "Missing"):
            DocsNavigation(self.documents)
        self.documents = Documents(ROOT)
        self.documents.records.append(
            dict(repository="grok-gadgets", source="new.md", page="new.html")
        )
        with self.assertRaisesRegex(ValueError, "Unmapped"):
            DocsNavigation(self.documents)
        self.documents = Documents(ROOT)
        self.documents.records.append(dict(self.documents.records[0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            DocsNavigation(self.documents)

    def test_duplicate_taxonomy_entry_fails(self):
        with patch("docs_navigation.GROUPS", GROUPS + (GROUPS[0],)):
            with self.assertRaisesRegex(ValueError, "Duplicate navigation"):
                DocsNavigation(self.documents)

    def test_active_sidebar_opens_parent_and_subgroup(self):
        page = self.documents.lookup[("grok-gadgets-esp32-sdk", "docs/sdk.md")]
        html = self.navigation.sidebar(page)
        self.assertIn(
            '<details class="doc-nav-group" open><summary>Build a gadget</summary>',
            html,
        )
        self.assertIn(
            '<details class="doc-nav-subgroup" open><summary>ESP32 SDK</summary>', html
        )
        active = [
            link for link in Links(html).links if link.get("aria-current") == "page"
        ]
        self.assertEqual([link["href"] for link in active], [page])
        self.assertNotIn(
            '<details class="doc-nav-subgroup" open><summary>Linux SDK</summary>', html
        )

    def test_breadcrumbs_and_related_stay_in_subgroup(self):
        first = self.documents.lookup[("grok-gadgets-linux-sdk", "README.md")]
        last = self.documents.lookup[("grok-gadgets-linux-sdk", "docs/operation.md")]
        crumb = self.navigation.breadcrumbs(first)
        self.assertIn("docs.html#build-a-gadget", crumb)
        self.assertIn("docs.html#linux-sdk", crumb)
        self.assertIn('aria-current="page">Linux SDK overview', crumb)
        self.assertNotIn('rel="prev"', self.navigation.related(first))
        self.assertNotIn('rel="next"', self.navigation.related(last))
        for link in Links(self.navigation.related(first)).links:
            self.assertIn("linux-sdk", link["href"])

    def test_community_drafts_are_maintenance(self):
        page = self.documents.lookup[
            ("grok-gadgets", "community/drafts/initial-posts.md")
        ]
        group, subgroup, _ = self.navigation.by_page[page]
        self.assertEqual(
            (group["title"], subgroup["title"]), ("Community", "Community maintenance")
        )

    def test_toc_matches_rendered_duplicate_and_formatted_headings(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "headings.md"
            path.write_text(
                "# Repeat\n\n## Repeat\n\n### Repeat\n\n## Use **tools** & `commands`\n\n#### Repeat\n\n## Repeat\n\n```md\n## Not a heading\n```\n"
            )
            record = dict(
                repository="grok-gadgets",
                source="README.md",
                snapshot=str(path),
                page="test.html",
            )
            toc = self.navigation.toc(record)
            anchors = [link["href"][1:] for link in Links(toc).links]
            self.assertEqual(
                anchors, ["repeat-2", "repeat-3", "use-tools-commands", "repeat-5"]
            )
            self.assertTrue(
                set(anchors).issubset(set(Links(self.documents.render(record)).ids))
            )
            self.assertIn("Use tools &amp; commands", toc)
            self.assertNotIn("Not a heading", toc)

    def test_toc_pinned_snapshot_ignores_wrapper(self):
        record = next(
            record for record in self.documents.records if record.get("sha256")
        )
        toc_links = Links(self.navigation.toc(record)).links
        rendered_ids = Links(self.documents.render(record)).ids
        self.assertTrue(toc_links)
        self.assertTrue(all(link["href"][1:] in rendered_ids for link in toc_links))

    def test_empty_toc_has_no_empty_navigation(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "empty.md"
            path.write_text("# Only title\n\nNo sections.\n")
            self.assertEqual(self.navigation.toc({"snapshot": str(path)}), "")


if __name__ == "__main__":
    unittest.main()
