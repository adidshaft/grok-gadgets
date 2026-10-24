# Builder call (draft, not posted)

**Status:** draft for the owner. It replaces [second-builder-call.md](../second-builder-call.md).
Post it only with the owner's yes, as a comment on
[#269](https://github.com/adidshaft/grok-gadgets/issues/269).

---

## Build a gadget for Grok Bot: be our first outside builder

We need one person outside the project to follow the builder guide on their own host and
tell us where it breaks.

**Current releases:** gateway `0.1.0a21`, ESP32 SDK `v0.2.0-alpha.19`, Linux SDK `0.1.0a10`.
Check the [project status](https://github.com/adidshaft/grok-gadgets/blob/main/docs/public/support-matrix.md)
before you start; it says what was tested and what was not.

**What you do (about one afternoon):**

1. Follow [Ship a gadget in one afternoon](https://grokgadgets.org/doc-docs-getting-started-ship-a-gadget).
2. Set up your own relay on a small Linux host with `relay init`, then prepare one or more
   gadgets: an ESP32-S3 board or a Linux machine.
3. Hand one gadget to someone with Grok Bot, or use it yourself. They claim it with the code
   on its screen.
4. Post the [report template](https://github.com/adidshaft/grok-gadgets/blob/main/community/drafts/phase13/report-template.md)
   here: each step that worked, each that did not, and how long it took.

**How big a relay gets:** on 18 October 2026 one 512 MB, 1-vCPU host carried 200 simulated
gadgets polling every 100 ms (about 61 % CPU) and 1,000 with long-poll (about 67 % CPU,
137 MB). Those are measurements of one host, not guarantees
([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ready-for-others-2026-10-18.md)).
A relay holds 64 gadgets
by default; `serve --max-devices` raises it. Credits per account are optional and off by
default; they measure use and involve no payments
([Credits on your relay](https://grokgadgets.org/doc-docs-getting-started-credits-on-your-relay)).

**What you need:** a small Linux host, a domain you control, Grok Bot, and an ESP32-S3 board
with a part or a Linux machine. Hardware and hosting are yours; the project pays for nothing.
Windows is not tested.

**What we do:** we answer within a working day and fix the guide where it failed you. Your
report goes into the verification records under your GitHub name only if you agree.

**What this is not:** a product, a service or a sale. The project runs no relay for you.
Read [Before you distribute a gadget](https://grokgadgets.org/doc-docs-getting-started-before-you-distribute)
before you give a gadget to anyone. Security problems go privately to
adidshaft@kyokasuigetsu.xyz.
