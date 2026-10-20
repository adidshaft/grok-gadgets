"""Static, escaped, source-driven documentation and roadmap builder."""

from datetime import datetime, timezone
from pathlib import Path
from html import escape as e
import json
import hashlib
import shutil
import os
import importlib.util
import tempfile
import re
import sys
from activity import load_activity
from documents import Documents, check_links
from docs_navigation import DocsNavigation

R = Path(__file__).resolve().parents[1]
DESTINATION = R / "website/dist"
kit_spec = importlib.util.spec_from_file_location(
    "simulator_kit", R / "scripts/build-simulator-kit.py"
)
kit_builder = importlib.util.module_from_spec(kit_spec)
kit_spec.loader.exec_module(kit_builder)
simulator_build = kit_builder.verify_download(R / "website/downloads")
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


def site_revision():
    """The hub commit recorded in every footer for deployment evidence."""
    if (R / ".git").exists():
        try:
            import subprocess

            return subprocess.check_output(
                ["git", "rev-parse", "--short=8", "HEAD"], cwd=R, text=True
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            pass
    return "source archive"


build_revision = site_revision()
build_note = (
    "Site "
    + build_revision
    + " · kit from gateway "
    + simulator_build["gateway_commit"][:8]
)
kit_manifest = "simulator-kit-" + kit_identity + "-manifest.json"
PUBLIC_SITE = os.environ.get(
    "GROK_GADGETS_PUBLIC_SITE", "https://grokgadgets.org/"
).strip()
if not re.fullmatch(r"https://[A-Za-z0-9.-]+/", PUBLIC_SITE):
    raise ValueError("GROK_GADGETS_PUBLIC_SITE must be an HTTPS site root URL")
issues = json.loads((R / "planning/issues.json").read_text())
issue_snapshot = None
snapshot_path = R / "publication/github-issues.json"
if snapshot_path.is_file():
    sys.path.insert(0, str(R / "scripts"))
    snapshot_module = importlib.import_module("github_snapshot")
    issue_snapshot = snapshot_module.load_snapshot(snapshot_path)
    issues = issue_snapshot["issues"]
# Input path is a build-time option, never a browser token or runtime fetch.
activity_path = os.environ.get("GROK_ACTIVITY_FILE")
if not activity_path and (R / "publication/github-activity.json").is_file():
    activity_path = str(R / "publication/github-activity.json")
activity = (
    load_activity(Path(activity_path), allow_fixture=True, classify_stale=True)
    if activity_path
    else {
        "state": "unavailable",
        "reason": "GitHub activity snapshot has not been refreshed",
    }
)
if activity.get("state") not in ["fixture", "unavailable", "cached", "live"]:
    raise ValueError("Unknown activity state")


# The page is static, so a fresh fetch is shown as a dated snapshot, never as "live".
ACTIVITY_LABELS = {
    "live": "SNAPSHOT",
    "cached": "CACHED",
    "fixture": "FIXTURE",
    "unavailable": "UNAVAILABLE",
}
ACTIVITY_REFRESH = (
    "<p>This is a snapshot, not a live feed. The site fetches it once a day at 06:17 UTC "
    "and after each successful hub build on main. A commit in a component repository "
    "appears after the next refresh.</p>"
)


def activity_html(record):
    state = record["state"]
    body = (
        '<p class="status">'
        + ACTIVITY_LABELS[state]
        + " — "
        + e(record.get("reason", "GitHub project activity"))
        + "</p>"
    )
    if state == "unavailable":
        return body
    if "last_successful_refresh" in record:
        stamp = datetime.fromisoformat(record["last_successful_refresh"])
        body += (
            '<p>Fetched at: <time datetime="'
            + e(stamp.isoformat())
            + '">'
            + stamp.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            + "</time></p>"
        )
    else:
        body += "<p>Fetched at: never; synthetic fixture</p>"
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
    if state in ["live", "cached"]:
        body += ACTIVITY_REFRESH
    return body


NAVIGATION = [
    ("start.html", "Get started"),
    ("docs.html", "Documentation"),
    ("roadmap.html", "Roadmap"),
    ("community.html", "Community"),
    ("contribute.html", "Contribute"),
    ("donate.html", "Donate"),
]


def page(name, title, body):
    home = name in ("index.html", "donate.html", "playground.html")
    documentation = name == "docs.html" or name.startswith("doc-")
    page_title = title + " · Grok Gadgets"
    description = (
        "Grok Gadgets is an open-source project giving your Grok Bot hands in the "
        "physical world: build hardware, set it up from a phone, just ask."
        if name == "index.html"
        else title
        + ": Grok Gadgets, an independent open-source project that connects real hardware "
        "to your existing Grok Bot."
    )
    share_image = PUBLIC_SITE + "media/grok-gadgets-share-v4.png"
    canonical_url = PUBLIC_SITE + (
        "" if name == "index.html" else name.removesuffix(".html")
    )
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
        + '</nav><div class="menu-components"><a href="https://github.com/adidshaft/grok-gadgets">GitHub</a><a href="esp32.html">ESP32</a><a href="linux.html">Linux</a><a href="home-assistant.html">Home Assistant</a><a href="architecture.html">Architecture</a><a href="releases.html">Releases</a></div><p class="creator-credit">Made by <a href="https://x.com/adidshaft">@adidshaft ↗</a></p><div class="product-reference"><p>Grok Bot is made by SpaceXSI.<br>Grok Gadgets is an independent project.</p><a href="https://x.ai/legal/brand-guidelines" aria-label="Official brand guidelines">↗</a></div></dialog>'
    )
    footer = (
        '<footer class="site-footer" data-site-revision="'
        + e(build_revision)
        + '" title="'
        + e(build_note)
        + '"><span class="independent-note">Independent open source. Not affiliated with SpaceXSI.<span class="footer-credit">Made by <a href="https://x.com/adidshaft">@adidshaft ↗</a></span></span><a href="https://github.com/adidshaft/grok-gadgets">GitHub ↗</a><a class="status-link" href="doc-docs-public-support-matrix.html">Status ↗</a>'
        + '<button id="motion-toggle" aria-pressed="false">Pause motion <span>[Ⅱ]</span></button></footer>'
    )
    scripts = (
        '<script src="motion.js" defer></script><script src="donate.js" defer></script>'
        + (
            '<script src="simulator.js" defer></script><script src="scene.js" defer></script><script src="roadmap-scene.js" defer></script><script src="signal-scene.js" defer></script><script src="hardware-scene.js" defer></script><script src="scene-gallery.js" defer></script>'
            if home
            else ""
        )
    )
    if documentation:
        scripts += '<script src="docs.js" defer></script>'
    (OUT / name).write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)"><meta name="theme-color" content="#111111" media="(prefers-color-scheme: dark)"><meta name="description" content="'
        + e(description, quote=True)
        + '"><title>'
        + e(page_title)
        + '</title><link rel="canonical" href="'
        + e(canonical_url, quote=True)
        + '"><meta property="og:type" content="website"><meta property="og:site_name" content="Grok Gadgets"><meta property="og:locale" content="en_US"><meta property="og:title" content="'
        + e(page_title, quote=True)
        + '"><meta property="og:description" content="'
        + e(description, quote=True)
        + '"><meta property="og:url" content="'
        + e(canonical_url, quote=True)
        + '"><meta property="og:image" content="'
        + e(share_image, quote=True)
        + '"><meta property="og:image:type" content="image/png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Large Grok Gadgets logo and name beside a conceptual wireframe hardware scene, with an oversized outline Grok Bot face in the background; open-source project, not affiliated with SpaceXSI."><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="'
        + e(page_title, quote=True)
        + '"><meta name="twitter:description" content="'
        + e(description, quote=True)
        + '"><meta name="twitter:image" content="'
        + e(share_image, quote=True)
        + '"><meta name="twitter:image:alt" content="Large Grok Gadgets logo and name beside a conceptual wireframe hardware scene, with an oversized outline Grok Bot face in the background; open-source project, not affiliated with SpaceXSI."><link rel="icon" type="image/png" href="media/grok-gadgets-icon.png"><link rel="stylesheet" href="style.css">'
        + (
            '<link rel="stylesheet" href="scene.css"><link rel="stylesheet" href="roadmap-scene.css"><link rel="stylesheet" href="signal-scene.css"><link rel="stylesheet" href="hardware-scene.css">'
            if home
            else ""
        )
        + '</head><body class="'
        + (
            "home-page"
            if home
            else "content-page documentation-page"
            if documentation
            else "content-page"
        )
        + '"'
        + (" data-donate-route" if name == "donate.html" else "")
        + (" data-playground-route" if name == "playground.html" else "")
        + '><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="identity" href="index.html" aria-label="Grok Gadgets home"><img src="media/grok-gadgets-icon.png" width="36" height="36" alt=""><span>Grok Gadgets</span></a><a class="header-contribute" href="contribute.html">Contribute ↗</a><div class="header-actions"><a id="donate-open" href="donate.html"'
        + (' aria-current="page"' if name == "donate.html" else "")
        + '>Donate</a><button id="menu-open" aria-haspopup="dialog" aria-controls="site-menu">Menu <span>[+]</span></button></div></header>'
        + menu
        + '<main id="main">'
        + body
        + "</main>"
        + (R / "website/donate.html").read_text()
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


first_success = "doc-docs-getting-started-first-success.html"
proof_section = (
    '<section class="home-proof" id="first-success" aria-labelledby="proof-heading">'
    '<p class="eyebrow">START IN MINUTES</p>'
    '<h2 id="proof-heading">Try the tools before you build.</h2>'
    '<p>Run a simulated gadget on your computer or open the <a href="playground.html">browser demo</a>. No hardware, no account.</p>'
    '<pre class="proof-output"><code>python3 -m venv .venv\n'
    ".venv/bin/python -m pip install grok-gadgets-gateway==0.1.0a18</code></pre>"
    '<p><a href="'
    + first_success
    + '">Follow the five-minute guide ↗</a> · <a href="doc-docs-public-how-we-verify.html">How we verify ↗</a></p></section>'
)

hosting_guide = '<p><a href="doc-docs-getting-started-hosting.html">Who runs the gateway? Hosting and remote access FAQ ↗</a></p>'
scene_source = R / "website/home-scene.html"
workbench = (
    '<details class="home-workbench" id="playground"><summary>Customize the virtual light <span aria-hidden="true">+</span></summary>'
    + (R / "website/playground.html")
    .read_text()
    .replace("{{SIMULATOR_BUILD}}", e(simulator_build["gateway_commit"][:8]))
    .replace("{{SIMULATOR_VERSION}}", e(simulator_build["package_version"]))
    + "</details>"
)
home_sections = (
    proof_section
    + '<section class="builder-paths" id="builder-paths" aria-labelledby="builder-heading"><p class="eyebrow">BUILD YOUR GADGET</p><h2 id="builder-heading">Make it real.</h2><p class="vision-line">Grok Bot acts on the world around you. Build a gadget once, hand it to anyone, and they just ask.</p>'
    + path_row(
        "01",
        "OLED starter kit",
        "Build the ESP32-S3 board. Hand it to anyone; they set it up from a phone.",
        "doc-docs-getting-started-repeat-the-kit.html",
        "Repeat the kit",
    )
    + path_row(
        "02",
        "No hardware",
        "Run a simulated gadget and call all six tools from your computer.",
        first_success,
        "First success",
    )
    + path_row(
        "03",
        "Raspberry Pi / Linux",
        "Turn a Pi or Linux box into a gadget with the Python SDK.",
        "linux.html",
        "Build with Linux",
    )
    + '<p class="quiet-note" id="components">Run Home Assistant? <a href="home-assistant.html">Let Grok Bot look inside ↗</a> · <a href="components.html">All components ↗</a></p></section>'
)
scene_markup = (
    scene_source.read_text() if scene_source.is_file() else "<h1>Grok Gadgets</h1>"
)
home_body = scene_markup.replace("{{PLAYGROUND_DETAILS}}", "").replace(
    "{{HOME_DETAILS}}", home_sections
)
page("index.html", "Home", home_body)
page("donate.html", "Donate", home_body)
page(
    "playground.html",
    "Playground",
    scene_markup.replace("{{PLAYGROUND_DETAILS}}", workbench).replace(
        "{{HOME_DETAILS}}", home_sections
    ),
)
page(
    "start.html",
    "Get started",
    intro(
        "Choose a path",
        "Start small.",
        "Received a gadget? Set it up, then claim it. Building for others? Start with your own relay.",
    )
    + '<div class="path-list">'
    + path_row(
        "01",
        "Set up a gadget you received",
        "You need its printed label and the builder’s running relay. Join home Wi-Fi with your phone.",
        "doc-docs-getting-started-phone-setup.html",
        "Phone setup",
    )
    + path_row(
        "02",
        "Use your gadget with Grok Bot",
        "Enter the code on its screen to claim it. Then give it a name and ask Grok Bot.",
        "doc-docs-getting-started-claim-your-gadget.html",
        "Claim guide",
    )
    + path_row(
        "03",
        "Build the tested OLED kit",
        "Parts, wiring, Wi-Fi setup and the optional always-on gateway service.",
        "doc-docs-getting-started-repeat-the-kit.html",
        "Kit guide",
    )
    + path_row(
        "04",
        "First success without hardware",
        "Install the gateway and rehearse a simulated light in five minutes.",
        first_success,
        "Gateway guide",
    )
    + path_row(
        "05",
        "Explore the simulator",
        "Customize a virtual light in the browser or download the local kit.",
        "simulator.html",
        "Try both",
    )
    + path_row(
        "06",
        "Build a Linux application",
        "Start from a reusable Python capability and agent.",
        "linux.html",
        "Linux SDK",
    )
    + path_row(
        "07",
        "Prepare gadgets for others",
        "Set up your relay, prepare a batch and check each gadget before hand-over.",
        "doc-docs-getting-started-ship-a-gadget.html",
        "Builder guide",
    )
    + path_row(
        "08",
        "Connect your home",
        "Reuse Home Assistant’s exposed Assist entities.",
        "home-assistant.html",
        "Home Assistant",
    )
    + '</div><p class="quiet-note">Report a kit test in <a href="https://github.com/adidshaft/grok-gadgets/issues/185">#185</a> or your own relay and batch in <a href="https://github.com/adidshaft/grok-gadgets/issues/269">#269</a>. <a href="doc-docs-public-support-matrix.html">Current releases and test limits ↗</a></p>'
    + hosting_guide,
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
        "playground.html",
        "Customize & try",
    )
    + path_row(
        "02",
        "On your computer",
        "Run the gateway's rehearsal command with its simulated light. No Bot account required.",
        "downloads/grok-gadgets-simulator-kit.zip",
        "Download kit",
    )
    + '<p class="quiet-note">The kit includes readable source, the wheel, locked hashed runtime dependencies, configuration schema and Apache-2.0 notices. Installation downloads the dependencies. No account connection happens automatically.</p>'
    + '<p><a href="doc-docs-getting-started-simulator-kit.html">Step-by-step setup &amp; customization ↗</a></p>'
    + '<p><a href="downloads/simulator-kit-manifest.json">Source commit, contents &amp; SHA256 hashes ↗</a></p>'
    + '<p class="status">Browser simulation only · <a href="doc-docs-public-support-matrix.html">project status ↗</a></p>'
    + proof_section
    + hosting_guide,
)
page(
    "esp32.html",
    "ESP32",
    intro(
        "Hardware / ESP32-S3",
        "One kit.<br>Start building.",
        "An ESP32-S3. A breadboard. A small OLED.",
    )
    + '<p class="status">One ESP32-S3 + OLED kit passed USB, Wi-Fi and phone setup checks · <a href="doc-docs-public-support-matrix.html">status ↗</a></p>'
    + path_row(
        "01",
        "Repeat the tested kit",
        "Parts, wiring, Wi-Fi and gateway setup, with observed results.",
        "doc-docs-getting-started-repeat-the-kit.html",
        "Kit guide",
    )
    + path_row(
        "02",
        "Make it yours",
        "Declare capabilities and handle commands.",
        "doc-docs-components-grok-gadgets-esp32-sdk-sdk.html",
        "SDK reference",
    )
    + '<p class="quiet-note">Owner-tested board: YD-ESP32-23 v1.3 with a 1.3-inch SH1106 OLED. The guide has the exact markings and wiring. <a href="https://github.com/adidshaft/grok-gadgets/issues/185">Share your result in tester issue #185 ↗</a></p>'
    + hosting_guide,
)
page(
    "linux.html",
    "Linux SDK",
    intro(
        "SDK / Linux",
        "Your code.<br>Connected.",
        "Describe a command in one line. Write the function. Run one command.",
    )
    + '<p class="status">Software tested · peripherals and systemd not yet verified · <a href="doc-docs-public-support-matrix.html">status</a></p>'
    + path_row(
        "01",
        "Quick start",
        "One install, ten lines of Python and grok-linux-agent dev. No tokens to copy.",
        "doc-docs-components-grok-gadgets-linux-sdk-README.html",
        "Quick start",
    )
    + path_row(
        "02",
        "Add commands and events",
        "The decorator API, schemas from type hints, events and shutdown hooks.",
        "doc-docs-components-grok-gadgets-linux-sdk-development.html",
        "Developer guide",
    )
    + '<p class="quiet-note"><a href="doc-docs-public-support-matrix.html">Linux verification status ↗</a></p>'
    + hosting_guide,
)
page(
    "home-assistant.html",
    "Home Assistant",
    intro(
        "Existing homes",
        "Use what<br>you already have.",
        "An integration recipe for Home Assistant’s own MCP server.",
    )
    + '<p class="status">Fixture tested · actual home and Grok Bot pending</p>'
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
    + '<p class="quiet-note">Home Assistant runs its own MCP server. Its endpoint authentication, reachability and Grok compatibility need separate verification. Entity coverage varies.</p>'
    + hosting_guide,
)
page(
    "architecture.html",
    "Architecture",
    intro(
        "How it works",
        "An action.<br>An observation.",
        "The assistant, connection point and device have separate jobs.",
    )
    + '<div class="flow"><a href="https://x.ai/bot"><img src="media/grok-mark.svg" width="40" height="40" alt="Grok"><span>Grok Bot</span><small>Run by SpaceXSI</small></a><b>↕ HTTPS sign-in or approved local command</b><span>Your gateway<small>Run by its operator</small></span><b>↕ USB / private LAN / outbound relay TLS</b><span>Your device<small>Execute and observe</small></span></div><p class="status">Requested → accepted → execution reported → physically observed</p><p><a href="doc-docs-architecture-overview.html">Architecture reference ↗</a></p><p class="quiet-note">The owner’s Grok Bot called the tools natively from Mac and iPhone through an owner-run tunnel with sign-in, and showed text on the OLED kit. Approved local commands work without a tunnel. A tunnel does not replace authentication. The gateway can run on an always-on server while the Mac sleeps. Phone setup joins the gadget to Wi-Fi without a data cable. Each person claims a gadget with the code on its screen and sees only their own gadgets. Home Assistant can use its own upstream MCP route.</p>'
    + hosting_guide,
)
roadmap_issues = [
    issue
    for issue in issues
    if issue.get("state", "open") == "open" and issue.get("stage", "ready") != "done"
]
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
    + "</p>"
    + (
        '<p><a href="'
        + e(i["github_url"], quote=True)
        + '">View issue on GitHub ↗</a></p>'
        if i.get("github_url")
        else ""
    )
    + "</article>"
    for i in roadmap_issues
)
page(
    "roadmap.html",
    "Roadmap",
    intro(
        "GitHub issue snapshot" if issue_snapshot else "Local preparation snapshot",
        "What’s next.",
        "Tested local work. Clear external gates.",
    )
    + (
        '<p class="quiet-note">Refreshed '
        + e(issue_snapshot["refreshed_at"])
        + ". GitHub Issues are authoritative; this page is a saved snapshot.</p>"
        if issue_snapshot
        else ""
    )
    + '<section class="roadmap-summary"><h2>Today, next, later.</h2><p><strong>Today:</strong> join a gadget to home Wi-Fi from a phone, with no cable, no computer and no app. Claim it with the code on its screen; your Grok Bot then sees only your gadgets, by the names you give them. Share, remove and hand over are explicit. Two people tested this on the owner’s relay and kit with their own iPhones (Phase 11).</p><p><strong>Updates:</strong> the relay operator sends signed firmware updates with no cable, and a bad image reverts by itself. Tested on the owner’s kit (Phase 12b). <a href="doc-docs-getting-started-keep-up-to-date.html">What gadget owners see ↗</a> · <a href="doc-docs-getting-started-sign-and-ship-an-update.html">Sign and ship an update ↗</a></p><p><strong>Builders:</strong> set up your own relay with one command, prepare gadgets in batches and check them in one report. Tested from the guide on a fresh host (Phase 12a). <a href="doc-docs-getting-started-ship-a-gadget.html">Ship a gadget ↗</a></p><p><strong>Next:</strong> a builder outside the project follows that guide, and the new examples run on hardware.</p><p><strong>Relays:</strong> one small relay host carried 1,000 simulated gadgets with long-poll, measured for 15 minutes on 18 October 2026. This does not establish physical gadget capacity. Phones on iPhone and Android sign in with the code on the gadget’s screen (Phase 13).</p><p><strong>Open gate:</strong> the three-day sign-in watch ends 21 October. ADR 014 acceptance and the hub release follow its result.</p><p><strong>Later:</strong> only a decision on a shared relay (Phase 14). A button press does not wake Grok Bot.</p><p><strong>Help:</strong> repeat the owner-tested kit and share results in <a href="https://github.com/adidshaft/grok-gadgets/issues/185">tester issue #185</a>.</p><p>The project hosts no relay. <a href="doc-docs-getting-started-connect-grok-bot.html">Connect your Grok Bot ↗</a> · <a href="doc-docs-getting-started-mac-free-route.html">Run the gateway away from your Mac ↗</a> · <a href="doc-docs-getting-started-phone-setup.html">Set up your gadget with your phone ↗</a> · <a href="doc-docs-getting-started-claim-your-gadget.html">Claim your gadget ↗</a> · <a href="doc-docs-public-support-matrix.html">Current releases and verification ↗</a></p></section>'
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
    + '<p class="community-help-links"><a href="doc-docs-getting-started-simulator-kit.html">Start here ↗</a> · <a href="doc-SUPPORT.html">Get help ↗</a> · <a href="doc-community-guidelines.html">Community policy ↗</a> · <a href="doc-CODE_OF_CONDUCT.html">Code of conduct ↗</a> · <a href="doc-SECURITY.html">Security ↗</a></p>'
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
    + '<p class="quiet-note">Policies live in GitHub. Reddit configuration and contributor-flair activation are separate steps.</p>',
)
page(
    "releases.html",
    "Releases",
    intro(
        "Public source · alpha releases",
        "Released alpha builds",
        "Simulation, separate SDKs, firmware builds and integration recipes.",
    )
    + '<p class="status">Alpha · one owner-tested kit · phone setup with no cable · Grok Bot on iPhone and Android through an always-on relay</p>'
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
        "Timestamped GitHub activity and its refresh state.",
        "activity.html",
        "Data state",
    ),
)
# Only explicitly selected public documents; original source identities resolve component links.
documents = Documents(R)
doc_navigation = DocsNavigation(documents)


def documentation_layout(content, current_page):
    return (
        '<div class="docs-layout"><aside class="docs-sidebar">'
        '<details class="doc-menu" open><summary>Browse documentation</summary>'
        + doc_navigation.sidebar(current_page)
        + '</details></aside><div class="docs-content">'
        + content
        + "</div></div>"
    )


for record in documents.records:
    rendered = documents.render(record)
    rendered = doc_navigation.with_toc(rendered, record)
    content = (
        doc_navigation.breadcrumbs(record["page"])
        + rendered
        + doc_navigation.related(record["page"])
        + '<p class="doc-source">Source: '
        + e(record["repository"] + "/" + record["source"])
        + "</p>"
    )
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
        documentation_layout(content, record["page"]),
    )
page("source-reference.html", "Source references", documents.reference_html())
page(
    "components.html",
    "Project components",
    documentation_layout(
        '<header class="docs-intro"><p class="eyebrow">PROJECT MAP</p><h1>Ten parts.<br>One open project.</h1><p>Choose a component and check its current evidence.</p></header>'
        + (R / "website/components.html").read_text(),
        "components.html",
    ),
)
page(
    "docs.html",
    "Documentation",
    documentation_layout(
        '<header class="docs-intro"><p class="eyebrow">Open source / Local alpha</p>'
        "<h1>Use it.<br>Build it.</h1>"
        "<p>Set up a gadget, claim it in Grok Bot, or build your own.</p>"
        '<nav class="docs-entry-paths" aria-label="Choose a path"><a href="doc-docs-getting-started-phone-setup.html">Set up a gadget ↗</a><a href="doc-docs-getting-started-claim-your-gadget.html">Claim in Grok Bot ↗</a><a href="doc-docs-getting-started-repeat-the-kit.html">Build a gadget ↗</a></nav>'
        '<p class="docs-note"><a href="doc-docs-public-support-matrix.html">Project status and open gates ↗</a></p></header>'
        + doc_navigation.index()
        + '<p class="docs-note"><a href="maintainers.html">Maintainer and process records ↗</a></p>',
        "docs.html",
    ),
)
page(
    "maintainers.html",
    "Maintainer records",
    documentation_layout(
        '<header class="docs-intro"><p class="eyebrow">For maintainers</p>'
        "<h1>Process and evidence records.</h1>"
        "<p>Release checks, dated verification records, community operations and brand "
        'sources. For what works today, see the <a href="doc-docs-public-support-matrix.html">'
        "project status</a>.</p></header>" + doc_navigation.index(maintainer=True),
        "maintainers.html",
    ),
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
    + '<p><a href="https://github.com/adidshaft/grok-gadgets">Contribute on GitHub ↗</a></p><p class="quiet-note">GitHub Issues track contributions and bugs. The roadmap shows a timestamped snapshot; a separate Project board remains pending.</p>',
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
        "Always labeled: snapshot, cached, fixture or unavailable.",
    )
    + activity_html(activity),
)
for f in [
    "style.css",
    "motion.js",
    "scene.css",
    "simulator.js",
    "scene.js",
    "donate.js",
    "docs.js",
    "roadmap-scene.js",
    "roadmap-scene.css",
    "signal-scene.js",
    "signal-scene.css",
    "scene-gallery.js",
    "hardware-scene.js",
    "hardware-scene.css",
]:
    source = R / "website" / f
    if source.is_file():
        shutil.copy(source, OUT / f)
shutil.copytree(R / "website/.well-known", OUT / ".well-known", dirs_exist_ok=True)
shutil.copytree(R / "website/media", OUT / "media", dirs_exist_ok=True)
shutil.copytree(R / "website/downloads", OUT / "downloads", dirs_exist_ok=True)
for approved_image in json.loads((R / "website/documents.json").read_text()).get(
    "images", []
):
    destination = OUT / approved_image["output"]
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(R / approved_image["source"], destination)
for output, record in documents.bundled_references.items():
    destination = OUT / output
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(R / record["source"], destination)
(OUT / "source").mkdir(exist_ok=True)
(OUT / "source/manifest.json").write_text(
    json.dumps(documents.bundled_references, indent=2) + "\n"
)


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
# Content fingerprints keep repeat visitors on the current styles and behavior.
asset_versions = {
    path.name: hashlib.sha256(path.read_bytes()).hexdigest()[:12]
    for pattern in ("*.css", "*.js")
    for path in OUT.glob(pattern)
}
for html_page in OUT.glob("*.html"):
    html_page.write_text(
        re.sub(
            r'(?:href|src)="([^"/?]+\.(?:css|js))"',
            lambda match: match.group(0)[:-1]
            + "?v="
            + asset_versions[match.group(1)]
            + '"',
            html_page.read_text(),
        )
    )
check_links(OUT)
kit_builder.verify_download(OUT / "downloads", simulator_build["gateway_inputs"])
if kit_builder.inputs() != simulator_build["build_inputs"]:
    raise ValueError(
        "Simulator kit inputs changed; run python3 scripts/build-simulator-kit.py"
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
