#!/usr/bin/env bash
# Deploy only the revision that is main right now. An older run that finishes late,
# or a rerun of an old run, must not replace newer production. Rollback is a separate,
# deliberate procedure: publication/website-deployment.md.
# Usage: check-current-main.sh OWNER/REPO DEPLOY_SHA   (writes current=true|false)
set -euo pipefail
repo=$1
deploy_sha=$2
main_sha=$(gh api "repos/$repo/commits/main" --jq .sha)
if ! [[ $main_sha =~ ^[0-9a-f]{40}$ ]]; then
  echo "Could not read the current main commit; no deployment was made." >&2
  exit 1
fi
if [ "$main_sha" = "$deploy_sha" ]; then
  echo "$deploy_sha is current main; deploying."
  echo "current=true" >> "${GITHUB_OUTPUT:-/dev/null}"
else
  echo "::notice::Skipped: $deploy_sha is no longer main ($main_sha is). The newer run deploys."
  echo "current=false" >> "${GITHUB_OUTPUT:-/dev/null}"
fi
