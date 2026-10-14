# Factory-provision and label a gadget

This guide is for builders. You prepare each gadget once with a computer. The person who gets
the gadget then sets it up with a phone alone ([Set up your gadget with your phone](phone-setup.md)).

**Status:** Phase 10 ([ADR 010](../decisions/010-phone-setup.md)). On 14 October 2026 the owner set up one kit this way with an iPhone and with an Android phone ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/phone-setup-2026-10-14.md)). Nobody else has repeated it yet.

## What you need

- A relay that runs your gateway ([Run the gateway away from your Mac](mac-free-route.md)).
- Gateway `0.1.0a14` or later on your computer, and the relay's `lan/ca.pem`.
- ESP32 SDK firmware with the setup hotspot (`v0.2.0-alpha.15` or later), for example the OLED
  kit's `esp32s3-oled-kit-wifi` build.
- A USB data cable.

## 1. Check the relay

```sh
grok-gadgets-gateway relay-check devices.example.net --ca relay-ca.pem
```

The device name must be a DNS-only record. A proxied record breaks every gadget's CA pin. New
relays use port 8444; a relay set up before 14 October 2026 uses 8443 (add `:8443`).

## 2. Enroll and flash

On the relay, enroll the gadget: `grok-gadgets-gateway enroll oledkit-0123456789ab`. Copy the
relay's `credentials.json` to your computer as `relay-credentials.json`, and keep it private.

Flash the firmware over USB, for example:

```sh
.venv/bin/pio run -e esp32s3-oled-kit-wifi -t upload
```

## 3. Factory-provision

```sh
grok-gadgets-gateway factory-provision /dev/cu.usbmodem101 --device oledkit-0123456789ab \
  --gateway devices.example.net --ca relay-ca.pem --credentials relay-credentials.json
```

The command checks the relay and the board. It sends the gadget's identity: the device token,
the relay name and port, and the CA. It adds a new hotspot passphrase and setup code. It never
sends Wi-Fi details.

It prints the label and writes three files in `labels/`: text, a Wi-Fi QR PNG and a printable
90 × 50 mm SVG. Print the SVG and stick it on the gadget or its box.

## 4. Check the gadget

The gadget restarts and shows `Setup 10 min` and its hotspot name. Scan the label once with a
phone to check it, then reset with BOOT (10 seconds) before you hand the gadget over.

## Keep the label safe

- The label is a secret. Do not show it in photos or listings.
- Records stay in `labels/` in your config folder, mode 0600. `grok-gadgets-gateway label ID`
  prints a lost label again.
- `factory-provision --replace` writes a board again with the same label. `--new-label` makes
  new values; the old label then stops working.
- Delete `relay-credentials.json` after provisioning: it holds every device token.

## Limits

- Flash encryption is off. Anyone who holds the gadget can read its token and Wi-Fi password.
- One phone at a time can join the setup hotspot.
- Claim codes and accounts come in Phase 11. Until then every gadget belongs to the relay operator.
