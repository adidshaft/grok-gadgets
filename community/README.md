# Community

GitHub is the source for community policies and technical records. Reddit links to these files.

On 5 October 2026 the subreddit description, Community Guide and a pinned welcome post were set up. Post flairs and user flairs are not configured. Automatic contributor recognition is not active.

Start with the [simulator setup](../docs/getting-started/simulator-kit.md). For help, use
[support](../SUPPORT.md), [community guidelines](guidelines.md),
[code of conduct](../CODE_OF_CONDUCT.md), and [security reporting](../SECURITY.md).

## Find a policy

| File | Use |
| --- | --- |
| [Community guidelines](guidelines.md) | Learn how to participate and report evidence. |
| [Reddit setup](reddit-setup.md) | See what was changed on Reddit and what it looked like before. |
| [Reddit channel package](reddit-package.md) | Copy-paste text for the subreddit, plus proposed rules and flairs. |
| [Contribution recognition](contribution-recognition.md) | Review opt-in account verification and private data requirements. |
| [Moderation policy](moderation-policy.md) | Check which actions need human authorization. |
| [Post drafts](drafts/initial-posts.md) | Review proposed community posts. |

## Future automation

Before activation, define where the service will run. Get separate approval for its schedule and credentials.

This applies to issue review, link checks, release drafts, contributor recognition, question routing, and moderation escalation. A chat plan does not start a service. No recurring community task is active.

## Run local checks

```sh
python3 -m unittest discover -s community/tests
python3 community/automation/recognition.py community/automation/fixtures.json
```
