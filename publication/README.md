# Publication records

These files support the live website and the hosted checks. The website is live at [grok-gadgets.pages.dev](https://grok-gadgets.pages.dev/).

| File | Used by |
| --- | --- |
| `github-issues.json` | Issue snapshot for the website roadmap. `scripts/refresh-github-snapshot.py` writes it; `website/build.py` reads it. See the [snapshot guide](snapshot-guide.md). |
| `github-activity.json` | Cached activity for the website. The Pages workflow refreshes it. |
| `action-pins.json` | Verified GitHub Action pins. `scripts/test_launch.py` checks every workflow against it. |
| `repositories.json`, `rulesets/` | Repository and branch-rule records. `scripts/test_launch.py` checks that the rules keep history and let the maintainer merge. |
| `labels.json`, `milestones.json` | Label and milestone definitions read by `scripts/issue_migration.py`. |
| `project.json` | Planned GitHub Project fields, listed as a website source reference. |
| [`website-deployment.md`](website-deployment.md) | How the Cloudflare Pages deployment works. |

The first-launch packaging, audit and issue-migration tools and their records are in [`archive/`](../archive/README.md). Nothing runs them now.
