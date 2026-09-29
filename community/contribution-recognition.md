# Opt-in contribution recognition

Request recognition explicitly. Verify ownership of GitHub and Reddit via an approved identity flow or unique, expiring challenge placed on both accounts and human verification. Bind immutable account IDs, never matching usernames. Verify a merged code, documentation, or test contribution to one of the five repositories. Opening an issue or unmerged PR is insufficient. Maintainer and moderator flairs take priority.

`python3 community/automation/recognition.py community/automation/fixtures.json` produces redacted dry-run decisions. Fixtures are synthetic. This decision engine has no live identity backend or Reddit adapter. Verified fields are trusted operational inputs, not user assertions; production needs signature/proof validation, expiry, replay protection, encrypted storage, access controls, and a separate review.

Awards use a stable idempotency key, bounded attempts, query-before-retry after uncertain outcomes, permission-revocation handling, manual denial, and changed-account re-verification. Successful outcomes must be durably recorded only after API confirmation. Account mappings remain private and outside Git. On unlink, revoke recognition consent, stop future access, delete mapping/proof data within 30 days, and offer a correction/removal review. Preserve only minimal nonidentifying audit statistics. No awards or live changes occur in this local phase.

Hardware tester eligibility: an opt-in test report identifying exact board/firmware/host, physical LED/button observations and recovery evidence reviewed by a maintainer. Contributor/Maintainer eligibility is verified; ordinary participation does not confer these roles.
