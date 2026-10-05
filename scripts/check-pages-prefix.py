"""Rehearse links, deep pages and downloads at the public site URL."""

import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "website"))
from documents import PageLinks  # noqa: E402

BASE = os.environ.get(
    "GROK_GADGETS_PUBLIC_SITE", "https://grok-gadgets.pages.dev/"
).strip()


def check(output, base=BASE):
    output = Path(output)
    origin = urlsplit(base)
    pages = {}
    for path in output.glob("*.html"):
        parser = PageLinks()
        parser.feed(path.read_text())
        pages[path.name] = parser
    checked = 0
    for name, parser in pages.items():
        # GitHub serves 404 at arbitrary nested paths; its assets must still resolve.
        current = urljoin(base, "missing/deep/page" if name == "404.html" else name)
        for link in parser.links:
            target = urlsplit(urljoin(current, link))
            if target.netloc != origin.netloc or target.scheme != origin.scheme:
                continue
            if not target.path.startswith(origin.path):
                raise ValueError("Link escapes project prefix: " + link)
            relative = unquote(target.path[len(origin.path) :]) or "index.html"
            if name == "404.html" and link.startswith("#"):
                if target.fragment not in parser.ids:
                    raise ValueError("Broken 404 fragment")
                continue
            if not (output / relative).is_file():
                raise ValueError("Broken prefixed/deep link: " + name + " → " + link)
            if target.fragment and (
                relative not in pages
                or unquote(target.fragment) not in pages[relative].ids
            ):
                raise ValueError("Broken prefixed fragment")
            checked += 1
    manifest = json.loads(
        (output / "downloads/simulator-kit-manifest.json").read_text()
    )
    filename = (
        "grok-gadgets-simulator-kit-"
        + manifest["gateway_commit"][:8]
        + "-"
        + manifest["archive_sha256"][:12]
        + ".zip"
    )
    if (
        hashlib.sha256((output / "downloads" / filename).read_bytes()).hexdigest()
        != manifest["archive_sha256"]
    ):
        raise ValueError("Versioned download does not match tested manifest")
    return {
        "base_url": base,
        "pages": len(pages),
        "resolved_local_links": checked,
        "download_sha256": manifest["archive_sha256"],
        "evidence": "local URL-prefix rehearsal; verify live Cloudflare delivery after deployment",
    }


if __name__ == "__main__":
    print(json.dumps(check(ROOT / "website/dist"), indent=2))
