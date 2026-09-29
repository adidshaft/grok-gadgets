# Reddit platform evaluation — 4 October 2026

Reviewed official [Devvit Reddit API](https://developers.reddit.com/docs/capabilities/server/reddit-api): enabling the Reddit permission supplies app authentication; private user data is restricted. Reviewed [HTTP Fetch](https://developers.reddit.com/docs/capabilities/server/http-fetch): exact external domains require per-app approval; HTTPS only, server fetch timeout bounded, client fetch limited to own API routes. Apps using fetch require public terms and privacy documents. Server endpoints still need permission checks.

Reviewed [Data API guidance](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki): registered OAuth, access request, descriptive User-Agent, rate headers, and deletion handling are required. Deleted-account identifying records must be removed; the docs recommend refreshing/removing stored data within 48 hours. Re-check applicable rules before launch.

Decision: keep local recognition engine runtime-neutral and inactive. Devvit may support approved moderator capabilities, but external GitHub proof fetch and account-link backend permissions require validation. A separately approved conventional OAuth service is another candidate. Do not claim unrestricted unattended awards, install an app, or bypass denied access via browser automation. No live network API is implemented here.
