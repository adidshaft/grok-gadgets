# C124 physical acceptance procedure — pending

Record board model C124, USB-C data cable, firmware SHA256, gateway/SDK commits, host OS, port, timestamp, and tester. Flash only after hardware is available and the user authorizes flashing their board. Use the SDK's pinned build and bootloader recovery instructions.

1. Discover the device and verify model, boot, capabilities, firmware and `simulated:false`.
2. Request green and observe LED physically, then another colour and off. Save both command/execution results and human observation separately.
3. Press/release the button; inspect ordered events and reported state. Check repeated reads do not introduce duplicates.
4. Unplug, attempt control, verify offline/unconfirmed status. Reconnect and verify state recovery.
5. Reboot device and gateway independently; check boot/session change, cursor reset, stale state, and no action replay.
6. Repeat through actual existing Grok Bot and each available client after account and reachable-authentication gates pass.
7. Ask a second tester to follow the instructions independently and record deviations.

Never capture tokens. Compilation and PTY/board-stub results cannot fulfill any physical step above.
