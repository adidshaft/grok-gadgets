"""Safe pinned Markdown, original source-relative links and accessible static diagrams."""

from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, quote
import json
import hashlib
import posixpath
import re
import shlex
import subprocess
import xml.etree.ElementTree as ET

from markdown_it import MarkdownIt

REPOSITORIES = {
    "grok-gadgets",
    "grok-gadgets-gateway",
    "grok-gadgets-linux-sdk",
    "grok-gadgets-esp32-sdk",
    "grok-gadgets-home-assistant",
}


def page_name(snapshot):
    return "doc-" + snapshot.replace("/", "-").removesuffix(".md") + ".html"


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"


def safe_url(url):
    decoded = unquote(url).strip()
    parts = urlsplit(decoded)
    return (
        not any(ord(c) < 32 for c in decoded)
        and not decoded.startswith("//")
        and (not parts.scheme or parts.scheme.lower() in {"https", "http", "mailto"})
        and "\\" not in decoded
    )


def static_diagram(source):
    """Bounded flowchart subset: no Mermaid runtime, directives, HTML or callbacks."""
    lines = [s.strip() for s in source.splitlines() if s.strip()]
    if len(lines) > 80 or not lines or lines[0] not in {"flowchart LR", "flowchart TD"}:
        raise ValueError("Unsupported or oversized diagram")
    nodes, edges = {}, []
    atom = r'([A-Za-z][A-Za-z0-9_]{0,30})(?:\[(?:"([\w .,()/:+&-]{1,100})"|([\w .,()/:+&-]{1,100}))\])?'
    for line in lines[1:]:
        line = line.replace("<br/>", " ").replace("<br>", " ")
        match = re.fullmatch(
            atom
            + r'\s*(-->|-\.->|<-->)\s*(?:\|"?([\w .,()/:+&-]{1,80})"?\|)?\s*'
            + atom,
            line,
        )
        if not match:
            raise ValueError("Unsafe or unsupported diagram statement")
        a, quoted_a, plain_a, kind, edge_label, b, quoted_b, plain_b = match.groups()
        for key, label in [(a, quoted_a or plain_a), (b, quoted_b or plain_b)]:
            if label and key in nodes and nodes[key] not in {key, label}:
                raise ValueError("Conflicting diagram label")
            nodes.setdefault(key, label or key)
            if label:
                nodes[key] = label
        edges.append((a, b, kind, edge_label or ""))
    if not nodes or len(nodes) > 24:
        raise ValueError("Empty or oversized diagram")
    # Dag layering with a bounded cycle check; supported diagrams are acyclic.
    levels = {key: 0 for key in nodes}
    for step in range(len(nodes)):
        changed = False
        for a, b, kind, edge_label in edges:
            if levels[b] <= levels[a]:
                levels[b] = levels[a] + 1
                changed = True
        if not changed:
            break
    else:
        raise ValueError("Cyclic diagram unsupported")
    columns = {}
    for key, level in levels.items():
        columns.setdefault(level, []).append(key)
    positions = {
        key: (24 + level * 220, 40 + row * 100)
        for level, keys in columns.items()
        for row, key in enumerate(keys)
    }
    width = (max(levels.values()) + 1) * 220 + 24
    height = max(len(keys) for keys in columns.values()) * 100 + 20
    description = "; ".join(
        nodes[a]
        + (" exchanges with " if kind == "<-->" else " to ")
        + nodes[b]
        + (" (pending)" if kind == "-.->" else "")
        + (": " + label if label else "")
        for a, b, kind, label in edges
    )
    parts = [
        f'<figure class="document-diagram" tabindex="0" aria-label="Scrollable connection diagram"><svg role="img" aria-label="Connection diagram" '
        f'viewBox="0 0 {width} {height}"><title>Connection diagram</title><desc>{escape(description)}</desc>'
    ]
    for a, b, kind, edge_label in edges:
        x, y = positions[a]
        tx, ty = positions[b]
        dash = ' stroke-dasharray="6 5"' if kind == "-.->" else ""
        parts.append(
            f'<path d="M{x + 174},{y + 25}L{tx - 8},{ty + 25}" fill="none" stroke="currentColor"{dash}/>'
            + f'<path d="M{tx - 15},{ty + 20}L{tx - 8},{ty + 25}L{tx - 15},{ty + 30}" fill="none" stroke="currentColor"/>'
        )
        if kind == "<-->":
            parts.append(
                f'<path d="M{x + 181},{y + 20}L{x + 174},{y + 25}L{x + 181},{y + 30}" fill="none" stroke="currentColor"/>'
            )
        if edge_label:
            parts.append(
                f'<text x="{(x + 174 + tx) / 2}" y="{y + 15}" text-anchor="middle" font-size="10">{escape(edge_label)}</text>'
            )
    for key, (x, y) in positions.items():
        parts.append(
            f'<rect x="{x}" y="{y}" width="174" height="50" rx="3" fill="white" stroke="currentColor"/>'
            f'<text x="{x + 87}" y="{y + 30}" text-anchor="middle" font-size="14">{escape(nodes[key])}</text>'
        )
    parts.append(
        f"</svg><figcaption>{escape(description)}. Intended paths; verification gates apply.</figcaption></figure>"
    )
    return "".join(parts)


class Documents:
    def __init__(self, root):
        self.root = Path(root)
        config = json.loads((self.root / "website/documents.json").read_text())
        self.hub_references = set(config.get("hub_references", []))
        self.bundled_references = {}
        self.records = []
        for source in config["hub"]:
            self.records.append(
                dict(
                    repository="grok-gadgets",
                    source=source,
                    snapshot=source,
                    page=page_name(source),
                    commit=None,
                )
            )
        for record in json.loads(
            (self.root / "compatibility/documentation-sources.json").read_text()
        ):
            if record["source"] in config["component_sources"]:
                self.records.append({**record, "page": page_name(record["snapshot"])})
        for alias in config["aliases"]:
            self.records.append(
                dict(
                    repository="grok-gadgets",
                    source=alias["source"],
                    snapshot=alias["source"],
                    page=alias["page"],
                    commit=None,
                )
            )
        self.lookup = {(r["repository"], r["source"]): r["page"] for r in self.records}
        self.references = {}
        self.images = {}
        for image in config.get("images", []):
            source = self.root / image["source"]
            if (
                image["repository"] != "grok-gadgets"
                or source.suffix not in {".png", ".jpg", ".svg", ".webp"}
                or (
                    source.suffix == ".png"
                    and not source.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
                )
                or (
                    source.suffix == ".jpg"
                    and not source.read_bytes().startswith(b"\xff\xd8\xff")
                )
                or (source.suffix == ".webp" and source.read_bytes()[8:12] != b"WEBP")
            ):
                raise ValueError("Unapproved documentation image")
            if hashlib.sha256(source.read_bytes()).hexdigest() != image["sha256"]:
                raise ValueError("Documentation image provenance mismatch")
            if source.suffix == ".svg":
                tree = ET.fromstring(source.read_text())
                allowed = {
                    "svg",
                    "title",
                    "desc",
                    "rect",
                    "text",
                    "path",
                    "circle",
                    "g",
                }
                if any(
                    node.tag.split("}")[-1] not in allowed
                    or any(
                        key.lower().startswith("on")
                        or key.split("}")[-1] in {"href", "src"}
                        for key in node.attrib
                    )
                    for node in tree.iter()
                ):
                    raise ValueError("Unsafe documentation SVG")
                if not tree.findall(
                    "{http://www.w3.org/2000/svg}title"
                ) or not tree.findall("{http://www.w3.org/2000/svg}desc"):
                    raise ValueError("Documentation SVG needs title and description")
            self.images[(image["repository"], image["source"])] = image["output"]
            # A component doc may show the same approved bytes from its own path.
            for same in image.get("same_as", []):
                copy = self.root.parent / same["repository"] / same["source"]
                if copy.is_file() and copy.read_bytes() != source.read_bytes():
                    raise ValueError("Component image differs from the approved copy")
                self.images[(same["repository"], same["source"])] = image["output"]
        self.parser = MarkdownIt(
            "commonmark", {"html": False, "linkify": False}
        ).enable("table")
        self.parser.validateLink = safe_url

    def resolve(self, url, record, image=False):
        if not safe_url(url):
            raise ValueError("Unsafe documentation URL")
        parsed = urlsplit(url)
        if parsed.scheme:
            if image:
                raise ValueError("Remote documentation images are not bundled")
            return url
        raw_path = unquote(parsed.path)
        if not raw_path:
            return (
                "#" + quote(unquote(parsed.fragment), safe="-_")
                if parsed.fragment
                else record["page"]
            )
        if raw_path.startswith("/"):
            raise ValueError("Absolute filesystem documentation link")
        virtual = posixpath.normpath(
            "/"
            + record["repository"]
            + "/"
            + posixpath.dirname(record["source"])
            + "/"
            + raw_path
        )
        pieces = virtual.lstrip("/").split("/", 1)
        if len(pieces) != 2 or pieces[0] not in REPOSITORIES:
            raise ValueError("Documentation link escapes project repositories")
        repo, source = pieces
        target = self.lookup.get((repo, source))
        if target:
            return target + (
                "#" + quote(unquote(parsed.fragment), safe="-_")
                if parsed.fragment
                else ""
            )
        if (repo, source) in self.images:
            return self.images[(repo, source)]
        if image:
            raise ValueError("Local image must be explicitly bundled before rendering")
        if repo == "grok-gadgets" and source in self.hub_references:
            local = self.root / source
            if (
                local.is_symlink()
                or not local.resolve().is_relative_to(self.root.resolve())
                or not local.is_file()
                or local.stat().st_size > 1024 * 1024
            ):
                raise ValueError("Unsafe bundled project reference")
            # Selected public records work from both Git clones and source archives.
            # Content hashes identify these bytes without inventing an archive HEAD.
            digest = hashlib.sha256(local.read_bytes()).hexdigest()
            output = "source/" + digest[:16] + "-" + local.name
            self.bundled_references[output] = {"source": source, "sha256": digest}
            return output
        # A real checkout alternative: verify the exact tracked object exists, never invent a public URL.
        checkout = self.root if repo == "grok-gadgets" else self.root.parent / repo
        commit = record.get("commit") if repo == record["repository"] else None
        if (checkout / ".git").exists():
            commit = (
                commit
                or subprocess.check_output(
                    ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
                ).strip()
            )
            subprocess.run(
                ["git", "-C", str(checkout), "cat-file", "-e", commit + ":" + source],
                check=True,
                capture_output=True,
            )
        else:
            # A standalone hub checkout uses the exact tracked component inventory.
            inventory = json.loads(
                (self.root / "compatibility/source-inventory.json").read_text()
            )
            origin = next(
                (item for item in inventory if item["repository"] == repo), None
            )
            if (
                not origin
                or source not in origin["files"]
                or (commit and origin["commit"] != commit)
                or not re.fullmatch(r"[0-9a-f]{40}", origin["commit"])
            ):
                raise ValueError("Unverified component source reference")
            commit = origin["commit"]
        key = (
            slug(repo + "-" + source)
            + "-"
            + hashlib.sha256((repo + "/" + source).encode()).hexdigest()[:8]
        )
        self.references[key] = dict(repository=repo, source=source, commit=commit)
        return "source-reference.html#" + key

    def render(self, record):
        text = (self.root / record["snapshot"]).read_text()
        if record.get("sha256"):
            marker = "This is a pinned documentation snapshot. Relative filesystem paths describe the component checkout.\n\n"
            if marker not in text:
                raise ValueError("Missing pinned documentation origin")
            text = text.split(marker, 1)[1]
            if hashlib.sha256(text.encode()).hexdigest() != record["sha256"]:
                raise ValueError("Pinned documentation hash mismatch")
        # Public content deliberately excludes journals, private host records and broad recursive imports.
        text = re.sub(r"/Users/[^/\s]+/projects/", "$WORKSPACE/", text)
        tokens = self.parser.parse(text)
        used = {}
        for i, token in enumerate(tokens):
            if token.type == "heading_open":
                heading = tokens[i + 1].content
                key = slug(heading)
                used[key] = used.get(key, 0) + 1
                token.attrSet(
                    "id", key if used[key] == 1 else key + "-" + str(used[key])
                )
            if token.type == "fence" and token.info.strip() == "mermaid":
                token.type = "html_block"
                token.content = static_diagram(token.content)
            for child in token.children or []:
                if child.type == "link_open":
                    child.attrSet("href", self.resolve(child.attrGet("href"), record))
                if child.type == "image":
                    child.attrSet(
                        "src", self.resolve(child.attrGet("src"), record, image=True)
                    )
        return (
            '<article class="document">'
            + self.parser.renderer.render(tokens, self.parser.options, {})
            + "</article>"
        )

    def reference_html(self):
        body = '<article class="document"><h1>Source checkout references</h1><p>These files are not mirrored into the site. Exact checkout commands are below. GitHub destinations are planned until publication.</p>'
        for key, r in sorted(self.references.items()):
            body += (
                '<section id="'
                + key
                + '"><h2>'
                + escape(r["repository"] + "/" + r["source"])
                + "</h2><p>Exact source snapshot:</p><pre><code>"
                + escape(
                    shlex.join(
                        [
                            "git",
                            "-C",
                            r["repository"],
                            "show",
                            r["commit"] + ":" + r["source"],
                        ]
                    )
                )
                + '</code></pre><p><a href="https://github.com/adidshaft/'
                + escape(r["repository"])
                + "/blob/"
                + escape(r["commit"])
                + "/"
                + quote(r["source"], safe="/")
                + '">Planned GitHub source at this commit</a></p></section>'
            )
        return body + "</article>"


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = set(), []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                raise ValueError("Duplicate HTML fragment ID")
            self.ids.add(attrs["id"])
        for attr in ["href", "src"]:
            if attr in attrs:
                self.links.append(attrs[attr])


def check_links(output):
    output = Path(output)
    pages = {}
    for file in output.glob("*.html"):
        parser = PageLinks()
        parser.feed(file.read_text())
        pages[file.name] = parser
    for name, parser in pages.items():
        for link in parser.links:
            if not safe_url(link):
                raise ValueError("Unsafe generated link")
            url = urlsplit(link)
            if url.scheme:
                continue
            target = url.path or name
            if not (output / unquote(target)).is_file():
                raise ValueError(f"Broken local file link: {name} → {target}")
            if url.fragment and (
                target not in pages or unquote(url.fragment) not in pages[target].ids
            ):
                raise ValueError(f"Broken fragment: {name} → {link}")
