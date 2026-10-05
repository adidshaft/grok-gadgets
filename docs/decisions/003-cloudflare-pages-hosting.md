# ADR 003 — Cloudflare Pages with checks-gated GitHub deployments

**Date:** 5 October 2026  
**Status:** Accepted for the public static website  
**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)

## Decision

Host the static documentation and project site on Cloudflare Pages using the free `pages.dev` hostname `https://grok-gadgets.pages.dev/` until the owner selects and purchases a custom domain. Do not enable a paid Cloudflare plan, buy a domain, or put the persistent gadget gateway on Pages.

Use Cloudflare Pages Direct Upload from GitHub Actions rather than Cloudflare's GitHub App integration. The existing protected GitHub main branch and CI remain the source of truth. After a main commit's `Hub checks` and `Integrated acceptance` workflows succeed for the same SHA, the deployment workflow builds that exact commit and deploys only `website/dist`. It never exposes the Cloudflare token to pull-request or build jobs. The token is scoped to Cloudflare Pages edit access for the project account and stored in the `cloudflare-pages-production` GitHub environment.

The static build reads the five public GitHub repositories through bounded API refreshes. Successful website deployments refresh a complete issue snapshot and repository activity. A scheduled run refreshes those snapshots daily at 06:17 UTC (11:47 India time), including star counts which have no reliable event notification path. If the issue export fails, the new build stops and the last successful site remains deployed. If the activity API fails, the page labels the timestamped fallback as cached or unavailable. The site never fetches the API from visitors' browsers and includes no GitHub token.

This process updates issue state and activity data separately from the pinned compatibility manifest. A component repository changing does not silently upgrade the tested protocol or documentation pins. Activity may reflect newer source activity while runtime compatibility remains pinned to an explicitly tested version.

## Security and operational boundaries

- The free static host contains no device credentials, user account data, persistent device service, or Grok backend.
- GitHub Actions uses its automatic read-only repository token for public issue/activity API requests.
- The Cloudflare Pages API token is only available to the production deployment job and is stored as an environment secret.
- Deploy only the artifact that passed the per-SHA workflow gate, content snapshot validation, simulator-kit verification, website tests, and URL-prefix/deep-link check.
- Failed refreshes or builds leave the current deployment untouched. Revert a reviewed main commit and let the same checks-gated workflow deploy the prior source if rollback is needed.
- Do not configure direct Git pushes from Cloudflare; avoid duplicate/racing deployments and the broader Cloudflare GitHub App permission set.

## Evidence required

This decision is implemented locally before activation. It becomes operational only when the Pages project, account-scoped token, protected GitHub environment secret, first deployment, and a successful main-triggered update are verified. After the first deploy, read back the canonical URL and metadata, check HTTPS, deep routes, navigation, responsive behavior, current issue/activity timestamp and the downloaded simulator archive's SHA-256. Update repository homepage links only after those checks pass.
