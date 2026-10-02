# Grok Gadgets0.1.0-alpha.1 — corrected unpublished candidate

An independent local alpha exclusively for the existing Grok Bot: gateway and simulator, separate Linux/ESP32 SDKs, AtomS3 Lite C124 USB firmware compilation, upstream Home Assistant diagnostics, interactive website and offline community preparation.

Corrections: immutable firmware ACK retries; command/input capability distinction; per-device/boot event retention; installed custom Linux factories (including annotated dataclasses); persistent honest activity cache and stale-build classification; safe semantic documentation with working source-relative links and static diagrams. See compatibility/tested-components.json and docs/verification/hardening-handoff.md for exact evidence. Final candidate manifest records source archives, complete Git history bundles, rebuilt Python distributions, firmware build provenance and website hashes.

Verified locally:21gateway tests,20Linux source tests,13Home Assistant tests,3ESP host suites plus real firmware consumer/USB PTY and compilation,12website tests,6community tests and12integrated groups. Installed custom factories pass macOS and actual offline Linux. Independent agent review resolved its two additional material findings.

Pending: actual Grok desktop/mobile tools, physical C124, actual home entities, real systemd/peripherals, another human reproducing setup and public/community activation. Remote HTTPS/OAuth is unimplemented; Wi-Fi requires separate secure design. Bounded queues/retries do not guarantee durable exactly-once execution. Firmware dependency redistribution obligations must be reviewed before release uploads.

Version remains0.1.0-alpha.1 because no earlier candidate was published. No public tag or release exists. Install from component READMEs; begin with simulation. Hosting the static site does not run a gateway or identity service.
