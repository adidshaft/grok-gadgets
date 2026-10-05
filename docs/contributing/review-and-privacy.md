# Review and privacy

Anyone can propose a contribution. A maintainer reviews it before merge. Open source does not require publishing credentials, personal information or household data.

## Choose the channel

| Need | Channel |
| --- | --- |
| Bug, feature or documentation change | Issue in the owning repository |
| Code or documentation contribution | Focused pull request linked to its issue |
| Questions and community examples | r/GrokGadgets; link actionable work to GitHub |
| Security vulnerability or leaked credential | GitHub private vulnerability reporting or SECURITY.md contact |
| Private conduct report | adidshaft@kyokasuigetsu.xyz |

## Review before merge

1. Check the change and its dependencies. Give workflow, installer and network changes extra review.
2. Run the owning repository's required checks. Add meaningful regression coverage for changed behavior.
3. Check docs, compatibility and evidence claims. Compilation is not a hardware test.
4. Review the staged files, generated artifacts, logs and commit identity for private information.
5. Merge through normal branch protections. Do not bypass failed checks for convenience.

Do not run untrusted contributor code on a maintainer computer with credentials or home-device access. Use isolated CI without deployment secrets. Never use a privileged PR workflow to execute unreviewed fork code. Review workflow and dependency changes before approving a run.

Current PR checks use read-only repository permissions and disable persisted checkout credentials. Deployment credentials belong to the main-restricted production environment. Keep fork checks separate from production deployment. These controls reduce risk; they do not replace code review.

## Keep private data private

Keep credentials in approved secret storage or ignored local configuration. Use dummy values in examples. Keep `.gitignore` current. Ignore rules do not remove already tracked files or past commits. GitHub secret scanning and push protection are enabled, but cannot detect every confidential value.

Check screenshots and logs for tokens, account details, household names and device addresses before sharing. Use a public or GitHub noreply commit email. Never merge the private recovery checkout into public history.

If a credential leaks, revoke or rotate it first and report privately. Removing a file is not proof that all public copies were erased. Do not paste the credential into an issue or PR.

## Track work without duplicate records

GitHub Issues are the source of truth. Use labels, milestones and linked PRs. A GitHub Project can provide a cross-repository view with Todo, In progress, Blocked and Done; it must reference those issues rather than duplicate their descriptions. Activation remains pending verification and separate authorization. Do not claim the board exists until its URL and access are verified.

Dependency vulnerability scanning is a known coverage gap. Keep it on the roadmap; green functional tests alone do not establish dependency security.
