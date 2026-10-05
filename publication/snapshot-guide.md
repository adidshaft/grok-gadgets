# GitHub issue snapshots

After migration, GitHub Issues owns issue state. The migrated local ledgers and mapping remain archival records; change issue state or its explicit Status field on GitHub. The Cloudflare deployment workflow reads and validates a full five-repository issue snapshot before each production deployment. It also refreshes once daily at 06:17 UTC to capture issue changes and cross-repository activity such as star counts. The deployment artifact is built with these snapshots; the visitor's browser makes no GitHub API requests.

From the hub, explicitly refresh using the existing gh authentication:

~~~sh
.venv/bin/python scripts/refresh-github-snapshot.py
~~~

The command makes GET requests only, fully paginates open and closed issues in all five approved adidshaft repositories, and excludes pull requests. It does not require push access or edit issues. Scheduled refreshes use the Actions-provided read-only token and keep the refreshed file only in the build workspace; they do not commit data-only snapshots to `main`. To refresh locally, review and commit `publication/github-issues.json` only as an ordinary source change.

The snapshot records a UTC `refreshed_at` timestamp, GitHub issue URLs, titles, labels, milestone titles and derived stages. A valid first-line migration marker retains its local ID. New unmarked contributions use repository#number and need no local-ledger entry. Closed issues are done regardless of historical body status; open issues use a recognized explicit Status field or proposed. An open issue whose body says done is proposed. Quoted/fenced examples and ambiguous status fields do not determine progress.

Only a short explicit Blocker or Blocked by section is retained for blocked issues. Unsafe contact/path/credential text, private endpoint URLs and oversized sections are omitted. Raw issue bodies, API responses and credentials are not saved in the snapshot or printed. Inspect the linked GitHub issue for full context.

Any page, repository, marker, identity or URL validation failure leaves the previous file intact. A complete five-repository result is validated before an atomic replacement; a failed replacement also preserves the old file. There is no partial-repository fallback or automatic retry.

To check the committed file without authentication or network access:

~~~sh
.venv/bin/python scripts/refresh-github-snapshot.py --check
.venv/bin/python -m unittest discover -s scripts -p test_github_snapshot.py -v
~~~

Missing or invalid snapshots fail the offline loader. The refresh time describes when GitHub was read, not when tests ran, a device was observed or native Grok invoked a tool. If the scheduled issue read or validation fails, deployment is withheld and the previous site remains available. Activity refresh failures are explicitly labeled as cached or unavailable; live activity older than one hour is displayed as cached.
