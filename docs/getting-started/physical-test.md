# Test the ordered ESP32-S3 and OLED kit

**Status: physical verification pending.** Compilation and simulated board tests do not complete this procedure.

## Before the test

Follow the [exact kit, inspection and wiring plan](experiment-kit.md). Wait until the board and OLED are available. Do not use C124 pin assignments or its firmware image. Obtain the owner's authorization before flashing it. Use the ESP32 SDK's pinned build and recovery instructions.

Run the local gateway and USB bridge on the host computer. A hardware test needs no public tunnel. The packaged remote MCP route for Grok Bot is not ready. Local `serve` listens only on `127.0.0.1:8766/mcp` and uses a bearer token. An authenticated remote MCP endpoint with TLS and approved, verified Grok Bot invocation are still needed. A tunnel adds reachability, not authentication.

Grok Bot's normal cloud computer cannot reach your private LAN through its internet connection alone. A separate possible experiment uses **Execution on Local Computer**. Enable it and approve a Mac command. Then use SSH from the Mac to a reachable Pi with SSH set up. USB alone does not create this route. This is not verified Grok Gadgets support or a packaged MCP integration. Read the [hosting FAQ](hosting.md) for the three paths. Do not expose the device protocol directly.

Record the AYWHP board and module markings, Robocraze OLED controller/interface, ApTechDeals breadboard wiring, reviewed pin table and USB-C data cable. Record firmware SHA-256, gateway and SDK commits, host operating system, port, time and tester. Do not record tokens. Pins, display driver and board configuration are provisional until inspection.

**M5 — Actual Grok remains blocked** on supported exact-kit invocation/reload evidence and the remote route. **M8 — Physical and independent verification remains blocked** until the ordered kit is inspected, peripheral operation is observed and independent reproduction is recorded. A Pi is not required for this ESP32-S3 experiment.

## Procedure

1. Discover the device. Check its model, boot identity, capabilities, firmware version and `simulated: false` value.
2. After the display capability and confirmed driver are implemented, request a short OLED message. Observe the 128×64 display, change the message and clear it. Record command results and physical observations separately. Check invalid or oversized text fails without an unintended change. If a suitable LED is fitted, test its declared output capability; a plain LED has no RGB capability.
3. If a suitable onboard or optional external button is fitted, press and release it. If none is fitted, record this check as skipped; do not claim a pass. Check event order and reported state. Repeat the reads and check for duplicate events.
4. Unplug the board. Try a command. Check that the result reports offline or unconfirmed status.
5. Reconnect the board. Check state recovery.
6. Restart the board and gateway separately. Check boot and session changes, cursor reset and stale state. Check that old actions do not run again.
7. Repeat through the existing Grok Bot after authentication and connection requirements pass. Test each available client separately.
8. Ask a second tester to follow the procedure. Record any differences.

Do not mark a failed or unavailable step as passed. Record its blocker and supporting evidence.
