# LinkedIn post, credits per account on a relay. Draft only (20 Oct 2026)

Attach: credits-demo-side-by-side-v2.mp4

---

Grok Gadgets can now be shared with other people on credits.

Grok Gadgets is an open-source project that lets Grok Bot control small hardware devices, such as an ESP32-S3 with an OLED display. A relay server connects the gadgets to Grok Bot. Until now, one question was open: when several people use the same relay, who uses how much, and who pays for it?

This release answers the first half without touching money.

What it means
The relay operator gives each person a credit balance. A command costs 1 credit. Each day a person's gadget is online costs 1 credit. Reading a gadget's state is free. The operator's own account is never charged.

How we tested it
I shared my kit with a second person and granted them 5 credits. They sent five messages from their own Grok Bot, and each one appeared on the display. The sixth was refused, and Grok Bot told them plainly: "Your credits on this relay are used up; ask its operator." Their gadget list kept working, a top-up worked at once, and a relay restart kept every balance.

What it takes
One flag on the relay (--credits) and one command to grant credits. Every day the relay writes a signed, hash-chained receipt for each person. A report checks the credits against the request log, so use can be verified after the fact.

What it is not
No payments, no tokens, no wallets. Credits are a usage measure on a relay you run yourself. We also decided that, for now, builders run their own relays; the project does not operate a shared one.

Tested on one kit, one relay and two people. The full record, the guide and the design decision are public.

If you build hardware, run infrastructure, or want a first open-source contribution, there is room to help:
• Credits guide: https://grokgadgets.org/doc-docs-getting-started-credits-on-your-relay
• Repeat the kit and report what broke: https://github.com/adidshaft/grok-gadgets/issues/185
• Build a gadget for other people: https://github.com/adidshaft/grok-gadgets/issues/269
• Project: https://grokgadgets.org

Independent open source, not affiliated with SpaceXSI.

#OpenSource #IoT #ESP32 #Hardware #GrokBot
