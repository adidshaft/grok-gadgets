"""Static, escaped, source-driven documentation and roadmap builder."""

from pathlib import Path
from html import escape as e
import json
import shutil
import os
import importlib.util
import tempfile
import re
from activity import load_activity
from documents import Documents, check_links

R = Path(__file__).resolve().parents[1]
DESTINATION = R / "website/dist"
kit_spec = importlib.util.spec_from_file_location(
    "simulator_kit", R / "scripts/build-simulator-kit.py"
)
kit_builder = importlib.util.module_from_spec(kit_spec)
kit_spec.loader.exec_module(kit_builder)
simulator_build = kit_builder.ensure_current(R / "website/downloads")
# Assemble the whole site away from the last known-good preview. Promote only after validation.
if DESTINATION.is_symlink():
    raise ValueError("Generated output must not be a symlink")
(R / "artifacts").mkdir(exist_ok=True)
site_staging = tempfile.TemporaryDirectory(prefix="site-build-", dir=R / "artifacts")
OUT = Path(site_staging.name) / "dist"
OUT.mkdir()
kit_identity = (
    simulator_build["gateway_commit"][:8] + "-" + simulator_build["archive_sha256"][:12]
)
kit_archive = "grok-gadgets-simulator-kit-" + kit_identity + ".zip"
kit_manifest = "simulator-kit-" + kit_identity + "-manifest.json"
PUBLIC_SITE = "https://adidshaft.github.io/grok-gadgets/"
issues = json.loads((R / "planning/issues.json").read_text())
# Input path is a build-time option, never a browser token or runtime fetch.
activity_path = os.environ.get("GROK_ACTIVITY_FILE")
activity = (
    load_activity(Path(activity_path), allow_fixture=True, classify_stale=True)
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
        body += "<p>Cached result: refresh failed or overdue. Last successful timestamp shown; not current live activity.</p>"
    return body


NAVIGATION = [
    ("start.html", "Get started"),
    ("docs.html", "Documentation"),
    ("roadmap.html", "Roadmap"),
    ("community.html", "Community"),
    ("contribute.html", "Contribute"),
]


def page(name, title, body):
    home = name == "index.html"
    body = body.replace(
        "downloads/grok-gadgets-simulator-kit.zip", "downloads/" + kit_archive
    ).replace("downloads/simulator-kit-manifest.json", "downloads/" + kit_manifest)
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
        + '</nav><div class="menu-components"><a href="https://github.com/adidshaft/grok-gadgets">GitHub (planned)</a><a href="esp32.html">ESP32</a><a href="linux.html">Linux</a><a href="home-assistant.html">Home Assistant</a><a href="architecture.html">Architecture</a><a href="releases.html">Releases</a></div><div class="product-reference"><img src="media/spacexai-mark.svg" width="28" height="28" alt="SpaceXAI"><p>Grok is made by SpaceXAI.<br>Grok Gadgets is an independent project.</p><a href="https://x.ai/legal/brand-guidelines" aria-label="Official brand guidelines">↗</a></div></dialog>'
    )
    footer = '<footer class="site-footer"><a href="start.html">Start building ↗</a><span class="independent-note">Independent. Open source.</span><button id="motion-toggle" aria-pressed="false">Pause motion <span>[Ⅱ]</span></button></footer>'
    scripts = '<script src="motion.js" defer></script>' + (
        '<script src="simulator.js" defer></script><script src="scene.js" defer></script>'
        if home
        else ""
    )
    (OUT / name).write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Open source devices for Grok. Explore the local alpha."><title>'
        + e(title)
        + ' · Grok Gadgets</title><link rel="canonical" href="'
        + PUBLIC_SITE
        + name
        + '"><meta property="og:title" content="'
        + e(title)
        + ' · Grok Gadgets"><meta property="og:description" content="Open-source devices for Grok. Try a simulator, explore separate SDKs and contribute to the experimental alpha."><meta property="og:image" content="'
        + PUBLIC_SITE
        + 'media/grok-gadgets-icon.png"><meta property="og:url" content="'
        + PUBLIC_SITE
        + name
        + '"><meta name="twitter:card" content="summary"><link rel="icon" type="image/png" href="media/grok-gadgets-icon.png"><link rel="stylesheet" href="style.css">'
        + ('<link rel="stylesheet" href="scene.css">' if home else "")
        + '</head><body class="'
        + ("home-page" if home else "content-page")
        + '"><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="identity" href="index.html" aria-label="Grok Gadgets home"><img src="media/grok-gadgets-icon.png" width="36" height="36" alt=""><span>Grok Gadgets</span></a><a class="header-contribute" href="contribute.html">Contribute ↗</a><button id="menu-open" aria-haspopup="dialog" aria-controls="site-menu">Menu <span>[+]</span></button></header>'
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
    (
        scene_source.read_text()
        + (R / "website/playground.html")
        .read_text()
        .replace("{{SIMULATOR_BUILD}}", e(simulator_build["gateway_commit"][:8]))
        .replace("{{SIMULATOR_VERSION}}", e(simulator_build["package_version"]))
        + (R / "website/components.html").read_text()
    )
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
        "Customize in the browser or use your Grok Bot with the inspectable kit.",
        "simulator.html",
        "Try both",
    )
    + path_row(
        "02",
        "Build a gadget",
        "Compile the C124 example with the reusable ESP32 SDK.",
        "esp32.html",
        "ESP32",
    )
    + path_row(
        "03",
        "Build a Linux application",
        "Start from a reusable Python capability and agent.",
        "linux.html",
        "Linux SDK",
    )
    + path_row(
        "04",
        "Connect your home",
        "Reuse Home Assistant’s exposed Assist entities.",
        "home-assistant.html",
        "Home Assistant",
    )
    + '</div><p class="quiet-note">Local alpha. Actual Grok connectivity and physical verification are pending.</p>',
)
page(
    "simulator.html",
    "Simulator",
    intro(
        "No hardware required",
        "Try it.<br>Then make it yours.",
        "One virtual light. Two ways to explore.",
    )
    + path_row(
        "01",
        "In your browser",
        "Color, button events and offline recovery. No downloads or Grok calls.",
        "index.html#playground",
        "Customize & try",
    )
    + path_row(
        "02",
        "With your Grok Bot",
        "An inspectable MCP simulator kit. Install in the Bot’s cloud computer using a supported Command connection.",
        "downloads/grok-gadgets-simulator-kit.zip",
        "Download kit",
    )
    + '<p class="quiet-note">The kit includes readable source, the wheel, locked hashed runtime dependencies, configuration schema and Apache-2.0 notices. Installation downloads the dependencies. No account connection happens automatically.</p>'
    + '<p><a href="doc-docs-getting-started-simulator-kit.html">Step-by-step setup &amp; customization ↗</a></p>'
    + '<p><a href="downloads/simulator-kit-manifest.json">Source commit, contents &amp; SHA256 hashes ↗</a></p>'
    + '<p class="status">Browser simulated · local MCP tested · native Grok receipts, physical and mobile pending</p>',
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
    + '<p class="status">Software tested on macOS and Linux container · peripherals/systemd pending</p>'
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
# Only explicitly selected public documents; original source identities resolve component links.
documents = Documents(R)
for record in documents.records:
    page(
        record["page"],
        next(
            (
                line.removeprefix("# ")
                for line in (R / record["snapshot"]).read_text().splitlines()
                if line.startswith("# ")
            ),
            Path(record["source"]).stem,
        ),
        '<p class="eyebrow">Reference / '
        + e(record["repository"] + "/" + record["source"])
        + "</p>"
        + documents.render(record),
    )
page("source-reference.html", "Source references", documents.reference_html())
doc_groups = [
    ("Start and contribute", {"grok-gadgets"}),
    ("Gateway and simulator", {"grok-gadgets-gateway"}),
    ("Linux SDK", {"grok-gadgets-linux-sdk"}),
    ("ESP32 SDK", {"grok-gadgets-esp32-sdk"}),
    ("Home Assistant", {"grok-gadgets-home-assistant"}),
]
links = ""
for label, repositories in doc_groups:
    links += "<h2>" + label + '</h2><ul class="documentation-index">'
    for record in documents.records:
        if record["repository"] in repositories:
            title = next(
                (
                    line.removeprefix("# ")
                    for line in (R / record["snapshot"]).read_text().splitlines()
                    if line.startswith("# ")
                ),
                record["source"],
            )
            links += (
                '<li><a href="'
                + record["page"]
                + '">'
                + e(title)
                + "<span>↗</span></a></li>"
            )
    links += "</ul>"
page(
    "docs.html",
    "Documentation",
    intro("Reference", "Go deeper.", "Choose a task, then a component.") + links,
)
page(
    "contribute.html",
    "Contribute",
    intro(
        "Software, docs and tests",
        "Make a first change.",
        "Three ready tasks. No hardware or account required.",
    )
    + path_row(
        "01",
        "Ready to contribute",
        "Glossary, troubleshooting and accessible command copying.",
        "doc-docs-contributing-ready-issues.html",
        "Ready queue",
    )
    + path_row(
        "02",
        "Find your repository",
        "Five independently useful components.",
        "doc-CONTRIBUTING.html",
        "Contribution guide",
    )
    + '<p><a href="https://github.com/adidshaft/grok-gadgets">Planned GitHub destination ↗</a></p><p class="quiet-note">GitHub activation pending. After migration, Issues and the Project become authoritative; local snapshots record their refresh time.</p>',
)
page(
    "404.html",
    "Page not found",
    intro("404", "Lost your way?", "This page does not exist.")
    + '<p><a href="'
    + PUBLIC_SITE
    + '">Return to the project ↗</a></p><p><a href="'
    + PUBLIC_SITE
    + 'docs.html">Open documentation ↗</a></p>',
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
for f in ["style.css", "motion.js", "scene.css", "simulator.js", "scene.js"]:
    source = R / "website" / f
    if source.is_file():
        shutil.copy(source, OUT / f)
shutil.copytree(R / "website/media", OUT / "media", dirs_exist_ok=True)
shutil.copytree(R / "website/downloads", OUT / "downloads", dirs_exist_ok=True)
for approved_image in json.loads((R / "website/documents.json").read_text()).get(
    "images", []
):
    destination = OUT / approved_image["output"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(R / approved_image["source"], destination)


# A deep missing URL must load 404 assets from the actual project base.
missing = OUT / "404.html"
missing.write_text(
    re.sub(
        r'(href|src)="([^"#:]*)"',
        lambda match: match[1] + '="' + PUBLIC_SITE + match[2] + '"',
        missing.read_text(),
    )
)
# Content-addressed download URLs prevent an older cached kit/manifest pair appearing current.
shutil.copy(
    OUT / "downloads/grok-gadgets-simulator-kit.zip", OUT / "downloads" / kit_archive
)
shutil.copy(
    OUT / "downloads/simulator-kit-manifest.json", OUT / "downloads" / kit_manifest
)
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    + "".join(
        "<url><loc>" + PUBLIC_SITE + f.name + "</loc></url>"
        for f in sorted(OUT.glob("*.html"))
        if f.name != "404.html"
    )
    + "</urlset>"
)
(OUT / "robots.txt").write_text(
    "User-agent: *\nAllow: /\nSitemap: " + PUBLIC_SITE + "sitemap.xml\n"
)
check_links(OUT)
kit_builder.verify_download(OUT / "downloads", simulator_build["gateway_commit"])
kit_builder.assert_source_unchanged(
    simulator_build["gateway_commit"], simulator_build["build_inputs"]
)
backup = Path(site_staging.name) / "previous-dist"
if DESTINATION.exists():
    DESTINATION.replace(backup)
try:
    OUT.replace(DESTINATION)
except BaseException:
    if backup.exists():
        backup.replace(DESTINATION)
    raise
OUT = DESTINATION
site_staging.cleanup()
print(f"Built and link/fragment-checked {len(list(OUT.glob('*.html')))} static pages")
