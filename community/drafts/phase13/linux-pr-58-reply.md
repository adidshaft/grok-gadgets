# Draft reply — Linux SDK PR #58 (not posted)

Status: draft for the owner, refreshed 24 October 2026. Post one option only after the owner's yes.
Target: https://github.com/adidshaft/grok-gadgets-linux-sdk/pull/58

Context: the PR has had no reply since 8 October. Five follow-ups (9, 12, 13, 14 and 17 October)
each asked for the same changes on newer releases.

## Option A: refresh the request

---

Thanks again for the Pi 5 report. Releases have moved on since my 17 October note, so here is the current request in one place.

Please repeat the software checks on Linux SDK `v0.1.0-alpha.10` (`0.1.0a10` on PyPI) and gateway `v0.1.0-alpha.20` (`0.1.0a20`). The request is otherwise unchanged:

- Keep the original alpha.2 report as dated evidence. Add the new run as a separate section with package versions, Pi OS release, exact commands, the stop and reconnect steps, and redacted results.
- Keep three results apart: **Software** (install, simulated lamp, reconnect); **Grok Bot** (operator-reported until a redacted request log shows the calls: time, tool, outcome only); and physical LED/button (**Not tested** unless you wire one).
- Optional: the agent can reach a relay over TLS (`--gateway`, `--ca`, `--device-id`). A loopback run is enough for this PR. Please do not open a public endpoint for it.

No tokens, authorization headers, client names or private hostnames, please. If you no longer have time for a re-run, say so and we will review the alpha.2 report as it stands, with the Grok Bot row marked operator-reported. Thanks!

---

## Option B: close with thanks

---

Thanks for testing on a real Pi 5 and writing it up. We have not heard back since 8 October, so I am closing this PR to keep the queue current. Nothing is lost: the branch and this discussion stay here.

If you want to pick it up again, reopen this PR or open a new one against `dev` with a run on the current releases (Linux SDK `v0.1.0-alpha.10`, gateway `v0.1.0-alpha.20`), keeping the alpha.2 report as dated evidence and the Grok Bot row marked operator-reported unless a redacted request log shows the calls. Hub issue [#15](https://github.com/adidshaft/grok-gadgets/issues/15) stays open for a hardware report.

---
