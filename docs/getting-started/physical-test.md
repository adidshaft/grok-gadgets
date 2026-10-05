# Test the C124 hardware

**Status: physical verification pending.** Compilation and simulated board tests do not complete this procedure.

## Before the test

Wait until the board is available. Obtain the owner's authorization before flashing it. Use the ESP32 SDK's pinned build and recovery instructions.

Run the local gateway and USB bridge on the host computer. A hardware test needs no public tunnel. The cloud Grok route requires a future authenticated remote MCP service and separate invocation evidence. Read the [hosting FAQ](hosting.md) before planning remote access. Do not expose the device protocol directly.

Record the board model C124, USB-C data cable, firmware SHA-256, gateway and SDK commits, host operating system, port, time and tester. Do not record tokens.

## Procedure

1. Discover the device. Check its model, boot identity, capabilities, firmware version and `simulated: false` value.
2. Request green. Observe the physical LED. Repeat with another color, then turn it off. Record command results and physical observations separately.
3. Press and release the button. Check event order and reported state. Repeat the reads and check for duplicate events.
4. Unplug the board. Try a command. Check that the result reports offline or unconfirmed status.
5. Reconnect the board. Check state recovery.
6. Restart the board and gateway separately. Check boot and session changes, cursor reset and stale state. Check that old actions do not run again.
7. Repeat through the existing Grok Bot after authentication and connection requirements pass. Test each available client separately.
8. Ask a second tester to follow the procedure. Record any differences.

Do not mark a failed or unavailable step as passed. Record its blocker and supporting evidence.
