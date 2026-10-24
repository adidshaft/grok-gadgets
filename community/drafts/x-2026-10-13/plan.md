# X build-in-public plan (before the announcement)

Status: draft. Nothing here is posted or scheduled. Each post needs the owner's approval.

## Rules for this phase

- The project has not been announced. These posts share the build. No "launching" and no
  "it's live". No release or star calls to action. Repo links stay out of the main posts and
  go in a reply only when someone asks.
- Every claim comes from a verification record dated 12 or 13 October 2026. One kit, one
  owner. On 12 October Grok Bot reached the board through a local shell command. On
  13 October it called the MCP tools natively from the Mac and the iPhone through a tunnel
  the owner ran, with a sign-in approved on the Mac (hub ADR 007 and the Remote HTTPS
  record). Posts written before 13 October describe the 12 October state only.
- Voice: adidshaft X voice. Plain words, lowercase openings are fine, no semicolons, no
  dashes of any kind, no engagement bait.
- Grok Bot is the only assistant named. The owner's 292 s "Short Demo" recording names
  another tool aloud, so it is not used.

## Audience and timing (US)

Builders who use Grok Bot, ESP32 and Arduino makers, Home Assistant users, and people
building MCP servers.

| Slot | ET | IST |
| --- | --- | --- |
| Morning | 9:30 am | 7:00 pm |
| Lunch | 12:30 pm | 10:00 pm |
| Saturday | 11:00 am | 8:30 pm |

Default run: Wednesday 14 to Sunday 18 October, two posts a day on weekdays, one at
the weekend. Move the start day as you like. Posts don't depend on calendar dates.

## Media (all in `media/`, metadata stripped)

| File | Use |
| --- | --- |
| `oled-online-x.mp4` | 7 s, 1:1. Real OLED showing Online + Grok Bot face, then a brand end card |
| `card-kit.png` | Real kit photos, parts and wiring |
| `card-route.png` | The three hops, with the native-MCP caveat |
| `card-wifi.png` | 8 Wi-Fi checks, including the failure |
| `card-stack.png` | The stack overflow bug |
| `card-sim.png` | No-hardware simulator output (marked simulated) |
| `card-status.png` | What works and what is not proven |
| `board-in-hand.jpg`, `breadboard-kit.jpg`, `oled-module.jpg` | Raw photos for replies |

## Day 1

**1A · morning · video `oled-online-x.mp4`**

> got an ESP32-S3 on my desk to show Online with a small Grok Bot face whenever it holds a TLS session to a gateway on my Mac.
>
> then Grok Bot ran one command on the Mac and "Hi from Grok Bot on Wi-Fi" showed up on the screen. 1.3 inch OLED, four jumpers, a breadboard.

**1B · lunch · `card-route.png`**

> it's three hops. Grok Bot runs a local command, the gateway on the Mac checks the device token, and the board gets the text over its own TLS session on Wi-Fi.
>
> Grok Bot isn't calling the MCP tools natively yet. it ran a shell command. that's the next thing to prove.

## Day 2

**2A · morning · `card-wifi.png`**

> 8 Wi-Fi checks on one ESP32-S3 kit, powered from a phone charger. 7 passed first time.
>
> the one that failed: router off for 3 to 4 minutes, and the board never came back. the Arduino-ESP32 core had stopped retrying on its own. now the firmware starts a fresh join every 15 s while offline. same test after that, back Online in under 15 s.

**2B · lunch · `card-kit.png`**

> the whole kit is an ESP32-S3-N16R8 board, a 1.3 inch I2C OLED and a breadboard. VCC to 3V3, GND, SCK to GPIO9, SDA to GPIO8.
>
> I ordered a 0.96 inch screen and a 1.3 inch one showed up. with the SSD1306 driver it left a lit column on the right edge. it's an SH1106, so that's the default now.

## Day 3

**3A · morning · `card-stack.png`**

> the ESP32 firmware had about 500 bytes left on its 8 KB loop stack and nothing crashed, so nobody knew.
>
> then I added Wi-Fi failure messages to the OLED (No network, Wrong password, Join timeout) and every provision line tripped the stack canary. two 3.4 KB copies of the settings were sitting on the stack. one buffer outside it fixed it.

**3B · lunch · text only**

> passing the I2C pins straight into the U8x8 constructor made begin() hang on this board. setting up Wire first and leaving the constructor alone worked.
>
> also the firmware only looks for the OLED at boot, so after rewiring you have to restart the board or it acts like the screen isn't there.

## Day 4

**4A · morning · `card-sim.png`**

> you don't need a board to try the flow. the gateway has a simulated light, and rehearse makes the same six tool calls Grok Bot would, on your own machine. about five minutes with git and uv.
>
> it prints that it doesn't prove a Grok Bot connection or anything physical, because it doesn't.

**4B · lunch · text only**

> two tests worth running on anything that talks to a home server.
>
> revoke its token and watch how fast it gets dropped. 0.42 s here.
>
> then serve a cert from a throwaway CA. the board failed TLS 23 times in a row and never said hello. that's what you want.

## Day 5 (weekend)

**5A · 11 am ET · `card-status.png`**

> where this stands. one kit passed USB and Wi-Fi checks, and Grok Bot put text on it through a local command.
>
> since then Grok Bot has called the tools natively from my Mac and my phone, through a tunnel I run and a sign-in I approve on the Mac.
>
> not proven yet: leaving that on every day, a real Raspberry Pi, and someone else rebuilding the kit from the written guide. that last one matters most to me.

## Replies and engagement (daily, about 20 minutes)

Searches to run each day: `ESP32 OLED`, `ESP32-S3`, `Grok Bot`, `MCP server hardware`,
`Home Assistant MCP`, `SH1106`. I draft one reply per post that has a concrete detail to
respond to. One narrow question or one useful fact from the build. No links unless asked.
You approve each reply before it goes out.

Reply bank for questions that are likely to come up:

- **"what's the cost?"** the board and screen were ordinary listings. I'd check current
  prices rather than quote mine.
- **"does it work with Grok Bot directly?"** yes, on my setup. Grok Bot calls the six
  tools itself from the Mac and phone apps, through a tunnel I run and a sign-in I approve
  on the Mac. making that safe to leave on every day is the next step.
- **"can I try it?"** there's a no-hardware simulator path. happy to share it.
  (Link only after the owner says the repos can be pointed at.)

## When the announcement is ready

Make the announcement post (thread) with the full video, links to grokgadgets.org and
the repos, and a call for one person to rebuild the kit. Quote the build-log posts from
this plan in it.
