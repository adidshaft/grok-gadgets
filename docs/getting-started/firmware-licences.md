# Firmware licence checklist

**This is not legal advice.** It lists what to publish with a firmware binary built with the
Grok Gadgets ESP32 SDK. People who get the binary must also get the source and the notices
that the licences ask for. Check your own build and its licences before you ship.

**Status:** Phase 12b. This checklist replaces the blocked framing of hub
[#30](https://github.com/adidshaft/grok-gadgets/issues/30). Signed binaries can ship from Phase
12b ([ADR 012](../decisions/012-signed-updates.md)).

## What is in a kit image

The OLED kit's `esp32s3-oled-kit-wifi` image links these parts
([dependency record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/dependencies.md)):

| Part | Version | Licence | What it asks of a binary |
| --- | --- | --- | --- |
| Grok Gadgets ESP32 SDK and the kit sketch | your release tag | Apache-2.0 | Include `LICENSE` and `NOTICE` |
| Arduino-ESP32 core | 2.0.17 (PlatformIO package 3.20017.0) | LGPL-2.1 for the Arduino core files | Corresponding source of the library, its licence, and the means to relink (below) |
| ESP-IDF and its components, prebuilt in the core | 4.4.7 | Apache-2.0, with other permissive licences in some components (for example mbedTLS Apache-2.0, lwIP BSD, FreeRTOS MIT) | Include their licence texts and notices |
| ArduinoJson | 6.21.5 | MIT | Include the copyright and licence text |
| U8g2 | 2.36.18 | BSD-2-Clause; its `LICENSE` file also lists font licences | Include the whole `LICENSE` file |

The AtomS3 Lite build also links Adafruit NeoPixel 1.12.3 under **LGPL-3.0**. The kit image
does not. LGPL-3.0 adds "Installation Information" duties for consumer products. Check them
before you ship a binary that links it.

LGPL-2.1 section 6(a) lets you distribute a combined work with the library's source and your
own work as relinkable object code or source
([LGPL-2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)).

## Checklist for each binary

### The exact build

- The source tag and commit of the SDK, and of your sketch if it is separate.
- The PlatformIO Core version.
- The pinned packages from `platformio.ini`: `espressif32@6.10.0`,
      `framework-arduinoespressif32@3.20017.0`, `toolchain-xtensa-esp32s3@8.4.0+2021r2-patch5`
      and `tool-esptoolpy@1.40501.0`.
- The build command, for example `pio run -e esp32s3-oled-kit-wifi`.
- The environment variables you set: `GROK_FIRMWARE_VERSION`, and that you set
      `GROK_UPDATE_PUBLIC_KEY` (not the key file's path or content).
- SHA-256 of every file you ship.
- The toolchain's host variant (`darwin_x86_64`, `darwin_arm64` or Linux). The image hash
      depends on it.

### Source and notices

- A link to the exact source tag, or a source archive of it.
- The Arduino-ESP32 2.0.17 source, or a link to Espressif's tag
      ([`2.0.17`](https://github.com/espressif/arduino-esp32/tree/2.0.17)).
- With a link only: a written offer to supply that source if the link stops working.
- One notices file with the licence texts of every part in the table above.
- `LICENSE` and `NOTICE` of the Grok Gadgets SDK.

### Relinking (LGPL-2.1)

- Open sketch: the source and the build steps above are enough to rebuild and relink.
- Closed sketch: ship the object files of your own code. These are the `.o` and `.a`
      files in `.pio/build/<env>/`, without the framework's own.
- Closed sketch: ship the linker command and the build configuration too. Then someone
      can relink with a changed core.
- Someone who changes the library can still put the result on the board.
- On the kit, USB flashing stays open because secure boot is off. If you turn on secure
      boot for a product, check what the licences ask before you ship.

### Signed updates

- An update-capable image contains your public key. Publish the key's ID (from
      `firmware keygen`), not the private key.
- The signed manifest names the board, version and SHA-256 of the image. Ship it with the
      release so anyone can compare the binary.

## A release asset, put together

| File | What it is |
| --- | --- |
| `firmware.bin` | The application image (also what a signed update carries) |
| `bootloader.bin`, `partitions.bin`, `boot_app0.bin` | For a first USB flash, with their offsets |
| `manifest.json`, `manifest.sig` | Only for a signed image |
| `SHA256SUMS` | Hashes of every file above |
| `NOTICES.txt` | Licence texts and notices of every part |
| `BUILD.md` | Tag, commit, toolchain, command, host variant |
| Source archive or tag link | The exact source, and the Arduino-ESP32 2.0.17 source link |

The project's own releases ship source only until the owner decides to publish a kit binary.
