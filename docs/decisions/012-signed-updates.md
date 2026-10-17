# ADR 012 — Signed firmware updates over the relay, with automatic revert

**Date:** 17 October 2026

**Status:** Accepted on 17 October 2026 with the Phase 12b [record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ota-2026-10-17.md): the owner's kit took signed updates over the relay with no cable, refused a wrong key and a changed byte, reverted an image that never came Online, and recovered from a power cut during a download., and Grok Bot showed text on the updated kit. The owner took decisions 1–5 on 17 October 2026 (below).

**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)

**Issues:** hub [HUB-SHIP-COMPLIANCE-001 #293](https://github.com/adidshaft/grok-gadgets/issues/293), [HUB-LIC-001 #294](https://github.com/adidshaft/grok-gadgets/issues/294), [#30](https://github.com/adidshaft/grok-gadgets/issues/30); ESP32 [ESP-CORE-001 #124](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/124), [ESP-OTA-001 #125](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/125); gateway GW-OTA-001

## Context

[ADR 011](011-accounts-and-claim-codes.md) lets a person claim a gadget that someone else built. Once it leaves the builder's desk, nobody can update it: a new image needs the USB cable and a computer with the toolchain. A gadget that cannot be fixed should not be handed out (research of 14 October 2026, section 5, owner review copy). From December 2027 the EU Cyber Resilience Act expects security updates from whoever sells a connected product, and the UK PSTI regulations already require a published update period.

Facts this design depends on:

- **The kit has two app slots.** `default_16MB.csv` holds `otadata`, `app0` and `app1`, each 6,553,600 bytes. The Wi-Fi image is 933,361 bytes on Arduino-ESP32 2.0.17 ([ESP-CORE-001 record](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/dev/docs/core-3x-decision.md)).
- **App rollback is on in the pinned core.** `CONFIG_BOOTLOADER_APP_ROLLBACK_ENABLE` is set in 2.0.17's prebuilt `sdkconfig.h`. A new image boots as *pending verify*. If it is not marked valid before the next reset, the bootloader boots the previous slot ([ESP-IDF OTA, rollback](https://docs.espressif.com/projects/esp-idf/en/v4.4.7/esp32s3/api-reference/system/ota.html#app-rollback)). Arduino's `initArduino()` marks the image valid at once unless the sketch defines `verifyRollbackLater()` to return true.
- **Nothing in the pinned core checks a signature.** `CONFIG_SECURE_SIGNED_APPS_NO_SECURE_BOOT` is off in both 2.0.17 and 3.3.12, and the Arduino `Update` class checks an optional MD5 only ([Update.h](https://github.com/espressif/arduino-esp32/blob/2.0.17/libraries/Update/src/Update.h)). ECDSA P-256 is in the core's mbedTLS 2.28.7 (`CONFIG_MBEDTLS_ECDSA_C`, `CONFIG_MBEDTLS_ECP_DP_SECP256R1_ENABLED`).
- **A gateway reply is at most 2,048 bytes including the LF** ([protocol 0.1.0](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/protocol/0.1.0/README.md)). The gateway never sends unsolicited frames, so the gadget must ask for every piece.
- **Released firmware resets its session on any unknown reply field** (ADR 011, fact 4). Every new field must follow an opt-in in the gadget's hello.
- **The core decision.** ESP-CORE-001 compiled the kit on 2.0.17 and 3.3.12. 3.3.12 adds 163 KB to the Wi-Fi image and nothing this design needs. Recommendation: stay on 2.0.17 for Phase 12b and migrate later, over the air, on a spare board first.

## Decision

### 1. What an update is

An **update** is three files, made on the builder's computer:

| File | Content |
| --- | --- |
| `image.bin` | The application image exactly as the build writes it (`firmware.bin`). Never a bootloader, partition table or NVS. |
| `manifest.json` | The signed description, below. Compact UTF-8 JSON, keys sorted, at most 512 bytes. |
| `manifest.sig` | ECDSA P-256 signature over SHA-256 of the exact `manifest.json` bytes, DER encoded (at most 72 bytes). |

```json
{"board":"esp32s3-oled-kit-wifi","format":"grok-gadgets-update/1","key_id":"3f9a1c0b7d2e4a65","min_protocol":"0.1.0","sha256":"<64 hex>","size":933361,"version":"0.2.0-alpha.17"}
```

- `board` names the build (the PlatformIO environment). The gadget compares it with the board compiled into it.
- `version` is the string the gadget reports as `firmware_version` in its hello (1–32 characters). The kit's version comes from the build; the hard-coded `0.2.0-wifi` goes.
- `sha256` and `size` cover `image.bin`. The signature covers the manifest, and the manifest covers the image.
- `min_protocol` is the lowest device protocol the image speaks. A gadget refuses an image whose `min_protocol` it does not know.
- `key_id` is the first 16 hex digits of SHA-256 of the public key (DER). It lets the gadget and the relay name the key in messages; it is not a trust decision.

### 2. Keys

- The **builder** owns one signing key pair. `firmware keygen` makes it on the builder's computer: the private key in a PEM file with mode 0600, the public key beside it. The private key never goes to the relay, a repository, a log or Grok Bot.
- The **public key is compiled into the image** at build time, from a file the build points to. A build without a key has updates off and sends no `update` field. The SDK's published reproducible builds have no key, so their checksums stay comparable. A builder's own images contain the builder's key.
- A gadget trusts up to two keys, so a builder can rotate: ship an image that trusts the old and the new key, then sign with the new one.
- **Losing the private key ends updates** for every gadget that trusts only that key; they then need the cable. The guide tells the builder to back it up offline.

### 3. Delivery over the device connection

All additions are opt-in and additive. The protocol version stays **0.1.0**, as with claim codes.

- **Opt-in.** A gadget with a compiled key adds `"update": "ready"` to its hello. Only then may a reply carry update fields. A relay before this change answers the field with `invalid_request`; the gadget sends the hello again without it and does not ask again until the next boot. When a hello with both `claim` and `update` is refused, the gadget drops `update` first, then `claim`.
- **Offer.** When the operator has assigned an image to the gadget, its `version` differs from the hello's `firmware_version`, and this gadget has not refused or reverted that version, the hello reply carries:

  ```json
  "update": {"version":"0.2.0-alpha.17","size":933361,"chunk":1024,"manifest":"<base64>","signature":"<base64>"}
  ```

  A poll reply carries `update` only when the offer changed during the session (a new assignment, or `null` when withdrawn).
- **Chunks.** The gadget asks `{"type":"update_chunk","version":V,"offset":N}`. The reply is `{"ok":true,"data":"<base64>"}` with `chunk` bytes (the last one shorter). 1,024 bytes are 1,368 base64 characters, so a reply stays under 1,400 bytes. A 933 KB image is 912 chunks.
- **Order.** One request at a time, as today. During a download the gadget still polls at least once a second and sends ACKs and events first, so commands and the BOOT button keep working. A download pauses while a command runs.
- **Reports.** `{"type":"update_status","version":V,"status":S,"reason":R}`, where `status` is `started`, `verified`, `rejected`, `failed`, `applied` or `reverted`, and `reason` is one of `signature`, `board`, `version`, `size`, `protocol`, `sha256`, `write`, `link`, `not_online`, `boot` (optional). The relay logs each one.
- **Gateway limits.** At most 8 gadgets download at once on one relay (more get `busy` and retry with backoff); the existing 30 frames a second per gadget applies; chunks are read from disk per request, never held in memory; an image is at most 8 MiB; `offset` must be a multiple of `chunk` below `size`. A withdrawn or changed assignment answers `update_unavailable`, and the gadget abandons the download.
- **Resume.** None in Phase 12b. A download interrupted by a disconnect or a power cut starts again from zero at the next offer. The half-written slot is never marked bootable.

### 4. What the gadget checks, in order

1. The manifest signature, with each compiled key. No key matches: `rejected`/`signature`, nothing downloaded.
2. `format`, `board` (equal to the compiled board), `min_protocol` (known), `version` (not the running one and not one this gadget reverted, kept in NVS), `size` (fits the other slot). Any failure: `rejected` with the reason, nothing downloaded. Only a reverted version is refused for good: the relay stops offering the others after one report, and the builder may sign the same version again.
3. Download into the other slot with `Update.begin(size)` and `Update.write`, hashing every byte with SHA-256 as it arrives.
4. Before `Update.end()`: the byte count equals `size` and the hash equals `sha256`. Otherwise `Update.abort()`, `failed`/`sha256`, and the running image stays.
5. `Update.end(true)` (which also checks the image header), `verified`, restart.

The OLED kit shows `Update 42%` on its status row during the download and `Reverted` for one minute after a revert.

### 5. Automatic revert

- The new image defines `verifyRollbackLater()` to return true, so Arduino leaves it *pending verify*.
- It marks itself valid (`esp_ota_mark_app_valid_cancel_rollback()`) only after it is **Online through the relay**: a hello accepted and one poll answered. It then reports `applied`.
- If it is not Online within **5 minutes** of boot, it calls `esp_ota_mark_app_invalid_rollback_and_reboot()` and the previous image starts.
- If it crashes, hangs into the watchdog or loses power before it is valid, the bootloader boots the previous image at the next reset.
- The previous image notices the reverted slot (`esp_ota_get_last_invalid_partition()`), keeps that version in NVS so it never downloads it again, and reports `reverted` once it is Online. The relay stops offering that version to that gadget until the operator assigns it again.
- A relay outage during those 5 minutes also reverts a good image. That is the safe side; the operator assigns it again.

### 6. Operator CLI (gateway)

| Command | Where | What it does |
| --- | --- | --- |
| `firmware keygen --out KEY` | Builder's computer | Makes the key pair; prints the public key path and `key_id` |
| `firmware sign IMAGE --key KEY --board B --version V [--min-protocol 0.1.0] --out DIR` | Builder's computer | Writes `image.bin`, `manifest.json` and `manifest.sig` to `DIR` |
| `firmware add DIR --public-key PUB` | Relay host | Checks size, hash and signature against `PUB`, then copies the update into `firmware/BOARD/VERSION/` in the config directory |
| `firmware assign DEVICE VERSION` / `--none` | Relay host | Offers that version to one gadget, or withdraws the offer; assigning again clears a refused or reverted result |
| `firmware status [DEVICE]` | Relay host | Assigned version, reported version, last result with time and reason, download progress |
| `firmware list` / `firmware remove BOARD VERSION` | Relay host | Stored updates; a removed update is withdrawn everywhere |

`serve` re-reads the assignment file when it changes, as it re-reads device credentials. `serve` alone writes the status file. `firmware add --unchecked` stores an update without the signature check; it exists so an owner can prove that a gadget refuses a wrong key, and the guide says so.

Log lines, never with key material or image bytes: `update_offered`, `update_started`, `update_progress` (each 25 %), `update_verified`, `update_applied`, `update_rejected`, `update_failed`, `update_reverted`, `update_busy`, `update_withdrawn`, each with the device, the version and the reason.

### 7. Who may push

- Only the **relay operator** assigns updates, with the CLI on the relay host. There is no Grok Bot tool for updates in Phase 12b, and an account's owner cannot push or block one.
- Only images signed with a key compiled into the gadget run. The relay operator without the builder's key cannot make a gadget run their code; the builder without the relay cannot deliver.
- The stage-1 case is one person in both roles: the owner builds, signs and runs the relay.

### 8. Anti-rollback and secure boot (documented only)

- **Anti-rollback is off.** A gadget accepts any signed version that is not the running one, so an operator can go back to an older image on purpose. A relay operator, or an attacker who controls the relay, can also push an older signed image with a known flaw. ESP-IDF's eFuse secure version (`CONFIG_BOOTLOADER_APP_ANTI_ROLLBACK`, 16 versions at most on the ESP32-S3) prevents that. It burns eFuses and needs a custom bootloader build. The "Before you distribute" note lists it for sold products.
- **Secure boot and flash encryption are off on the kit.** Anyone with the board and a USB cable can flash any image and read NVS (ADR 005). The signature check protects the over-the-air path only. Secure boot v2 with signed apps is the documented path for sold products; it is irreversible and changes the published build checksums (ESP-IDENTITY-001).

## Threat model

| # | Threat | Control |
| --- | --- | --- |
| U1 | A relay, network or stored file serves a modified image | SHA-256 in the signed manifest, checked before `Update.end()`; the old image keeps running |
| U2 | An image signed with another key | Signature check before any download; `rejected`/`signature` logged on the relay |
| U3 | An image for another board | `board` in the signed manifest |
| U4 | A good signature on a broken image (crash, no Wi-Fi, wrong relay settings) | Pending-verify boot; valid only after Online; 5-minute limit; bootloader revert on reset |
| U5 | Power cut during download | The other slot is not bootable until `Update.end()`; restart from zero |
| U6 | Power cut during the trial boot | Bootloader boots the previous image |
| U7 | The same bad version offered again and again | The relay stops offering a version after `rejected`, `failed` or `reverted`; the gadget also keeps a reverted version in NVS |
| U8 | Downgrade to an older signed image | Not prevented (section 8); documented with the anti-rollback path |
| U9 | Stolen signing key | Not prevented. Rotation needs an image that trusts a new key, signed with the old one before it leaked, or the cable. The key stays off the relay. |
| U10 | Many gadgets downloading at once | 8 at a time, chunks read from disk, per-gadget frame limit |
| U11 | Downloads starve commands | Polls, ACKs and events go first; at least one poll a second |
| U12 | Released firmware breaks on new reply fields | Fields only after `"update": "ready"`; old relays fall back cleanly |
| U13 | Physical access | Not prevented on the kit (section 8) |

## The order: Phase 12b before Phase 12

1. Phase 11 shipped "Hand a gadget to someone". A handed-over gadget cannot be updated without the cable and the Mac.
2. The project says nothing about distributing gadgets before the compliance note and over-the-air updates exist (owner decisions of 14 October 2026). Batch labels first would multiply gadgets nobody can update.
3. Phase 12b closes on the owner's kit alone. Phase 12 needs an outside builder.
4. Phase 12b does not depend on the connector work in Phase 12 (gateway #176).

Phase 12 (relay init, labels, builder page, Linux remote transport, examples) follows.

## Owner decisions

Taken on 17 October 2026: the owner approved decisions 1–5 as recommended. Decision 6 is the owner's task in the acceptance; decision 7 is asked after the licence checklist.

1. **Order:** Phase 12b before Phase 12. Recommendation: yes.
2. **Who may push:** the relay operator with the CLI only. Recommendation: yes; a Grok Bot tool for owners to see or accept updates is a later phase.
3. **Core:** stay on Arduino-ESP32 2.0.17 for Phase 12b (ESP-CORE-001 no-go). Recommendation: yes.
4. **Anti-rollback on the kit:** off, documented only. Recommendation: yes.
5. **Revert limit:** 5 minutes to reach Online. Recommendation: yes.
6. **Signing key:** made on the Mac with `firmware keygen`, kept out of every repository, backed up offline by the owner.
7. **Release asset (#30):** whether the first signed kit binary ships as a release asset is asked separately, after the licence checklist (#294).

## Acceptance (Phase 12b)

Gateway tests for every rule above, and `rehearse` with a simulated gadget that downloads, verifies, restarts with the new version and reports `applied`. ESP32 host tests for the checks of section 4 and the revert rules of section 5. Then, on the owner's kit and relay, each with the owner's go-ahead:

- One last USB flash with the update-capable image.
- Relay backed up and upgraded to the candidate gateway.
- Push version N+1: the OLED shows progress, the kit restarts, goes Online, reports the new version in its hello, and Grok Bot shows text on it.
- An image signed with another key, and an image with one changed byte, are refused and logged.
- A signed image that never goes Online reverts by itself.
- A power cut during a download recovers.

The record goes to `docs/verification/ota-2026-10-DD.md`, each item Pass, Fail or Not tested, with gateway log lines and the owner's observations.

## Not in scope

The core migration, secure boot and flash encryption on the kit, delta or compressed images, resumable downloads, update scheduling, a Grok Bot update tool, Client ID Metadata Documents (gateway #176), long-poll (gateway #182), the Phase 12 builder kit, a shared relay, the Linux SDK and Home Assistant.
