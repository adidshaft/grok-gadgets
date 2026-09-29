# Static website deployment proposal — not activated

After GitHub owner/repository approval, enable GitHub Pages Actions for the hub only. Build from main with Python, run hub/website/community checks, upload website/dist, and deploy under contents:read/pages:write/id-token:write permissions with a protected pages environment. No tokens belong in frontend JavaScript. Initial activity remains unavailable; only an approved server-side refresh job may fetch GitHub metadata.

Refresh at most hourly, bounded pagination/timeouts, exclude PRs from issue counts, deduplicate numeric contributor IDs, active=eligible merged PR in last 90 days excluding identifiable bots, label aggregate stars as summed per-repository stars. On failed refresh show last-success timestamp and cached state or unavailable. Validate untrusted content and escape output. Canonical docs and roadmap rebuild with approved source changes. Domain choice is deferred; no purchase is needed.

Pages serves static assets only. It does not provide Grok gateway process, persistent sessions, private account linking, or hardware connectivity. Deployment cannot close those product gates.
