# Draft reply — Linux SDK PR #58 (not posted)

Status: draft for the owner. Post only after the owner's yes.
Target: https://github.com/adidshaft/grok-gadgets-linux-sdk/pull/58

---

Thanks again for the Pi 5 report. Releases have moved on since my 17 October note, so here is the current request in one place.

Please repeat the software checks on Linux SDK `v0.1.0-alpha.9` (`0.1.0a9` on PyPI) and gateway `v0.1.0-alpha.17` (`0.1.0a17`). The request is otherwise unchanged:

- Keep the original alpha.2 report as dated evidence. Add the new run as a separate section with package versions, Pi OS release, exact commands, the stop and reconnect steps, and redacted results.
- Keep three results apart: **Software** (install, simulated lamp, reconnect); **Grok Bot** (operator-reported until a redacted request log shows the calls: time, tool, outcome only); and physical LED/button (**Not tested** unless you wire one).
- New in alpha.9, optional: the agent can reach a relay over TLS (`--gateway`, `--ca`, `--device-id`). A loopback run is enough for this PR. Please do not open a public endpoint for it.

No tokens, authorization headers, client names or private hostnames, please. If you no longer have time for a re-run, say so and we will review the alpha.2 report as it stands, with the Grok Bot row marked operator-reported. Thanks!
