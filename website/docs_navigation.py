"""Task-based documentation navigation. Every published page has one home."""

from html import escape
import re

from documents import slug


# Each entry is (repository suffix, source path, reader-facing title).
# An empty suffix identifies the hub. URLs come from Documents, never this map.
GROUPS = (
    (
        "Start here",
        "Choose a path and check what is verified.",
        (
            (
                None,
                (
                    ("", "README.md", "Project overview"),
                    ("", "docs/getting-started/simulator-kit.md", "Try the simulator"),
                    (
                        "",
                        "docs/getting-started/hosting.md",
                        "Hosting and remote access",
                    ),
                    ("", "docs/public/support-matrix.md", "Supported paths and limits"),
                    ("", "SUPPORT.md", "Get help"),
                ),
            ),
        ),
    ),
    (
        "Build a gadget",
        "Use the SDK for your device.",
        (
            (
                "Linux SDK",
                (
                    ("linux-sdk", "README.md", "Linux SDK overview"),
                    ("linux-sdk", "docs/development.md", "Create a Linux gadget"),
                    ("linux-sdk", "docs/operation.md", "Run a Linux gadget"),
                ),
            ),
            (
                "ESP32 SDK",
                (
                    ("esp32-sdk", "README.md", "ESP32 SDK overview"),
                    ("esp32-sdk", "docs/sdk.md", "Use the firmware library"),
                    (
                        "esp32-sdk",
                        "docs/build-flash.md",
                        "Build and flash the C124 example",
                    ),
                    (
                        "esp32-sdk",
                        "docs/board-sources.md",
                        "Board configuration and sources",
                    ),
                    ("esp32-sdk", "docs/dependencies.md", "Firmware dependencies"),
                    ("esp32-sdk", "docs/protocol-recovery.md", "Protocol recovery"),
                    (
                        "",
                        "docs/getting-started/physical-test.md",
                        "Test the physical C124",
                    ),
                ),
            ),
        ),
    ),
    (
        "Gateway and simulator",
        "Connect gadgets and inspect command results.",
        (
            (
                None,
                (
                    ("gateway", "README.md", "Gateway overview"),
                    ("gateway", "docs/local-operation.md", "Run the gateway"),
                    ("gateway", "docs/simulator.md", "Use the gateway simulator"),
                    ("gateway", "docs/architecture.md", "Gateway architecture"),
                ),
            ),
        ),
    ),
    (
        "Home Assistant",
        "Check the existing Home Assistant integration path.",
        (
            (
                None,
                (
                    ("home-assistant", "README.md", "Home Assistant overview"),
                    ("home-assistant", "docs/setup.md", "Set up the integration path"),
                    (
                        "home-assistant",
                        "docs/feasibility.md",
                        "Capabilities and limits",
                    ),
                ),
            ),
        ),
    ),
    (
        "Contribute",
        "Find work and prepare a safe contribution.",
        (
            (
                None,
                (
                    ("", "CONTRIBUTING.md", "Contribution guide"),
                    ("", "docs/contributing/ready-issues.md", "Find an issue"),
                    (
                        "",
                        "docs/contributing/writing-guide.md",
                        "Write clear documentation",
                    ),
                    (
                        "",
                        "docs/contributing/review-and-privacy.md",
                        "Review and privacy checks",
                    ),
                    ("", "SECURITY.md", "Report a security issue"),
                    ("", "GOVERNANCE.md", "Project governance"),
                    ("", "ROADMAP.md", "Project roadmap"),
                ),
            ),
        ),
    ),
    (
        "Community",
        "Join the community and understand its rules.",
        (
            (
                "Participation",
                (
                    ("", "community/README.md", "Community overview"),
                    ("", "community/guidelines.md", "Community guidelines"),
                    ("", "CODE_OF_CONDUCT.md", "Code of conduct"),
                    (
                        "",
                        "community/contribution-recognition.md",
                        "Contributor recognition",
                    ),
                ),
            ),
        ),
    ),
    (
        "Reference",
        "Inspect how the parts fit together.",
        (
            (
                None,
                (("", "docs/architecture/overview.md", "Project architecture"),),
            ),
        ),
    ),
)


# Maintainer and process records: published so links keep working, but listed only on
# maintainers.html, never in the public documentation index or sidebar.
MAINTAINER_GROUPS = (
    (
        "Releases and verification",
        "Release checks and dated evidence records.",
        (
            (
                None,
                (
                    ("gateway", "docs/release.md", "Gateway release checks"),
                    ("", "docs/public/local-status.md", "Overall verification status"),
                    ("", "docs/public/gateway-verification.md", "Gateway verification"),
                    (
                        "",
                        "docs/public/linux-sdk-verification.md",
                        "Linux SDK verification",
                    ),
                    (
                        "",
                        "docs/public/esp32-sdk-verification.md",
                        "ESP32 SDK verification",
                    ),
                    (
                        "",
                        "docs/public/home-assistant-verification.md",
                        "Home Assistant verification",
                    ),
                ),
            ),
        ),
    ),
    (
        "Community operations",
        "Moderation and channel preparation.",
        (
            (
                None,
                (
                    ("", "community/moderation-policy.md", "Moderation policy"),
                    ("", "community/reddit-setup.md", "Reddit setup checklist"),
                    ("", "community/reddit-package.md", "Reddit channel package"),
                    ("", "community/platform-evaluation.md", "Platform evaluation"),
                    ("", "community/content-plan.md", "Community content plan"),
                    ("", "community/drafts/initial-posts.md", "Draft community posts"),
                ),
            ),
        ),
    ),
    (
        "Brand and visuals",
        "Visual sources and asset provenance.",
        (
            (
                None,
                (
                    ("", "docs/visuals/README.md", "Visual guide"),
                    ("", "docs/visuals/brand-provenance.md", "Brand asset provenance"),
                ),
            ),
        ),
    ),
)


class DocsNavigation:
    def __init__(self, documents):
        self.documents = documents
        records = {}
        pages = set()
        for record in documents.records:
            key = (record["repository"], record["source"])
            if key in records or record["page"] in pages:
                raise ValueError("Duplicate documentation record: " + str(key))
            records[key] = record
            pages.add(record["page"])
        self.groups = []
        self.by_page = {}
        used = set()
        audiences = [(group, False) for group in GROUPS]
        audiences += [(group, True) for group in MAINTAINER_GROUPS]
        for (title, description, subgroups), maintainer in audiences:
            group = {
                "title": title,
                "description": description,
                "id": slug(title),
                "subgroups": [],
                "maintainer": maintainer,
            }
            for subtitle, entries in subgroups:
                subgroup = {
                    "title": subtitle,
                    "id": slug(subtitle) if subtitle else group["id"],
                    "items": [],
                }
                for suffix, source, label in entries:
                    key = ("grok-gadgets" + ("-" + suffix if suffix else ""), source)
                    if key in used:
                        raise ValueError("Duplicate navigation entry: " + str(key))
                    if key not in records:
                        raise ValueError("Missing documentation record: " + str(key))
                    used.add(key)
                    item = {
                        "title": label,
                        "page": records[key]["page"],
                        "record": records[key],
                    }
                    subgroup["items"].append(item)
                    self.by_page[item["page"]] = (group, subgroup, item)
                group["subgroups"].append(subgroup)
            self.groups.append(group)
        if used != set(records):
            raise ValueError(
                "Unmapped documentation records: " + str(sorted(set(records) - used))
            )

    @staticmethod
    def _link(item, current=None):
        active = ' aria-current="page"' if item["page"] == current else ""
        return f'<a href="{escape(item["page"], quote=True)}"{active}>{escape(item["title"])}</a>'

    def _audience(self, maintainer):
        return [group for group in self.groups if group["maintainer"] == maintainer]

    def index(self, maintainer=False):
        parts = ['<section class="doc-catalog" aria-label="Documentation topics">']
        for group in self._audience(maintainer):
            parts.append(
                f'<section class="doc-category" id="{escape(group["id"])}"><header><h2>{escape(group["title"])}</h2><p>{escape(group["description"])}</p></header>'
            )
            for subgroup in group["subgroups"]:
                parts.append('<div class="doc-subgroup">')
                if subgroup["title"]:
                    parts.append(
                        f'<h3 id="{escape(subgroup["id"])}">{escape(subgroup["title"])}</h3>'
                    )
                parts.append(
                    '<ul class="doc-links">'
                    + "".join(
                        "<li>" + self._link(item) + "</li>"
                        for item in subgroup["items"]
                    )
                    + "</ul></div>"
                )
            parts.append("</section>")
        return "".join(parts) + "</section>"

    def is_maintainer(self, page):
        found = self.by_page.get(page)
        return bool(found and found[0]["maintainer"]) or page == "maintainers.html"

    def sidebar(self, current_page):
        maintainer = self.is_maintainer(current_page)
        home = "maintainers.html" if maintainer else "docs.html"
        label = "Maintainer records" if maintainer else "All documentation"
        parts = [
            f'<nav class="doc-sidebar-nav" aria-label="Documentation"><a class="doc-nav-home" href="{home}">{label}</a>'
        ]
        for group in self._audience(maintainer):
            active = any(
                item["page"] == current_page
                for subgroup in group["subgroups"]
                for item in subgroup["items"]
            )
            parts.append(
                f'<details class="doc-nav-group"{" open" if active else ""}><summary>{escape(group["title"])}</summary>'
            )
            for subgroup in group["subgroups"]:
                if subgroup["title"]:
                    opened = any(
                        item["page"] == current_page for item in subgroup["items"]
                    )
                    parts.append(
                        f'<details class="doc-nav-subgroup"{" open" if opened else ""}><summary>{escape(subgroup["title"])}</summary>'
                    )
                parts.append(
                    "<ul>"
                    + "".join(
                        "<li>" + self._link(item, current_page) + "</li>"
                        for item in subgroup["items"]
                    )
                    + "</ul>"
                )
                if subgroup["title"]:
                    parts.append("</details>")
            parts.append("</details>")
        return "".join(parts) + "</nav>"

    def breadcrumbs(self, current_page):
        group, subgroup, item = self.by_page[current_page]
        home, label = (
            ("maintainers.html", "Maintainers")
            if group["maintainer"]
            else ("docs.html", "Docs")
        )
        parts = [
            f'<nav class="doc-breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="{home}">{label}</a></li>',
            f'<li><a href="{home}#{escape(group["id"])}">{escape(group["title"])}</a></li>',
        ]
        if subgroup["title"]:
            parts.append(
                f'<li><a href="{home}#{escape(subgroup["id"])}">{escape(subgroup["title"])}</a></li>'
            )
        parts.append(f'<li aria-current="page">{escape(item["title"])}</li></ol></nav>')
        return "".join(parts)

    def related(self, current_page):
        _, subgroup, item = self.by_page[current_page]
        items = subgroup["items"]
        position = items.index(item)
        parts = []
        for index, relation, label in (
            (position - 1, "prev", "Previous"),
            (position + 1, "next", "Next"),
        ):
            if 0 <= index < len(items):
                adjacent = items[index]
                parts.append(
                    f'<a rel="{relation}" href="{escape(adjacent["page"], quote=True)}"><small>{label}</small><strong>{escape(adjacent["title"])}</strong></a>'
                )
        return (
            '<nav class="doc-pagination" aria-label="More in this topic">'
            + "".join(parts)
            + "</nav>"
            if parts
            else ""
        )

    def toc(self, record):
        text = (self.documents.root / record["snapshot"]).read_text()
        if record.get("sha256"):
            marker = "This is a pinned documentation snapshot. Relative filesystem paths describe the component checkout.\n\n"
            if marker not in text:
                raise ValueError("Missing pinned documentation origin")
            text = text.split(marker, 1)[1]
        text = re.sub(r"/Users/[^/\s]+/projects/", "$WORKSPACE/", text)
        tokens = self.documents.parser.parse(text)
        used, entries = {}, []
        for i, token in enumerate(tokens):
            if token.type != "heading_open":
                continue
            inline = tokens[i + 1]
            key = slug(inline.content)
            used[key] = used.get(key, 0) + 1
            anchor = key if used[key] == 1 else key + "-" + str(used[key])
            if token.tag in {"h2", "h3"}:
                label = "".join(
                    child.content
                    if child.type not in {"softbreak", "hardbreak"}
                    else " "
                    for child in inline.children or []
                    if child.type
                    in {"text", "code_inline", "image", "softbreak", "hardbreak"}
                )
                level_class = " toc-subheading" if token.tag == "h3" else ""
                entries.append(
                    f'<li class="doc-toc-{token.tag}{level_class}"><a href="#{escape(anchor)}">{escape(label)}</a></li>'
                )
        if not entries:
            return ""
        return (
            '<details class="doc-toc" open><summary>On this page</summary><nav aria-label="On this page"><ul>'
            + "".join(entries)
            + "</ul></nav></details>"
        )
