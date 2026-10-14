# How it works

Grok Gadgets lets your Grok Bot use small devices: a display, a light, a button. You talk to Grok Bot as usual, and it uses the device for you.

There are three people in this story:

- **The builder** makes a gadget with our SDKs and gives or sells it.
- **The end user** owns the gadget and talks to their own Grok Bot.
- **Grok Bot** runs the chat and calls the gadget's tools when you ask.

## The picture

```text
 End user                       Builder's relay                 Home
 Grok Bot on phone or Mac       (an always-on server)
 ┌──────────────┐  HTTPS +     ┌──────────────────┐   TLS,      ┌──────────┐
 │ "Show hello  │  sign-in     │ gadget tools     │   outbound  │  gadget  │
 │  on my       │ ───────────▶ │ device listener  │ ◀────────── │  (Wi-Fi) │
 │  display"    │              └──────────────────┘             └──────────┘
 └──────────────┘
```

- The gadget connects **out** from the home Wi-Fi to the relay. No router setup and no computer at home.
- Grok Bot connects to the relay with a one-time sign-in.
- The relay passes Grok Bot's request to the gadget and passes the answer back.

## What each person does

**Builder (once):**

1. Build the gadget with the [ESP32 SDK](https://github.com/adidshaft/grok-gadgets-esp32-sdk) and test it with the simulator.
2. Run one relay for all their gadgets. It is the open-source gateway on a small server.
3. Give each gadget its identity and the relay's address, then ship it.

**End user (once per builder):**

1. Plug in the gadget and join it to home Wi-Fi.
2. Add the builder's address in Grok Bot and sign in once.
3. Talk. It works from the phone and from the Mac.

## Common questions

**Can the builder's relay see my Grok Bot?**
No. Grok Bot signs in to the relay, not the other way round. The relay only receives the gadget requests that your Grok Bot sends: the device, the command and the device's reported state. It never sees your chats, your account or your Wi-Fi password. You can remove the connection at any time.

**Do I need a special Grok Bot?**
No. You keep the Grok Bot you use every day. The gadgets are one more connection in it, on the phone and on the Mac.

**What if I do not want to use the builder's relay?**
The software is open source. You can run your own relay for your own gadgets. The [Mac-free route guide](mac-free-route.md) shows how.

**I own gadgets from four builders. Do I need four apps?**
No. Add each builder's address to Grok Bot once and sign in once for each. Then one Grok Bot chat can use all of them: "dim the lamp and show the weather on the desk display". This is the design; so far one gadget server has been tested.

**What happens if the relay is down?**
Grok Bot tells you it cannot reach the gadget. Nothing is queued. The gadget shows `Relay...` and reconnects by itself when the relay is back.

**Can a button on the gadget start a Grok Bot chat?**
No. Button presses wait on the relay until Grok Bot reads them.

## What works today and what is planned

| Step | State |
| --- | --- |
| Grok Bot on Mac and iPhone calls the gadget tools | Works on the owner's kit, gateway on the Mac |
| Gadget reaches an always-on relay instead of the Mac | Works on the owner's kit since 13 October 2026, with the Mac asleep ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/mac-free-route-2026-10-13.md)) |
| Wi-Fi setup from a phone, no cable | Planned, Phase 10 |
| Sign in with a code shown on the gadget | Planned, Phase 11 |
| One-command relay for builders | Planned, Phase 12 |

Today a person needs a USB cable, a terminal and an approval step on the server. The later phases remove those steps for end users. See the [roadmap](../../ROADMAP.md) and [ADR 009](../decisions/009-relay-route.md).

Next: [Connect your Grok Bot](connect-grok-bot.md) · [Run the gateway away from your Mac](mac-free-route.md)
