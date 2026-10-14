# ADR 010 — Phone-only Wi-Fi setup: a setup hotspot with a captive page

**Date:** 14 October 2026

**Status:** Proposed. The owner decides; acceptance needs the Phase 10 record.

**Owner:** Grok Gadgets hub (`adidshaft/grok-gadgets`)

**Issues:** hub [HUB-ADR-010 #265](https://github.com/adidshaft/grok-gadgets/issues/265), [HUB-SETUP-001 #266](https://github.com/adidshaft/grok-gadgets/issues/266); ESP32 [ESP-SETUP-001 #114](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/114), [ESP-SETUP-002 #115](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/115), [ESP-ONBOARD-001 #72](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/72), [ESP-CORE-001 #124](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/124); gateway [GW-SETUP-001 #158](https://github.com/adidshaft/grok-gadgets-gateway/issues/158)

## Context

[ADR 009](009-relay-route.md) put the gateway on an always-on relay. Gadgets connect out to it from any home network. One step still needs a computer: `wifi-provision` sends the Wi-Fi name and password, the device token, the relay name and the CA over USB.

The goal of Phase 10: a person who received a gadget joins it to their home Wi-Fi **with a phone alone**. They use no computer, no app and no account. The gadget then shows **Online** through the relay. The builder prepares the gadget once, at the factory, with a computer.

The person has an iPhone or an Android phone with its normal camera and browser. The gadget is an ESP32-S3 on Arduino-ESP32 2.0.17 (ESP-IDF 4.4.7), with a small OLED and a BOOT button. Some gadgets will have no display.

Constraints from the research of 14 October 2026:

- iPhone Safari has no Web Bluetooth and no Web Serial. On iPhone, BLE setup needs an app.
- The pinned core offers ESP-IDF provisioning Security 0 and 1 only. Security 2 (SRP6a) needs ESP-IDF 5 (ESP-CORE-001).
- The UK PSTI regulations and EN 18031 refuse universal default passwords. One shared hotspot password for every gadget is not acceptable.
- iOS and Android both join a network from a `WIFI:T:WPA;S:…;P:…;;` QR code in the camera app.
- Both phones probe for a captive network after they join one. iOS then opens a sign-in sheet; if it does not, the person opens `captive.apple.com` or the page address in the browser.

## Options

| Option | Phone needs | iPhone | Android | Secret on the air | Cost on the kit |
| --- | --- | --- | --- | --- | --- |
| **A. Setup hotspot + captive page** | Camera and browser | Yes | Yes | WPA2 with a per-device passphrase | Wi-Fi AP, DNS, a small HTTP server |
| B. BLE Improv | An app on iPhone; Chrome on Android | App only | Chrome | None of its own | BLE stack (Bluedroid), more RAM |
| C. ESP-IDF provisioning apps (SoftAP or BLE) | A vendor app | App only | App only | Security 1 (X25519 + proof of possession) | `WiFiProv` library |
| D. Web Serial over USB | A computer, or Chrome on Android with a cable | No | Cable | Cable | Already exists (`wifi-provision`) |
| E. WPS push button | Router support | Router | Router | WPS | WPS is often off or removed |

Only **A** works on both phones with nothing installed. B and C need an app on iPhone. D needs a cable. E depends on the router, and many routers disable WPS.

## Proposed decision

Use **A**: a setup hotspot with a captive page, protected by per-device secrets on a printed label. BLE (B) stays a documented builder option for a later phase.

### The label

The builder prints one label per gadget at the factory (`grok-gadgets-gateway factory-provision`, GW-SETUP-001). It shows:

- the hotspot name, `GrokGadget-` and the last four characters of the device ID, for example `GrokGadget-89AB`;
- the hotspot passphrase: 16 characters from a 32-character alphabet without look-alike characters (80 bits);
- a `WIFI:T:WPA;S:GrokGadget-89AB;P:…;;` QR code, so the phone joins by scanning;
- the setup code: 8 characters from the same alphabet, written `XXXX-XXXX` (40 bits);
- the device ID and the page address, `http://192.168.4.1`.

The gadget stores these values in its factory settings. A lost label is reprinted from the builder's records; the identity does not change.

### Factory settings and user settings (ESP-SETUP-002)

- Flash storage splits into two namespaces. `grok-factory` holds the device token, the relay name and port, the CA, the hotspot passphrase and the setup code. `grok-wifi` holds the home Wi-Fi name and password, and later the claim state.
- `factory-provision` writes `grok-factory` over USB once. It never asks for home Wi-Fi.
- A BOOT reset (hold 10 s) and the console `factory_reset` wipe `grok-wifi` only. The gadget keeps its identity and opens the setup hotspot again.
- A gadget provisioned before Phase 10 (everything in `grok-wifi`) keeps working: the firmware reads the old layout when `grok-factory` is empty.

### The setup window

- The hotspot opens only while `grok-wifi` is empty: on first power-on, or after a BOOT reset.
- It stays open for **10 minutes** after power-on, then closes. A power cycle opens a new window while the gadget is still unprovisioned.
- It closes after a successful join. Once joined, the gadget never opens the hotspot again until a BOOT reset. A stranger cannot reopen it from outside.
- The display shows the hotspot name, "Scan the label" and the minutes left. A gadget without a display blinks its status light.

### The captive page (ESP-SETUP-001)

- WPA2-PSK on the hotspot, with the label passphrase. Plain HTTP on `192.168.4.1` inside the hotspot: the phone would not trust a certificate in a captive sheet, and WPA2 protects the link.
- A DNS server answers every name with `192.168.4.1`, so the phone's captive check finds the page.
- The page asks for the setup code first. It accepts Wi-Fi details only with the right code. It compares the code in constant time.
- It lists nearby 2.4 GHz networks from a scan, with a field for a hidden network name, and a password field.
- After a submit it shows live status: joining, joined, Online through the relay, or a reason it failed. The reasons come from the existing join diagnosis (ESP-WIFI-DIAG): wrong password, network not found, timed out. The display shows the same.
- The page never shows stored values: not the home Wi-Fi name or password, the token, the passphrase or the setup code.
- Rate limits: after 5 wrong setup codes, the page refuses codes for 1 minute, then for twice as long after each further wrong code. After 20 wrong codes the hotspot closes until a power cycle.
- One phone at a time: the hotspot allows one station.

### What happens after the join

The gadget saves the home Wi-Fi details in `grok-wifi` and closes the hotspot. It then connects to the relay with the factory token, name and CA (ADR 009), exactly as a USB-provisioned gadget does. The relay logs `device_hello`; the display shows **Online**. The person's Grok Bot uses the gadget through the relay as before.

## Threat model

| Threat | Mitigation | Remaining risk |
| --- | --- | --- |
| A stranger nearby joins the hotspot during setup | Per-device WPA2 passphrase; the hotspot opens only while unprovisioned, for 10 minutes | Someone who reads the label in that window |
| A stranger guesses the setup code | 40-bit code, rate limits, hotspot closes after 20 wrong codes | None practical |
| A neighbour re-provisions a working gadget | No hotspot once joined; only a physical BOOT reset reopens it | Physical access to the gadget |
| Evil twin hotspot that captures the home password | The label names the exact hotspot and device ID; the phone joins by QR with the passphrase, so a twin needs the passphrase too | A person who joins a look-alike name by hand |
| Sniffing the home Wi-Fi password | WPA2 on the hotspot; the password goes to the gadget only, never to the relay | — |
| Reading secrets from the gadget | Out of scope: flash encryption is off (ADR 005). Whoever holds the board can read the token and Wi-Fi password | Documented; hardware identity is ESP-IDENTITY-001 research |
| A lost or copied label | Reprint from the builder's records; after a BOOT reset, the label works again, so treat it like a key | A copied label plus physical access |
| Universal default password rules (PSTI, EN 18031) | Every gadget has its own passphrase and setup code | — |

## Consequences

- No app, no account and no computer for the person who sets up the gadget. One computer step stays with the builder: `factory-provision` over USB.
- The label is a secret. Builders must not photograph it into public listings.
- The firmware grows: soft AP, DNS server and HTTP server. ESP-SETUP-001 records the RAM and flash cost of the Wi-Fi build.
- Station and hotspot share one radio. While the gadget tries the home network, the hotspot may move to the home network's channel and the phone may drop for a few seconds. The page and the display both show the result, so a dropped page is not a lost result. The Phase 10 record tests this on iPhone and Android.
- Claim codes and accounts stay in Phase 11 (ADR 011). Phase 10 gadgets belong to the relay operator, as in ADR 009 stage 1.

## Acceptance

Accepted when the Phase 10 record (`docs/verification/phone-setup-2026-10-DD.md`) shows, on the owner's kit with the computer closed, with relay log lines and the owner's observation:

- Pass: label scanned on an iPhone, setup code entered, home Wi-Fi picked, **Online** through the relay, and Grok Bot on the iPhone shows text on the kit.
- Recorded: a wrong home password shown; the window expiring; a wrong setup code refused; a BOOT reset then a new join; the same flow on Android if a phone is available. Each item is Pass, Fail or Not tested.

## Not decided here

Claim codes and accounts (ADR 011), over-the-air updates (Phase 12b), the core migration (ESP-CORE-001, research only), and a shared relay (Phase 13).
