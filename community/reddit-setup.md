# Reddit audit and setup

On 5 October 2026 the owner asked for the subreddit to be prepared. A moderator review in Chrome recorded the before-state below. Then the description and Community Guide were updated and a welcome post was created and highlighted. The applied copy and the remaining proposals are in [the Reddit channel package](reddit-package.md). Tracking issue: `HUB-RED-001`.

## Before-state (5 October 2026)

- Community: public `r/GrokGadgets`, created 4 October 2026. No posts and no pinned post.
- Description: "An independent community for building open-source gadgets powered by Grok. Share ESP32 and Raspberry Pi projects, smart-home integrations, demos, code, and build guides. Beginners welcome—bring your questions and experiments. Not affiliated with xAI. Run by https://x.com/adidshaft"
- Rules: "Respect others and be civil" and "No spam".
- Post settings: all post types allowed; no post guidelines; post flair disabled; archiving off.
- Flairs: no post-flair or user-flair entries; member self-assignment off.
- Community Guide: enabled, generic welcome message, 0 of 3 resources.
- Sidebar: Community details and Rules widgets only.
- Appearance: branded icon and banner already set.
- Moderators: two accounts, both with full permissions. No moderator access was changed.

## Changes applied (5 October 2026)

- Replaced the description with the package wording and read it back.
- Created ["Welcome to r/GrokGadgets — start here"](https://www.reddit.com/r/GrokGadgets/comments/1wxzg00/welcome_to_rgrokgadgets_start_here/). Reddit's spam filter first hid it; the body was edited to remove direct links, and the owner moderator account then approved it. The approval persisted after reload, and Reddit's public `/new.json` listing shows the post with `removed_by: null` and `stickied: true`.
- Added the post to Community highlights (Reddit records it as stickied).
- Saved the Community Guide welcome message and the "Start here", "Try the simulator" and "Contribute" resources (3 of 3).
- No rules, flairs, moderator permissions, appearance or automation were changed.

**Correction:** the link check at the time recorded the project website as a GitHub Pages 404, so the website was left out. That was the wrong address. The site is live at <https://grok-gadgets.pages.dev/>; adding it is listed as an owner action in the package.

Future Reddit changes need specific owner authorization.

## Automation

Reddit developer platform and Data API access must be approved before a runtime is chosen. There is no browser workaround for denied API access. A static website cannot host private identity linking. Activation needs approved app and moderator scopes, private durable mapping and audit storage, a runtime and schedule, revocation monitoring, failure alerts, a deletion policy and human escalation.
