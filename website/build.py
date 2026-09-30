"""Static, escaped, source-driven documentation and roadmap builder."""

from html.parser import HTMLParser
from pathlib import Path
from html import escape as e
import json
import shutil
import os

R = Path(__file__).resolve().parents[1]
OUT = R / "website/dist"
OUT.mkdir(parents=True, exist_ok=True)
issues = json.loads((R / "planning/issues.json").read_text())
# Input path is a build-time option, never a browser token or runtime fetch.
activity_path = os.environ.get("GROK_ACTIVITY_FILE")
activity = (
    json.loads(Path(activity_path).read_text())
    if activity_path
    else {"state": "unavailable", "reason": "Public repositories have not been created"}
)
if activity.get("state") not in ["fixture", "unavailable", "cached", "live"]:
    raise ValueError("Unknown activity state")


def activity_html(record):
    state = record["state"]
    body = (
        '<p class="status">'
        + e(state.upper())
        + " — "
        + e(record.get("reason", "GitHub project activity"))
        + "</p>"
    )
    if state == "unavailable":
        return body
    body += (
        "<p>Last successful refresh: "
        + e(record.get("last_successful_refresh", "Not a live refresh; fixture"))
        + "</p>"
    )
    data = record.get("data", {})
    for key, label in [
        ("aggregate_stars", "Aggregate stars (sum, not unique people)"),
        ("open_issues", "Open issues, excluding PRs"),
        ("contributors", "Deduplicated contributors"),
        (
            "active_contributors",
            "Active contributors, eligible merged PR in last 90 days",
        ),
    ]:
        value = data.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("Invalid activity count")
        body += "<p>" + label + ": " + str(value) + "</p>"
    for release in data.get("releases", []):
        body += (
            "<p>"
            + e(release["repository"])
            + " · "
            + e(release["name"])
            + " · "
            + e(release["date"])
            + "</p>"
        )
    if state == "fixture":
        body += "<p>Synthetic development fixture. These numbers are not real project activity.</p>"
    if state == "cached":
        body += "<p>Refresh failed. Timestamped cached result; not current live activity.</p>"
    return body


NAVIGATION = [
    ("start.html", "Get started"),
    ("docs.html", "Documentation"),
    ("roadmap.html", "Roadmap"),
    ("community.html", "Community"),
]


def page(name, title, body):
    home = name == "index.html"
    active_links = "".join(
        '<a href="'
        + path
        + '"'
        + (' aria-current="page"' if path == name else "")
        + ">"
        + label
        + "<span>↗</span></a>"
        for path, label in NAVIGATION
    )
    menu = (
        '<dialog id="site-menu" aria-labelledby="menu-title"><div class="menu-top"><p id="menu-title">Explore</p><button id="menu-close" aria-label="Close menu">Close <span>[esc]</span></button></div><nav aria-label="Main navigation">'
        + active_links
        + '</nav><div class="menu-components"><a href="esp32.html">ESP32</a><a href="linux.html">Linux</a><a href="home-assistant.html">Home Assistant</a><a href="architecture.html">Architecture</a><a href="releases.html">Releases</a></div><div class="product-reference"><img src="media/spacexai-mark.svg" width="28" height="28" alt="SpaceXAI"><p>Grok is made by SpaceXAI.<br>Grok Gadgets is an independent project.</p><a href="https://x.ai/legal/brand-guidelines" aria-label="Official brand guidelines">↗</a></div></dialog>'
    )
    footer = '<footer class="site-footer"><a href="start.html">Start building ↗</a><span class="independent-note">Independent. Open source.</span><button id="motion-toggle" aria-pressed="false">Pause motion <span>[Ⅱ]</span></button></footer>'
    scripts = '<script src="motion.js" defer></script>' + (
        '<script src="scene.js" defer></script>' if home else ""
    )
    (OUT / name).write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Open source devices for Grok. Explore the local alpha."><title>'
        + e(title)
        + ' · Grok Gadgets</title><link rel="icon" type="image/png" href="media/grok-gadgets-icon.png"><link rel="stylesheet" href="style.css">'
        + ('<link rel="stylesheet" href="scene.css">' if home else "")
        + '</head><body class="'
        + ("home-page" if home else "content-page")
        + '"><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="identity" href="index.html" aria-label="Grok Gadgets home"><img src="media/grok-gadgets-icon.png" width="36" height="36" alt=""><span>Grok Gadgets</span></a><button id="menu-open" aria-haspopup="dialog" aria-controls="site-menu">Menu <span>[M]</span></button></header>'
        + menu
        + '<main id="main">'
        + body
        + "</main>"
        + footer
        + '<noscript><nav class="fallback-navigation" aria-label="Navigation without JavaScript"><a href="start.html">Get started</a> · <a href="docs.html">Docs</a> · <a href="roadmap.html">Roadmap</a> · <a href="community.html">Community</a></nav></noscript>'
        + scripts
        + "</body></html>"
    )


def intro(k, title, desc):
    return (
        '<p class="eyebrow">'
        + e(k)
        + "</p><h1>"
        + title
        + '</h1><p class="lede">'
        + desc
        + "</p>"
    )


def path_row(number, title, description, url, link_text):
    return (
        '<article class="path-row"><span class="path-number">'
        + number
        + "</span><div><h2>"
        + title
        + "</h2><p>"
        + description
        + '</p></div><a href="'
        + url
        + '">'
        + link_text
        + " ↗</a></article>"
    )


scene_source = R / "website/home-scene.html"
page(
    "index.html",
    "Home",
    scene_source.read_text()
    if scene_source.is_file()
    else "<h1>Grok, meet the real world.</h1><p>Interactive architecture is being assembled locally.</p>",
)
page(
    "start.html",
    "Get started",
    intro(
        "Choose a path", "Start small.", "A simulated device is all you need to begin."
    )
    + '<div class="path-list">'
    + path_row(
        "01",
        "Try the simulator",
        "Discover a device. Change its LED. Read button events.",
        "doc-docs-components-grok-gadgets-gateway-README.html",
        "Run the demo",
    )
    + path_row(
        "02",
        "Build a gadget",
        "A reusable SDK for ESP32 or a Linux application.",
        "esp32.html",
        "ESP32",
    )
    + path_row(
        "03",
        "Connect your home",
        "Reuse Home Assistant’s exposed Assist entities.",
        "home-assistant.html",
        "Home Assistant",
    )
    + '</div><p class="quiet-note">Local alpha. Actual Grok connectivity and physical verification are pending.</p>',
)
page(
    "esp32.html",
    "ESP32",
    intro(
        "Hardware / C124",
        "One board.<br>Two possibilities.",
        "An RGB LED. A button. AtomS3 Lite C124.",
    )
    + '<p class="status">Firmware compiled · hardware pending</p>'
    + path_row(
        "01",
        "Build over USB",
        "Pinned firmware, SDK and recovery instructions.",
        "doc-docs-components-grok-gadgets-esp32-sdk-build-flash.html",
        "Build guide",
    )
    + path_row(
        "02",
        "Make it yours",
        "Declare capabilities and handle commands.",
        "doc-docs-components-grok-gadgets-esp32-sdk-sdk.html",
        "SDK reference",
    )
    + '<p class="quiet-note">Target: M5Stack AtomS3 Lite C124 + USB-C data cable. <a href="doc-docs-components-grok-gadgets-esp32-sdk-verification.html">Verification record ↗</a></p>',
)
page(
    "linux.html",
    "Linux SDK",
    intro(
        "SDK / Linux",
        "Your code.<br>Connected.",
        "Declare a capability. Handle a command. Report state.",
    )
    + '<p class="status">15 tests passed on macOS and Linux Docker</p>'
    + path_row(
        "01",
        "Run the agent",
        "Independently installable Python SDK.",
        "doc-docs-components-grok-gadgets-linux-sdk-README.html",
        "Install",
    )
    + path_row(
        "02",
        "Add a capability",
        "Handlers, events and reconnect semantics.",
        "doc-docs-components-grok-gadgets-linux-sdk-development.html",
        "Developer guide",
    )
    + '<p class="quiet-note">Physical peripherals and systemd lifecycle remain pending.</p>',
)
page(
    "home-assistant.html",
    "Home Assistant",
    intro(
        "Existing homes",
        "Use what<br>you already have.",
        "An integration recipe for Home Assistant’s own MCP server.",
    )
    + '<p class="status">Fixture tested · actual home and Grok pending</p>'
    + path_row(
        "01",
        "Expose a few entities",
        "Start with the devices Assist can operate.",
        "doc-docs-components-grok-gadgets-home-assistant-setup.html",
        "Setup recipe",
    )
    + path_row(
        "02",
        "Check compatibility",
        "Read-only discovery. No device actions.",
        "doc-docs-components-grok-gadgets-home-assistant-README.html",
        "Run the probe",
    )
    + '<p class="quiet-note">Upstream MCP notifications are unsupported. Entity coverage varies.</p>',
)
page(
    "architecture.html",
    "Architecture",
    intro(
        "How it works",
        "An action.<br>An observation.",
        "The assistant, connection point and device have separate jobs.",
    )
    + '<div class="flow"><a href="https://x.ai/bot"><img src="media/grok-mark.svg" width="40" height="40" alt="Grok"><span>Grok Bot</span><small>Account route pending</small></a><b>↕ MCP</b><span>Gateway<small>Route and report</small></span><b>↕ USB / local TCP</b><span>Your device<small>Execute and observe</small></span></div><p class="status">Requested → accepted → execution reported → physically observed</p><p><a href="doc-docs-architecture-overview.html">Architecture reference ↗</a></p><p class="quiet-note">Home Assistant can use its upstream MCP route directly. Local MCP success is separate from actual Grok or hardware verification.</p>',
)
rows = "".join(
    '<article class="issue"><span>'
    + e(i["id"])
    + " / "
    + e(i["milestone"])
    + "</span><h3>"
    + e(i["problem"])
    + '</h3><p class="status">'
    + e(i["stage"])
    + "</p><p>"
    + e(i.get("blocker") or " · ".join(i["labels"]))
    + "</p></article>"
    for i in issues
)
page(
    "roadmap.html",
    "Roadmap",
    intro(
        "Source-driven / local issues",
        "What’s next.",
        "Tested local work. Clear external gates.",
    )
    + '<div class="issue-list">'
    + rows
    + "</div>",
)
page(
    "community.html",
    "Community",
    intro(
        "Build together",
        "Makers welcome.",
        "Share a build. Ask a question. Improve the tools.",
    )
    + '<p><a class="text-cta" href="https://www.reddit.com/r/GrokGadgets/">r/GrokGadgets ↗</a></p>'
    + path_row(
        "01",
        "Contribute",
        "Code, tests and documentation all count.",
        "doc-CONTRIBUTING.html",
        "Contribution guide",
    )
    + path_row(
        "02",
        "Recognition",
        "Opt in. Verify ownership. Merge a contribution.",
        "doc-community-contribution-recognition.html",
        "Recognition policy",
    )
    + '<p class="quiet-note">Community policies and live changes remain subject to publication approval.</p>',
)
page(
    "releases.html",
    "Releases",
    intro(
        "Unpublished local candidate",
        "0.1.0-alpha.1",
        "Simulation, separate SDKs, firmware builds and integration recipes.",
    )
    + '<p class="status">Actual Grok · physical hardware · independent reproduction pending</p>'
    + path_row(
        "01",
        "What passed",
        "Exact commits, environments and remaining gates.",
        "doc-docs-verification-local-handoff.html",
        "Local handoff",
    )
    + path_row(
        "02",
        "Project activity",
        "Unavailable until public repositories exist.",
        "activity.html",
        "Data state",
    ),
)
# Technical content remains complete on dedicated reference pages.
for src in [
    R / "CONTRIBUTING.md",
    R / "CODE_OF_CONDUCT.md",
    R / "SECURITY.md",
    *sorted((R / "docs").rglob("*.md")),
    *sorted((R / "community").rglob("*.md")),
]:
    name = "doc-" + str(src.relative_to(R)).replace("/", "-").replace(".md", ".html")
    page(
        name,
        src.stem,
        '<p class="eyebrow">Reference / '
        + e(str(src.relative_to(R)))
        + '</p><pre class="document">'
        + e(src.read_text())
        + "</pre>",
    )
links = "".join(
    '<li><a href="'
    + f.name
    + '">'
    + e(f.stem.removeprefix("doc-").replace("-", " "))
    + "<span>↗</span></a></li>"
    for f in sorted(OUT.glob("doc-*.html"))
)
page(
    "docs.html",
    "Documentation",
    intro("Reference", "Go deeper.", "Setup, SDKs, architecture and verification.")
    + '<ul class="documentation-index">'
    + links
    + "</ul>",
)
page(
    "activity.html",
    "Project activity",
    intro(
        "Source records",
        "Activity.",
        "Always labeled: live, cached, fixture or unavailable.",
    )
    + activity_html(activity),
)
for f in ["style.css", "motion.js", "scene.css", "scene.js"]:
    source = R / "website" / f
    if source.is_file():
        shutil.copy(source, OUT / f)
shutil.copytree(R / "website/media", OUT / "media", dirs_exist_ok=True)


class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if (
                k in ["href", "src"]
                and v
                and not v.startswith(("http:", "https:", "#", "mailto:"))
            ):
                assert (OUT / v.split("#")[0]).is_file(), (self.file, v)


for f in OUT.glob("*.html"):
    parser = Links()
    parser.file = f.name
    parser.feed(f.read_text())
print(f"Built and link-checked {len(list(OUT.glob('*.html')))} static pages")
