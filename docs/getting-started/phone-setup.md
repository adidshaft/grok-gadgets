# Set up your gadget with your phone

Your gadget came with a printed label. Its builder has already prepared it for the operator’s gateway.
With the label and a phone you can join the gadget to your home Wi-Fi.
Wi-Fi setup needs no computer, separate setup app or setup account. After setup the gadget shows **Online**.

**Status:** Phase 10 ([ADR 010](../decisions/010-phone-setup.md)). On 14 October 2026 the owner set up one kit this way with an iPhone and with an Android phone ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/phone-setup-2026-10-14.md)). Nobody else has repeated it yet.

## What you need

- The gadget and its label. Keep the label private: it works like a key.
- An iPhone or an Android phone with its normal camera.
- Your home Wi-Fi name and password. The gadget uses 2.4 GHz Wi-Fi only.
- A USB charger for the gadget.

## Set it up

1. Plug the gadget into the charger. The screen shows `Setup 10 min` and a name such as
   `GrokGadget-89AB`. You have 10 minutes.
2. Open the phone's camera and point it at the QR code on the label. Tap **Join** when the
   phone offers the gadget's Wi-Fi.
3. The phone opens the **Set up your gadget** page. If it does not, open the browser and go to
   `192.168.4.1`.
4. Type the **setup code** from the label and tap **Continue**.
5. Pick your home Wi-Fi from the list, type its password and tap **Join**.
6. Wait about 20 seconds. The page and the gadget's screen show the result. When the screen
   shows **Online**, setup is done.

Connect your existing Grok Bot account to the operator’s gateway before using the gadget.
Follow [Connect your Grok Bot](connect-grok-bot.md) first. Then ask Grok Bot, for example: "Show hello on my gadget."

## If something goes wrong

| The screen or page shows | Do this |
| --- | --- |
| `Wrong password` | Type the password again and tap **Join**. Check upper and lower case. |
| `No network` | Use a 2.4 GHz network. Check the network name. |
| `Join timeout` | Check that the router is on and near the gadget. Try again. |
| "That setup code is not right" | Check the code on the label. `0` and `O`, `1` and `I` are never used. |
| "Too many wrong codes" | Wait for the time on the page, then try again. |
| `Setup closed` and `Power cycle` | Unplug the gadget, plug it in again, and start from step 2. |
| `Setup locked` | Too many wrong codes. Unplug the gadget and plug it in again. |
| The page drops while joining | Normal for a few seconds. Watch the gadget's screen for the result. |

## Move to a new network

Hold the gadget's **BOOT** button for 10 seconds. The screen counts down and the gadget forgets
your Wi-Fi. It keeps everything else. It opens its setup Wi-Fi again: start from step 1.

## Privacy

- The gadget sends your Wi-Fi password to nobody. It stores the password on the gadget only.
- The setup page never shows a stored value.
- Anyone who holds the gadget can read what it stores. If you give the gadget away, reset it
  with BOOT first.
