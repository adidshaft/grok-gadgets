# Test the ordered ESP32-S3 and OLED kit

**Status: passed on the owner's kit on 12 October 2026** ([record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/dev/docs/verification/oled-kit-2026-10-12.md)).
Another person's reproduction is still needed. Compilation and simulated board
tests do not complete this procedure.

## Before the test

Follow the [kit parts and tested wiring](experiment-kit.md). The YD-ESP32-23
v1.3 board and RG1.30 IIC v2.2 display have no fitted headers; establish secure
connections before powering the display. Do not use C124 pin assignments or its
firmware image. Flash only a board you own, with the image built for it. Use the ESP32 SDK's pinned build and recovery instructions.

Run the local gateway and USB bridge on the host computer. A hardware test needs no public tunnel. The packaged remote MCP route for Grok Bot is not ready. Local `serve` listens only on `127.0.0.1:8766/mcp` and uses a bearer token. An authenticated remote MCP endpoint with TLS and approved, verified Grok Bot invocation are still needed. A tunnel adds reachability, not authentication.

Grok Bot's normal cloud computer cannot reach your private LAN through its internet connection alone. A separate possible experiment uses **Execution on Local Computer**. Enable it and approve a Mac command. Then use SSH from the Mac to a reachable Pi with SSH set up. USB alone does not create this route. This is not verified Grok Gadgets support or a packaged MCP integration. Read the [hosting FAQ](hosting.md) for the three paths. Do not expose the device protocol directly.

Record the YD-ESP32-23 v1.3 board and ESP32-S3-N16R8 module markings. Record the
Electrifier RG1.30 IIC v2.2 display, actual controller/address, breadboard wiring,
pin table and USB-C data cable. Record firmware SHA-256, gateway and SDK
commits, host operating system, port, time and tester. Do not record tokens. The
3.3 V GPIO8/GPIO9 wiring passed on the owner's kit.

**M5 — Actual Grok is partly done:** Grok Bot showed text on this kit through local shell execution; native tool calls need the remote route. **M8 — Physical and independent verification is partly done:** the owner's kit passed; independent reproduction is still needed. A Pi is not required for this ESP32-S3 experiment.

## Procedure

1. Discover the device. Check its model, boot identity, capabilities, firmware version and `simulated: false` value.
2. Request a short OLED message. Observe the 128×64 display, change the message and clear it. Record command results and physical observations separately. Check invalid or oversized text fails without an unintended change. If a suitable LED is fitted, test its declared output capability; a plain LED has no RGB capability.
3. If a suitable onboard or optional external button is fitted, press and release it. If none is fitted, record this check as skipped; do not claim a pass. Check event order and reported state. Repeat the reads and check for duplicate events.
4. Unplug the board. Try a command. Check that the result reports offline or unconfirmed status.
5. Reconnect the board. Check state recovery.
6. Restart the board and gateway separately. Check boot and session changes, cursor reset and stale state. Check that old actions do not run again.
7. Repeat through the existing Grok Bot after authentication and connection requirements pass. Test each available client separately.
8. Ask a second tester to follow the procedure. Record any differences.

Do not mark a failed or unavailable step as passed. Record its blocker and supporting evidence.
