# Tell me when: a routine that reads gadget events

A button press on a gadget cannot wake Grok Bot. Grok Bot documents no way for an outside
device to start a conversation or send you a notification. A gadget event waits in the
gateway until Grok Bot reads it.

To hear about events without asking, give one Bot a **routine** that reads your gadget events
on a schedule and tells you only when something new happened.

## What you get, and its limits

| Question | Answer |
| --- | --- |
| How soon do I hear about a button press? | At the next run. Routine schedules must be at least five minutes apart, so expect up to five minutes or more. |
| Does a press wake Grok Bot at once? | No. There is no push from a gadget. |
| Can I set it up on the phone? | You can pause, resume, review and delete a routine on the phone. Editing its schedule or instruction and testing it currently need the desktop app. |
| Does it run while my computer is off? | Background routines run in the cloud. The gateway must be reachable, for example on a [relay](mac-free-route.md). |
| Does it cost usage? | Yes. Every run is Bot work and counts towards your weekly usage, even when there is nothing new. |
| How many? | A Bot can own up to 50 routines. |

Sources: Grok Bot [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations), [Mobile](https://docs.x.ai/grok-bot/mobile), [Approvals, security, and privacy](https://docs.x.ai/grok-bot/approvals-security-and-privacy) (read 14 October 2026).

## Before you start

- Grok Bot already uses your gadgets: [Connect your Grok Bot](connect-grok-bot.md).
- The gateway runs where the routine can reach it at any hour. A Mac that sleeps misses runs.

## Set it up

1. In the desktop app, open the Bot that has the `grok-gadgets` server and send:

   > Every 5 minutes, call `gadgets_read_events` from grok-gadgets with a null cursor. Look
   > only at events whose `received_at` is within the last 5 minutes. If there are any, tell me
   > the device, the event name and the time. If there are none, finish without a message.

2. The Bot creates the routine and shows its next run. Check the schedule says every 5 minutes.
3. Approve the first `gadgets_read_events` call when the Bot asks. Choose **Always allow this
   in the future** only for `gadgets_read_events`. It reads events and changes nothing.
4. Press the gadget's button, wait for the next run, and check that the Bot tells you.

Why the approval rule matters: an approval for work that started without you, such as a
routine, expires after about 10 minutes. The action then does not run. Without the rule, a
routine that runs while you are away reads nothing.

Do not add an automatic rule for `gadgets_command`. A routine should read, not act.

## Tune it

- **Less usage:** a longer schedule, for example every 15 minutes, with "within the last 15 minutes".
- **One gadget:** add "only for device `oledkit-0123456789ab`" to the instruction.
- **Quiet hours:** pause the routine from the Bot's profile on the phone with **Active**.

The gateway keeps the last 128 events. If a run sees `history_lost`, older events were dropped
before the routine read them.

## What is not verified

- The owner has not yet run this routine for a measured day. The usage per run is unknown.
  [Track usage](track-usage.md) explains how to measure it.
- Whether a run that finds nothing still sends a notification depends on your notification
  settings. Check after the first quiet run.
- Grok Bot documents events from its own account integrations as routine triggers. It
  documents no trigger URL or webhook that a gadget could call.
