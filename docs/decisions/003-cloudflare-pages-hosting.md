# ADR 003 — Cloudflare Pages with checks-gated GitHub deployments

**Date:** 5 October 2026  
**Status:** Accepted for the public static website  
**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)

## Decision

Host the static documentation and project site on Cloudflare Pages using the free `pages.dev` hostname `https://grok-gadgets.pages.dev/` until the owner selects and purchases a custom domain. Do not enable a paid Cloudflare plan, buy a domain, or put the persistent gadget gateway on Pages.

This decision covers the website only. Gateway and tunnel operators have separate responsibilities. The [hosting FAQ](../getting-started/hosting.md) records them and the unimplemented remote MCP security work.

Use Cloudflare Pages Direct Upload from GitHub Actions rather than Cloudflare's GitHub App integration. The existing protected GitHub main branch and CI remain the source of truth. After a main commit's `Hub checks` and `Integrated acceptance` workflows succeed for the same SHA, the deployment workflow builds that exact commit and deploys only `website/dist`. It never exposes the Cloudflare token to pull-request or build jobs. The token is scoped to Cloudflare Pages edit access for the project account and stored in the `cloudflare-pages-production` GitHub environment.

The static build reads the five public GitHub repositories through bounded API refreshes. Successful website deployments refresh a complete issue snapshot and repository activity. A scheduled run refreshes those snapshots daily at 06:17 UTC (11:47 India time), including star counts which have no reliable event notification path. If the issue export fails, the new build stops and the last successful site remains deployed. If the activity API fails, the page labels the timestamped fallback as cached or unavailable. The site never fetches the API from visitors' browsers and includes no GitHub token.

This process updates issue state and activity data separately from the pinned compatibility manifest. A component repository changing does not silently upgrade the tested protocol or documentation pins. Activity may reflect newer source activity while runtime compatibility remains pinned to an explicitly tested version.

## Custom domain — 7 October 2026

The owner purchased `grokgadgets.org` in Cloudflare and authorized connecting it to the existing Pages project. Use `https://grokgadgets.org/` as the canonical site root for page metadata, share images, sitemap and current website links. Keep the original `grok-gadgets.pages.dev` hostname available. The Pages deployment project and checks-gated workflow remain the same. Custom-domain activation and certificate delivery are separate Cloudflare setup steps; the deployment token still requires no DNS permissions.

## Security and operational boundaries

- The free static host contains no device credentials, user account data, persistent device service, or Grok backend.
- GitHub Actions uses its automatic read-only repository token for public issue/activity API requests.
- The one-year Cloudflare Pages API token grants account-level Pages edit access across the account's Pages projects; it has no DNS or zone permissions. It is only available to the production deployment job and is stored as an environment secret in `cloudflare-pages-production`, restricted to `main` with administrator bypass disabled.
- Deploy only the artifact that passed the per-SHA workflow gate, content snapshot validation, simulator-kit verification, website tests, and URL-prefix/deep-link check.
- Failed refreshes or builds leave the current deployment untouched. Revert a reviewed main commit and let the same checks-gated workflow deploy the prior source if rollback is needed.
- Do not configure direct Git pushes from Cloudflare; avoid duplicate/racing deployments and the broader Cloudflare GitHub App permission set.

## Evidence required

The Pages project, account-owned one-year token, `main`-restricted GitHub environment secrets, and first main-triggered deployment were verified on 5 October 2026. Deployment `589fab44-972e-47d6-a02b-05cf12a0576c` published main SHA `925d4b6e362f30202d1072ebfecd9d52fc49637e`. The canonical host, HTTPS routes `/`, `/start`, `/architecture`, and `/activity`, live activity timestamp, and simulator archive checksum were verified. The live Pages URL is recorded in all five repository About fields. The GitHub repository homepage metadata was read back after those checks passed.
