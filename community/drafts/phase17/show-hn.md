# Show HN. Draft only (27 Oct 2026)

**Title** (80 characters max):

Show HN: Grok Gadgets, open-source hardware your Grok Bot can control

**URL:** https://github.com/adidshaft/grok-gadgets

**First comment** (post right after submitting):

---

Hi HN. Grok Gadgets is an open-source gateway and SDKs that let Grok Bot control small devices through MCP tools. The tested path is an ESP32-S3 with a 1.3-inch OLED: it joins home Wi-Fi from a phone with no cable, you claim it with the code on its screen, and from then on your Grok Bot sees only your gadgets.

What exists today, all tested on my own setup only:

- A gateway that runs on a small Linux relay. Grok Bot reaches it through a tunnel with OAuth sign-in; gadgets connect over TLS with per-device tokens.
- Accounts with claim codes, sharing and hand-over; signed firmware updates over the relay with automatic revert; nightly config backups with a tested restore.
- A Linux SDK (Python) and a simulator, so you can try the six tools without hardware.

What is not tested: anyone but me. It is one kit, one relay and my own phones. Windows is untested, and a 1,000-gadget load test was simulated, not physical.

That is why I'm posting. I'm looking for one person to repeat the kit from the guide and one to run their own relay and ship a gadget. Failed runs are as useful as passes:

- Tester call: https://github.com/adidshaft/grok-gadgets/issues/185
- Builder call: https://github.com/adidshaft/grok-gadgets/issues/269

The project runs no service and sells nothing. Apache-2.0. Happy to answer anything about the protocol, the relay or the sign-in flow.

---
