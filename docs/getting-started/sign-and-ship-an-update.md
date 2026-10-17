# Sign and ship an update

This guide is for builders who run a relay for their gadgets. You sign a firmware image on
your computer and send it to gadgets through your relay, with no cable.

**Status:** Phase 12b ([ADR 012](../decisions/012-signed-updates.md)). On 17 October 2026 the
owner did these steps with one kit and one relay ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ota-2026-10-17.md)).
Nobody else has repeated them yet.

## What you need

- Gateway `0.1.0a16` or later on your computer and on your relay.
- ESP32 SDK `v0.2.0-alpha.17` or later, for example the OLED kit's `esp32s3-oled-kit-wifi`
  build.
- A USB cable, once per gadget, for the first update-capable image.

## 1. Make your signing key (once)

On your computer, not on the relay:

```sh
grok-gadgets-gateway firmware keygen --out ~/grok-gadgets-keys/builder.key
```

This writes `builder.key` (mode 0600) and `builder.pub.pem`, and prints the key ID. Back up
the private key offline. If you lose it, a cable is the only way to update gadgets that trust
only that key. Never put it in a repository, on the relay or in a chat.

## 2. Build and flash an update-capable image (once per gadget)

```sh
GROK_UPDATE_PUBLIC_KEY=~/grok-gadgets-keys/builder.pub.pem \
  .venv/bin/pio run -e esp32s3-oled-kit-wifi -t upload
```

The image reports the SDK version, for example `0.2.0-alpha.17`. Its console `status` shows
`"updates": "ready"`. Wi-Fi settings and the claim stay in the gadget.

## 3. Build and sign each new version

Give every image its own version, and sign it with the same version and board:

```sh
GROK_UPDATE_PUBLIC_KEY=~/grok-gadgets-keys/builder.pub.pem GROK_FIRMWARE_VERSION=0.2.0-alpha.17.1 \
  .venv/bin/pio run -e esp32s3-oled-kit-wifi
grok-gadgets-gateway firmware sign .pio/build/esp32s3-oled-kit-wifi/firmware.bin \
  --key ~/grok-gadgets-keys/builder.key --board esp32s3-oled-kit-wifi \
  --version 0.2.0-alpha.17.1 --out update-0.2.0-alpha.17.1
```

Copy the `update-0.2.0-alpha.17.1` directory and `builder.pub.pem` to the relay host.

## 4. Store and send it (relay host)

```sh
grok-gadgets-gateway firmware add update-0.2.0-alpha.17.1 --public-key builder.pub.pem
grok-gadgets-gateway firmware assign GADGET-ID 0.2.0-alpha.17.1
grok-gadgets-gateway firmware status
```

`add` refuses a wrong signature or a changed image. The gadget gets the offer at its next
poll. `firmware status` then shows `downloading`, then `applied`. The request log has
`update_offered`, `update_progress`, `update_verified` and `update_applied` lines.

| Status | Meaning | Do this |
| --- | --- | --- |
| `rejected (signature)` | The gadget does not trust that key | Sign with the key compiled into the gadget |
| `rejected (board)` | Wrong `--board` | Sign again with the gadget's build name |
| `failed (sha256)` | The image changed after signing | Copy the update again and `firmware add` it |
| `reverted (not_online)` | The new image did not reach the relay within 5 minutes | Fix the image; sign it as a new version |
| `reverted (boot)` | The new image crashed or lost power on trial | Fix the image; sign it as a new version |

A gadget never downloads a version it reverted, even if you assign it again.

## 5. Before you give gadgets away

- Decide and publish how long you will ship security updates.
- Keep the relay running and the key safe for that time.
- Read [Before you distribute a gadget](before-you-distribute.md) and the
  [firmware licence checklist](firmware-licences.md).

## Limits

- Anti-rollback is off. Any signed version other than the running one, and other than a
  reverted one, is accepted.
- Secure boot and flash encryption are off on the kit. Anyone with the board and a cable can
  flash it. The signature protects the over-the-air path only.
- A download that stops starts again from the beginning.
- At most 8 gadgets download at once from one relay.

More detail: the gateway's [signed updates guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/updates.md)
and the ESP32 SDK's [updates page](https://github.com/adidshaft/grok-gadgets-esp32-sdk/blob/main/docs/updates.md).
