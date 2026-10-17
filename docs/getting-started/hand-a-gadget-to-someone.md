# Hand a gadget to someone

You can give your gadget to another person. A reset on the gadget alone never moves it to
them: you agree on Grok Bot, or a 7-day wait passes. This stops a stranger who picks up your
gadget from taking it.

**Status:** Phase 11 ([ADR 011](../decisions/011-accounts-and-claim-codes.md)). On 17 October 2026 the owner and a second person handed the kit over this way ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/claim-2026-10-17.md)). The 7-day wait is tested in software only.

## The quick way: remove it first

1. You say in Grok Bot: "Remove my gadget, the desk display."
2. The gadget's screen shows `Code XXXX-XXXX`.
3. The new owner claims it with that code ([Claim your gadget](claim-your-gadget.md)).

## When the gadget is already with them

1. The new owner holds the gadget's **BOOT** button for 10 seconds. The screen counts down.
2. They set it up on their Wi-Fi with their phone and the label
   ([Set up your gadget with your phone](phone-setup.md)).
3. The screen shows `Code XXXX-XXXX` for 10 minutes. This is a transfer code.
4. They say in their Grok Bot: "Claim the gadget code XXXX-XXXX." Grok Bot says the transfer
   is **pending**. They cannot use the gadget yet.
5. You still own it. Your Grok Bot lists it with the pending transfer and the date it
   completes.
6. To let it go now, say: "Remove my gadget, the desk display." The transfer completes at
   once, and the new owner can use it.
7. If you did not agree, say: "Refuse the transfer of the desk display." The gadget stays yours.
   Do this within 7 days: after that, a pending transfer completes by itself.

When a gadget changes hands, every share ends and the old names for it are removed.

## If something goes wrong

| What you see | Do this |
| --- | --- |
| The screen shows `Online`, not a code, after the reset | The transfer code shows only after a phone setup. Do steps 1 and 2 again. |
| "That code did not work." | The code lasts 10 minutes. Reset and set up again for a new one. |
| Grok Bot says "waiting for its owner" | The old owner has not removed it yet. Ask them, or wait for the 7 days. |
