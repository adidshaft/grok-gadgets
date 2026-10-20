# Claim your gadget

Your relay account owns a gadget after you claim it with the code on its screen.
Your Grok Bot sees your owned gadgets and those shared with your account.
Other accounts cannot see yours unless you share them.

**Tested on 17 October 2026:** two people used their own iPhones, one relay and the owner’s OLED kit.
See the [record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/claim-2026-10-17.md) and [accounts design](../decisions/011-accounts-and-claim-codes.md).
On 18 October, the owner's Grok Bot on Android also claimed the kit and showed text.
See the [Android record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ready-for-others-2026-10-18.md#android-and-a-stranger-style-sign-in-tier-owner-18-october-2026).
Independent relay reproduction remains open in [#269](https://github.com/adidshaft/grok-gadgets/issues/269).

## What you need

- A relay running gateway `0.1.0-alpha.15` or later with accounts enabled.
- Gadget firmware from ESP32 SDK `0.2.0-alpha.16` or later.
- The gadget, set up on your home Wi-Fi ([Set up your gadget with your phone](phone-setup.md)).
- Grok Bot on your phone or computer.
- The relay address from the person who gave you the gadget, for example
  `https://gadgets.example.net/mcp`.

## Claim it

1. Look at the gadget's screen. An unclaimed gadget shows `Code XXXX-XXXX` and
   `Add in Grok Bot`. The code changes every 10 minutes.
2. In Grok Bot, say: "Add the Remote HTTPS server https://gadgets.example.net/mcp with OAuth
   sign-in." Use the address you were given.
3. Tap the sign-in card. A page asks for the code. Type the code from the screen and tap
   **Continue**. The page closes and Grok Bot is connected.
4. The gadget's screen changes to **Online**.
5. Grok Bot asks what to call the gadget. Give it a simple name and a room, for example
   "Desk display" in "Office". From now on you can say "show hello on the desk display".
6. Say: "Give me a recovery code for my gadget account." Keep the code private. It signs you
   in again on a new phone, or after 30 days without use.

## Add another gadget

When you are already signed in, say: "Claim the gadget code XXXX-XXXX" with the code on the
new gadget's screen.

## Share a gadget

- Say: "Share the desk display with use access." Grok Bot gives you a share code. It works
  once, for 10 minutes. Give it only to the person you mean.
- `use` lets them read the gadget and send it commands. `view` lets them only read it.
- They say "Claim this share code" in their own Grok Bot. Your accounts stay separate.
- To end it, say: "List the shares on the desk display and revoke them."

Sharing keeps your ownership. To change the owner, follow [Hand a gadget to someone](hand-a-gadget-to-someone.md).

## If something goes wrong

| What you see | Do this |
| --- | --- |
| "That code did not work." | Type the code on the screen now. Codes change every 10 minutes and work once. |
| "Too many tries" | Wait an hour, or ask the relay's operator. |
| Grok Bot says it is not signed in | Tap the sign-in card again and type a fresh code. |
| The gadget shows `Online`, but your Grok Bot does not list it | Someone else has claimed it. Ask them to remove it, or see [Hand a gadget to someone](hand-a-gadget-to-someone.md). |
| You lost your recovery code and cannot sign in | Ask the relay's operator for a link code (`accounts link`). |

## What the relay keeps

The relay keeps your account ID, which gadgets you own or share, and the names you gave
them. It keeps codes only in memory and never writes them to a file or a log. The relay's
operator can see and change everything on their server.
