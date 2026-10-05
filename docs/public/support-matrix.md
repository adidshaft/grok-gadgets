# Support and verification matrix

This is an experimental software alpha exclusively for Grok. The [compatibility manifest](../../compatibility/tested-components.json) pins the tested versions/commits; the final candidate manifest identifies exact packaged HEADs. A successful simulation, compilation or ACK does not establish physical operation.

| Path | Software evidence | External acceptance still needed |
| --- | --- | --- |
| Browser playground | Local JavaScript model, customization/export tests, desktop and narrow-screen checks | Public HTTPS download behavior after approved deployment |
| Simulator kit / gateway 0.1.0a1 | Fresh installer, protected defaults, custom configuration and official MCP discovery/command/error/retry/state/event checks; Python 3.11 baseline | Native Grok receipts; Windows and Intel Mac installation; independent human reproduction |
| Linux SDK 0.1.0a1 | Custom library/agent source and installed-package tests on macOS; isolated aarch64 Linux/Python 3.11 container acceptance | Real peripherals, systemd startup/recovery, other host architectures |
| ESP32 SDK 0.1.0 / C124 USB example | C++ host suites, canonical protocol, actual firmware-consumer simulated USB/PTY checks and ESP32-S3 cross-compilation | C124 flashing, USB enumeration, observed GPIO35 RGB and GPIO41 button, disconnect/recovery |
| Home Assistant diagnostics 0.1.0a1 | Read-only fixture/loopback MCP client and package tests; upstream MCP reuse | Real Home Assistant installation, selected exposed entities and Grok client acceptance |
| Existing Grok Bot | Dedicated computer installation observed; local-client acceptance remains separate | Inspectable native requests/results for the exact supported connector; mobile clients |
| Community recognition | Consent/identity/merged-contribution fixture logic, bounded offline tests | Approved identity backend, platform permissions and moderator activation |

Remote authenticated HTTPS/OAuth and provisioning, Wi-Fi, and voice entry points are future work. No public service, real device, Reddit action or unattended automation is enabled. Record additional acceptance through the appropriate issue form with exact version/hash and safely redacted evidence.

During fresh publication setup, an Intel Python 3.13 environment selected a cryptography source build and failed with the installed old Rust toolchain. The native arm64 Python 3.11 environment installed the pinned wheels and passed gateway/Home Assistant checks. Intel Mac setup remains unverified; this is not a claim that every Intel installation fails.
