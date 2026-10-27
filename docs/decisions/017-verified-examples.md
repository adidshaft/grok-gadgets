# ADR 017 — Verified examples: what Pass means for the climate sensor, switch and servo

**Date:** 27 October 2026

**Status:** Proposed. The owner accepts it when the three examples have their hardware records and the daily-use record exists. No money moves.

**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)

**Phase:** 18, "More gadgets in daily use" ([milestone](https://github.com/adidshaft/grok-gadgets/milestone/27)). ADR numbers differ from phase numbers.

**Issues:** hub [HUB-EX-001 #449](https://github.com/adidshaft/grok-gadgets/issues/449), [HUB-EX-003 #451](https://github.com/adidshaft/grok-gadgets/issues/451), [HUB-EX-004 #452](https://github.com/adidshaft/grok-gadgets/issues/452), [HUB-DAILY-002 #271](https://github.com/adidshaft/grok-gadgets/issues/271); ESP32 [ESP-EXAMPLE-004 #167](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/167)

## Context

[ADR 013 §6](013-builder-kit.md) added three builder examples to the ESP32 SDK: a climate sensor, a low-voltage switch and a servo. They compile, and each passes host tests. Nobody has run them with the parts, so every guide marks them **Not tested on hardware**. The OLED kit is still the only gadget with a hardware record.

Two numbers are also missing. Phase 8 recorded one day of the daily route, and [#271](https://github.com/adidshaft/grok-gadgets/issues/271) asks for another day and a usable measurement. [ADR 016](016-pay-for-a-relay.md) measured 1 credit per gadget-day twice, but both runs had no commands. A typical day with commands is open.

Facts this decision depends on:

- **Parts.** Each example names one part. The climate sensor uses an AHT20 I²C module. The switch uses a 1-channel relay module that switches from 3.3 V logic. The servo is an SG90 on its own 5 V supply with a common ground. The board is the OLED kit's ESP32-S3-DevKitC-1 with an ESP32-S3-WROOM-1-N16R8 module. The switch is for low-voltage loads only.
- **Updates bind a board name.** A signed update names the build environment as its board ([ADR 012](012-signed-updates.md)). A gadget refuses an image for another board. So the OLED kit cannot become an example by signed update, and a new board's first image goes on by USB.
- **Counting commands.** The gateway's `usage` command summarizes its request log by day and capability. It reads no Grok Bot account and prints no arguments, state or tokens.

## Decision

### 1. Pass per example

An example passes when every check in its README passes on hardware, with Grok Bot through the owner's relay:

| Example | Checks |
| --- | --- |
| Climate sensor | Grok Bot reads `climate` close to a room thermometer; `threshold.set` near the reading, then `threshold.crossed` with `above: true` and `above: false`; an out-of-range value is refused; an unplugged module reports `sensor: missing` and returns when plugged back |
| Switch | `switch.set` on and off with the load following; the same value again changes nothing; with the load on, a lost relay link turns it off between 30 and 35 seconds; it boots off |
| Servo | `servo.move` to 0 and 180 with the status after the move ends; an out-of-range angle is refused and the arm stays put; the board does not reset during a move |

Each check is **Pass**, **Fail** or **Not tested**. The evidence is gateway or relay logs plus the owner's observation and a photo of the wiring. Model narratives are not evidence. One record, `docs/verification/examples-2026-MM-DD.md`, covers all three.

### 2. Boards

We prefer one board per example: all three then run together during daily use, and the OLED kit stays on the relay. One board may also take each example in turn. The record says which.

### 3. Images

Each new board's first image goes on by USB, with factory provisioning, as in [Ship a gadget](../getting-started/ship-a-gadget.md). Every later image for that example goes by signed update over the relay. Each flash and each update waits for the owner's yes.

### 4. Daily use

The owner uses the gadgets from Grok Bot for at least three UTC days in a row. Commands per day come from `grok-gadgets-gateway usage --since … --until … --json` on the relay, read once at the end with the owner's yes. The record keeps counts only: commands per day and per capability, and gadget-days. It keeps no command arguments, state, account names, tokens, hostnames or addresses.

The count closes [#271](https://github.com/adidshaft/grok-gadgets/issues/271) and gives ADR 016 its commands row. Neither the record nor ADR 016 states a price.

### 5. Linux

The Linux SDK's climate example is simulated. With a Raspberry Pi or another Linux board with I²C, it runs with a real AHT20 over long-poll. Without one, the record says Not tested.

## Consequences

- Builders get three examples with hardware records, not only the OLED kit.
- Stage 0 gets a commands-per-day number from real use.
- One owner, one relay and one set of parts is still one setup. An outside builder ([#269](https://github.com/adidshaft/grok-gadgets/issues/269)) and tester ([#185](https://github.com/adidshaft/grok-gadgets/issues/185)) remain open.

## Not in scope

Mains wiring, payments, wallets, prices, mainnet, operator payouts, hardware identity, the Home Assistant bridge and capacity work.
