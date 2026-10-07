# Static website deployment — Cloudflare Pages

The live destination is the free Cloudflare Pages hostname `https://grok-gadgets.pages.dev/`. No custom domain is selected or purchased. The deployment method is Cloudflare Pages Direct Upload from `.github/workflows/pages.yml`; do not connect the repo with Cloudflare's GitHub App or enable a competing Pages deployment.

On a successful `Integrated acceptance` run for `main`, the workflow verifies that `Hub checks` also passed on the identical commit, refreshes the complete public issue/activity snapshots, rebuilds the source-driven site, checks pages, internal/deep links, the tested simulator kit and its checksum, then deploys the exact output. The build checks out gateway `main` and rebuilds the kit from it whenever the gateway files the kit is made from have changed (from 6 October 2026), so the download always matches gateway `main`. A daily scheduled run refreshes cross-repository metadata, including star counts. PRs and arbitrary branches never receive the Cloudflare secret. Only the protected `cloudflare-pages-production` environment deployment job uses the account-scoped Pages token.

Cloudflare Pages project `grok-gadgets`, its one-year Pages Edit token, and the `main`-restricted GitHub environment are active. First production deployment `589fab44-972e-47d6-a02b-05cf12a0576c` was deployed from main `925d4b6e362f30202d1072ebfecd9d52fc49637e`; its build also passed on that exact SHA. Live HTTPS routes `/`, `/start`, `/architecture`, and `/activity` returned 200. That hosted simulator archive matched SHA-256 `47f58e94ea6e3c8b6fd3acec1bd0fb4cc84597c3c8d7e28ac49b2bad08c3e894`. Later `main` kit rebuilds are recorded in `website/downloads/simulator-kit-manifest.json`. All five GitHub repository About homepage fields now point to the verified Pages URL. Failed builds or incomplete issue snapshots keep the prior live version. The site remains static and does not run the gateway, Grok connector, identity backend, or Reddit automation.

## Newer production always wins

Every deployment run shares one concurrency group, `cloudflare-pages-production`. Runs never overlap. A newer queued run replaces an older queued run. A started run is not cancelled.

Just before upload, `.github/deploy/check-current-main.sh` compares the run's commit with current `main`. If `main` has moved on, the run skips the upload and the newer run deploys. This covers an older run that finishes late and a rerun of an old run. If GitHub cannot report `main`, the job fails and nothing is deployed. The exact-commit check gates and the protected environment are unchanged.

## Intentional rollback

A rerun of an old workflow run no longer rolls back production, because that commit is not current `main`. Roll back on purpose instead:

1. Open a `hotfix/<ISSUE-ID>-revert-<slug>` PR into `main` that reverts the bad change. Merge it after the checks pass. The normal workflow then deploys the reverted `main`. Sync `dev` as the hotfix policy in CONTRIBUTING.md describes.
2. In an emergency, the maintainer can promote an earlier deployment in the Cloudflare Pages dashboard. This is temporary: the next run deploys current `main` again, at the latest with the daily refresh at 06:17 UTC. Land the revert on `main` before then.
