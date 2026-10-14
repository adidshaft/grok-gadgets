# Phone-only setup — 14 October 2026

Phase 10 ([#266](https://github.com/adidshaft/grok-gadgets/issues/266), [ADR 010](../decisions/010-phone-setup.md)). The owner's ESP32-S3 OLED kit was factory-provisioned once on the Mac. The owner then joined it to home Wi-Fi with an iPhone alone: the kit on a USB charger, the Mac closed, no app. The kit reached **Online** through the relay, and Grok Bot on the iPhone showed text on it. Times are UTC. The owner authorized flashing and provisioning.

Evidence levels:

- **Log**: the relay's request log, read after each step.
- **Console**: the kit's USB console `status` reply (only while it was on the Mac).
- **Owner**: what the owner saw, with screenshots kept privately.

| Item | Value |
| --- | --- |
| Relay | The Phase 9 relay, unchanged: gateway `0.1.0a13`, device port 8443, `devices.example.net` DNS-only. No change on the server or DNS |
| Firmware | ESP32 SDK `dev` commit `7aa72de` (`esp32s3-oled-kit-wifi`): static RAM 108,076 B, flash 932,617 B |
| Provisioning | Gateway `dev` commit `0808844`: `factory-provision /dev/cu.usbmodem… --device oledkit-… --gateway devices.example.net:8443 --ca … --credentials …`, run from a separate worktree, with the relay CA and registry copied into a private 0700 folder |
| Phone | iPhone, iOS camera and the captive sheet; mobile data on |
| Home network | The owner's 2.4 GHz network; its name stays private |

## Before the phone

| Time | What happened | Source |
| --- | --- | --- |
| 09:40 | After flashing, the old Phase 9 settings (full `grok-wifi` record) came back **Online**: `factory: false`, free heap 182,340 B | Console |
| 09:40 | `relay-check devices.example.net:8443`: DNS-only record, the relay CA on the port | Mac |
| 09:40 | `factory-provision`: preflight passed, board checked, identity and label values sent; label printed and written as SVG, PNG and text | Mac |
| 09:40 | Still **Online** with `factory: true`: a full USB record takes precedence, as designed | Console |
| 09:40:52 | `factory_reset` over the console: `grok-wifi` erased, factory identity kept | Console |
| 09:40:58 | `provisioned: false`, `factory: true`, `setup: open`, free heap 215,468 B | Console |

## With the phone

| Time | What happened | Source |
| --- | --- | --- |
| ~09:51 | The kit, still on the Mac's USB, closed its hotspot after 10 minutes: `setup: closed`. The OLED showed `Setup closed` and `Power cycle`. The iPhone's QR join then reported "Unable to join the network" | Console, Owner |
| ~09:53 | The owner moved the kit to a USB charger (power cycle). The OLED showed the setup screen again | Owner |
| ~09:54 | The owner scanned the label's QR code with the iPhone camera and joined `GrokGadget-XXXX`. The captive sheet opened at `192.168.4.1`, entered the setup code, picked the home network and typed its password | Owner |
| 09:55:03 | `device_connected`, `device_hello` from the kit on port 8443 | Log |
| 09:55 | Page: "Done. The gadget is Online. You can close this page." OLED: `Online`, `Grok Bot`, the face | Owner |
| 10:02:29 | `gadgets_command` `display.text` from Grok Bot on the iPhone, remote, `executed`, `ok` | Log |

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Label QR joins the hotspot on the iPhone | Pass | Owner |
| Captive page opens; setup code accepted; home Wi-Fi picked | Pass | Owner |
| Online through the relay, no computer | Pass | Log `device_hello` 09:55:03, Owner |
| Grok Bot on the iPhone shows text | Pass | Log 10:02:29, Owner: "Phone setup works" on the OLED |
| Setup window expires after 10 minutes | Pass | Console `setup: closed`, Owner |
| Wrong setup code refused | PENDING | |
| Wrong home password shown | PENDING | |
| BOOT reset, then re-join | PENDING | |
| Same flow on Android | PENDING | |

## Notes

- The relay runs gateway `0.1.0a13`, so its log lines have no `protocol` field yet (GW-COMPAT-001 is in the next release).
- Grok Bot's connector backend made the call; its self-reported client name is not recorded here.
- A kit on the computer's USB counts down its window too. Move it to the charger just before scanning.
- `factory-provision` said the board would open its hotspot while the board still had its old full Wi-Fi record. Fixed in gateway [#184](https://github.com/adidshaft/grok-gadgets-gateway/pull/184).
