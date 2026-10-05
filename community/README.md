# Community

GitHub is the source for community policies and technical records. Reddit links to these files.

The 5 October 2026 audit confirmed a Reddit description, icon, banner, pinned welcome post, and community guide. Post flairs and user flairs were not configured. Automatic contributor recognition was not active.

## Find a policy

| File | Use |
| --- | --- |
| [Community guidelines](guidelines.md) | Learn how to participate and report evidence. |
| [Reddit setup](reddit-setup.md) | Review the setup proposal. Check each item against the live settings. |
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
