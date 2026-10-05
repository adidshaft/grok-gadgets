"""Check crawler-facing share metadata and the public preview image."""

from html.parser import HTMLParser
from pathlib import Path
import struct
import sys


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.canonical = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta":
            key = attrs.get("property") or attrs.get("name")
            if key:
                self.meta[key] = attrs.get("content", "")
        elif tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")


def check(site):
    pages = sorted(site.glob("*.html"))
    if not pages:
        raise ValueError(f"No HTML pages found in {site}")
    for page in pages:
        metadata = Metadata()
        metadata.feed(page.read_text())
        values = metadata.meta
        base = f"https://grok-gadgets.pages.dev/{page.name}"
        image = "https://grok-gadgets.pages.dev/media/grok-gadgets-share-v1.png"
        expected = {
            "description": None,
            "og:type": "website",
            "og:site_name": "Grok Gadgets",
            "og:title": None,
            "og:description": None,
            "og:url": base,
            "og:image": image,
            "og:image:type": "image/png",
            "og:image:width": "1200",
            "og:image:height": "630",
            "og:image:alt": None,
            "twitter:card": "summary_large_image",
            "twitter:title": None,
            "twitter:description": None,
            "twitter:image": image,
            "twitter:image:alt": None,
        }
        for key, value in expected.items():
            actual = values.get(key)
            if not actual or (value is not None and actual != value):
                raise ValueError(f"{page.name}: invalid or missing {key}: {actual!r}")
        for key in ("description", "og:description", "twitter:description"):
            if "Grok Bot" not in values[key] or "Grok Gadgets" not in values[key]:
                raise ValueError(
                    f"{page.name}: description must identify Grok Bot and Grok Gadgets"
                )
        if metadata.canonical != base:
            raise ValueError(
                f"{page.name}: unexpected canonical {metadata.canonical!r}"
            )
        if "localhost" in values["og:image"] or "localhost" in values["twitter:image"]:
            raise ValueError(f"{page.name}: local share image URL")

    image_path = site / "media/grok-gadgets-share-v1.png"
    data = image_path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) < 24:
        raise ValueError(f"Invalid PNG: {image_path}")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1200, 630):
        raise ValueError(f"Unexpected preview dimensions: {width}x{height}")
    print(f"Verified crawler metadata on {len(pages)} pages and {width}x{height} PNG")


if __name__ == "__main__":
    check(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("website/dist"))
