# Repeat the ESP32-S3 OLED setup

Use this guide to repeat the owner's 12 October 2026 setup. It covers one
YD-ESP32-23 v1.3 board with an ESP32-S3-N16R8 module and one 1.3-inch SH1106
OLED at I²C address `0x3C`. The owner passed USB and Wi-Fi acceptance with this
kit. Your results are new evidence; do not assume your board will pass.

Use the released [ESP32 SDK v0.2.0-alpha.9](https://github.com/adidshaft/grok-gadgets-esp32-sdk/releases/tag/v0.2.0-alpha.9)
and [gateway v0.1.0-alpha.6](https://github.com/adidshaft/grok-gadgets-gateway/releases/tag/v0.1.0-alpha.6).
Read each repository's setup guide before running its commands. Firmware binaries
are not published. Build the firmware from source.

## 1. Check the parts

- Check that the board says `YD-ESP32-23` and `v1.3`. Check the module marking
  `ESP32-S3-N16R8`.
- Check that the OLED says `RG1.30 IIC V2.2` and has `VCC`, `GND`, `SCK` and
  `SDA` pads. This guide uses the SH1106 controller.
- Use a USB-C data cable for flashing and provisioning. Use the board's native
  **USB** port, not **COM**. Use a 2.4 GHz Wi-Fi network for the wireless run.

Disconnect USB power before you move a wire. Use a secure connection. The
delivered boards had no fitted pin headers; loose jumpers caused resets during
the owner's first attempt. The passing test used jumpers directly on the pins.

| OLED pad | Board pad |
| --- | --- |
| `VCC` | `3V3` |
| `GND` | `GND` |
| `SCK` | GPIO9 |
| `SDA` | GPIO8 |

The onboard RGB light uses GPIO48. The BOOT button uses GPIO0. Check printed pad
labels; do not infer pin position from a photo or wire color.

## 2. Flash and check USB

In the ESP32 SDK checkout, follow [Build and flash](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/v0.2.0-alpha.9/examples/oled-kit/README.md).
Build `esp32s3-oled-kit` for USB or `esp32s3-oled-kit-wifi` for Wi-Fi. For the
first flash, hold BOOT while you connect the cable to **USB**, then release it.
Restart the board after you change any display wire. The firmware checks for the
OLED at startup.

For a USB run, start the gateway and its USB bridge by following the
[gateway kit guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/v0.1.0-alpha.6/docs/experiment-kit.md).
Check a short `display.text` command, `display.clear`, the RGB light, a BOOT
press and recovery after unplugging and reconnecting. Record the command reply
and what you saw on the board as separate results. A reply does not prove a
physical effect.

## 3. Provision and check Wi-Fi

For Wi-Fi, use the ESP32 SDK's `esp32s3-oled-kit-wifi` build. In the gateway
checkout, follow the [Wi-Fi devices guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/v0.1.0-alpha.6/docs/wifi-devices.md).
Keep the gateway on the Mac and start its private LAN TLS listener by hand.
There is no installed service. Reserve the Mac's address on your router; if it
changes, issue a new listener certificate and provision the board again.

1. Run `uv run grok-gadgets-gateway init` and `uv run grok-gadgets-gateway lan-cert PRIVATE_ADDRESS` for the Mac's private address.
2. Run `uv run grok-gadgets-gateway enroll DEVICE` once. Use the same device ID that
   the board reports.
3. Stop the USB bridge. Run `uv run grok-gadgets-gateway wifi-provision PORT --device
   DEVICE --lan PRIVATE_ADDRESS` while the board is on the USB data cable. Type
   the Wi-Fi name and password at the local prompts. Do not paste them into a
   public issue or log.
4. Start `uv run grok-gadgets-gateway serve --lan-listen PRIVATE_ADDRESS`. Move the
   board to a USB charger. Wait for **Online** on the OLED.
5. Send a short text command and clear it. Press and release BOOT. Turn the
   router off and on, then check that the board returns to **Online**. Restart
   the gateway and check it again.

The board uses a pinned local CA certificate and a device token. It stores the
Wi-Fi password and token in flash without encryption. If the board is lost,
revoke its token and change the Wi-Fi password. Do not forward the LAN listener
port on your router or put it behind a tunnel.

Holding BOOT for 10 seconds erases the board's Wi-Fi settings. The display
counts down after 3 seconds. Release BOOT before zero to keep the settings.

## 4. Record the result

Copy this table into a new [GitHub issue](https://github.com/adidshaft/grok-gadgets/issues).
Remove private addresses, Wi-Fi names, tokens, passwords, serial numbers and
household details before posting.

| Item | Your result |
| --- | --- |
| Board and OLED markings | |
| ESP32 SDK and gateway release tags | |
| Firmware build and SHA-256 | |
| Host OS and connection type | |
| OLED text and clear: reply / observation | |
| RGB and BOOT: reply / observation | |
| USB disconnect and recovery | |
| Wi-Fi online and recovery, if tested | |
| Failed or skipped checks | |

The owner's [USB record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-2026-10-12.md)
and [Wi-Fi record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/verification/oled-kit-wifi-2026-10-12.md)
show the evidence level to use. Grok Bot ran an approved local command in the
owner's setup; native MCP tool calls remain unverified.
