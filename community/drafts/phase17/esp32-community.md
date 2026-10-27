# ESP32 community post. Draft only (27 Oct 2026)

For an ESP32 maker forum or subreddit the owner chooses. Read its rules on self-promotion
first; post as a project share with a question, not an ad.

**Title:** ESP32-S3 + SH1106 OLED that joins Wi-Fi from a phone and takes commands from Grok Bot. Looking for someone to repeat the build

**Body:**

---

I've been building an open-source SDK for ESP32-S3 gadgets that Grok Bot can control. My test board is an ESP32-S3 dev board with a 1.3-inch SH1106 OLED on a breadboard.

What it does on my kit:

- First boot opens a short setup window; a phone joins the board to home Wi-Fi with no cable and no app.
- The OLED shows a claim code; whoever enters it owns the gadget, and their Grok Bot can then show text, clear the screen and read the BOOT button state.
- Firmware updates are signed and go over Wi-Fi; a bad image reverts on its own (I tested a power cut mid-download).

What I don't know yet is whether the guide works for anyone else. If you have an ESP32-S3 and a 1.3-inch SH1106 OLED lying around, I'd love a run of the guide, including where it fails:

- Guide and parts: https://github.com/adidshaft/grok-gadgets/blob/main/docs/getting-started/repeat-the-kit.md
- Where to report: https://github.com/adidshaft/grok-gadgets/issues/185

Questions about the wiring, PlatformIO setup or the protocol are welcome here too. Apache-2.0, nothing for sale.

---
