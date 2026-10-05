# Opt-in contribution recognition

**Status:** The local decision engine works with test data. It has no live account verification service or Reddit adapter. It does not award live flair.

## Contributor eligibility

The person must request recognition. Then complete these checks:

1. Verify ownership of both the GitHub account and the Reddit account.
2. Use an approved verification process. Alternatively, put a unique challenge on both accounts and have a human check it. The challenge must expire.
3. Link the immutable account IDs. Do not match accounts by username.
4. Verify a merged code, documentation, or test contribution to one of the five project repositories.

An issue or an unmerged pull request does not qualify. Maintainer and moderator flairs take priority over contributor flair.

Ordinary participation does not give a person the Contributor or Maintainer role. Verify eligibility before you assign either role.

## Hardware tester eligibility

The person must opt in and submit a test report. The report must identify the exact board, firmware, and host. It must include physical LED and button observations and recovery evidence. A maintainer must review it.

## Test the decision engine

Run:

```sh
python3 community/automation/recognition.py community/automation/fixtures.json
```

The command uses synthetic data and gives redacted dry-run decisions. It does not verify real accounts.

Verified fields must come from trusted operations. Do not accept a user's assertion as verification.

The engine fails closed:

- Consent, ownership proofs and merges count only when the value is exactly `true`. Text such as `"false"` or `"yes"` does not count.
- GitHub IDs must be numeric user IDs. Reddit IDs must be `t2_` account IDs. Repositories must be `adidshaft/<name>`.
- Bot accounts and automation pull requests never qualify.
- Any existing flair other than Contributor is preserved. A manual override of `deny` (any case) blocks the award; any other override goes to review.
- One GitHub account links to one Reddit account. A second link goes to review. Awards are keyed per Reddit account.
- Revoked consent after an award gives a `would_remove` decision.
- The dry-run log shows a timestamp, outcome, reason and short hashes only. It never shows account IDs or proofs.

## Requirements before activation

Complete a separate review before live use. The service must validate signatures and proofs. It must reject expired or reused proofs. Use encrypted storage and access controls.

For each award:

- Use a stable idempotency key to prevent duplicate awards.
- Limit the number of attempts.
- Check the current result before a retry if the previous result is uncertain.
- Handle revoked permissions and manual denial.
- Verify ownership again if an account changes.
- Save a durable success record only after the API confirms success.

Keep account links and proofs private and outside Git.

## Remove an account link

When a person unlinks an account:

1. Revoke consent for recognition.
2. Stop future access.
3. Delete the account link and proof data within 30 days.
4. Offer a review to correct or remove recognition.

Keep only the minimum audit statistics. These statistics must not identify a person.
