# Reddit channel package

This is the copy that was applied to r/GrokGadgets on 5 October 2026, plus proposals that are not applied yet. The audit trail is in [reddit-setup.md](reddit-setup.md). Tracking issue: `HUB-RED-001`.

## Owner action needed

When the package was applied, the website was wrongly recorded as unavailable, so Reddit links only to GitHub. The site is live at <https://grok-gadgets.pages.dev/>. Add it as a Community Guide resource and in the welcome post when you next edit the subreddit:

| Label | Destination |
| --- | --- |
| Website and simulator | `https://grok-gadgets.pages.dev/` |

## Community description (applied)

Independent open-source tools and SDKs for connecting devices to Grok. Explore the Linux and ESP32 SDKs, Home Assistant setup, or start with the software simulator. Experimental alpha; native Grok and physical-device verification remain in progress. Unaffiliated with xAI, M5Stack, and Home Assistant.

Optional longer wording for a sidebar widget:

> Grok Gadgets is an independent, open-source project for connecting devices to Grok. Try the browser simulator, build with the Linux or ESP32 SDK, or explore the Home Assistant setup. This is an experimental alpha: local software and simulator paths have been tested, while native Grok invocation, mobile behavior, and physical hardware remain unverified. Keep credentials and private household data out of posts.

## Community Guide welcome message (applied)

> Welcome {username}! Start with the pinned post and the simulator — no hardware needed. Alpha: simulations and builds don't prove Grok or hardware operation. Keep credentials and household details private.

## Welcome post (applied, approved and stickied)

**Title:** Welcome to r/GrokGadgets — start here

**Body:**

Welcome! Grok Gadgets is an independent open-source project exploring ways to connect devices to Grok.

Start with the browser simulator; it does not call Grok or control a physical device. Find the project hub, simulator guide, and contribution links in the Community Guide.

This is an experimental alpha. Actual Grok invocation and physical-device operation remain unverified. Keep credentials, tokens, private logs, and household details out of posts.

Not affiliated with xAI, M5Stack, or Home Assistant.

## Community Guide resources (applied, 3 of 3)

| Label | Destination |
| --- | --- |
| Start here | `https://github.com/adidshaft/grok-gadgets` |
| Try the simulator | `https://github.com/adidshaft/grok-gadgets/blob/main/docs/getting-started/simulator-kit.md` |
| Contribute | `https://github.com/adidshaft/grok-gadgets/blob/main/docs/contributing/ready-issues.md` |

## Proposed menu or sidebar links

| Label | Destination |
| --- | --- |
| Website | `https://grok-gadgets.pages.dev/` |
| Start here | `https://github.com/adidshaft/grok-gadgets` |
| Roadmap | `https://github.com/adidshaft/grok-gadgets/blob/main/ROADMAP.md` |
| Contribute | `https://github.com/adidshaft/grok-gadgets/blob/main/CONTRIBUTING.md` |
| Security | `https://github.com/adidshaft/grok-gadgets/blob/main/SECURITY.md` |

## Proposed post flairs

Start with **Help**, **Build**, **Guide**, **Release** and **Announcement**. Keep flair optional until there are enough posts to need it. Post flair is currently disabled with no entries.

Role flairs such as **Contributor**, **Maintainer** and **Hardware tester** stay moderator-assigned and evidence-backed; see [contribution recognition](contribution-recognition.md). User flair currently has no entries and members cannot self-assign.

## Proposed rules

Keep the two existing rules ("Respect others and be civil" and "No spam") and review these additions together:

1. Keep posts relevant to Grok-connected gadgets, the project, and compatible maker work.
2. Be respectful and help beginners; critique ideas and evidence without attacking people.
3. Label evidence accurately. Simulated, compiled, actual Grok, and physical-device results are different claims.
4. Never post credentials, tokens, personal data, private logs, or identifying smart-home details.
5. Share reproducible builds and troubleshooting steps; redact logs before posting.
6. No spam, scams, or unsolicited promotion. Disclose relevant affiliations and commercial interests.

## Checklist

- [x] All five GitHub repositories are public on `main`.
- [x] Description, Community Guide welcome message and three resources applied and read back.
- [x] Welcome post created, approved, highlighted and visible in the public feed.
- [ ] Add the website link (owner action above).
- [ ] Apply the proposed rules, flairs and menu links only when they are needed.
