# Support and verification matrix

This experimental alpha is exclusively for Grok. The [compatibility manifest](../../compatibility/tested-components.json) identifies tested versions and commits. The final candidate manifest identifies packaged commits. Simulation, compilation and command acknowledgements do not prove physical operation.

| Path | Software evidence | External acceptance still needed |
| --- | --- | --- |
| Browser playground | Local JavaScript model, customization/export tests, desktop and narrow-screen checks | Independent user reproduction; HTTPS routes and simulator download checked on 5 October 2026 |
| Simulator kit / gateway 0.1.0a1 | Fresh installer, protected defaults, custom configuration and official MCP discovery/command/error/retry/state/event checks; Python 3.11 baseline | Native Grok receipts; Windows and Intel Mac installation; independent human reproduction |
| Linux SDK 0.1.0a1 | Custom library/agent source and installed-package tests on macOS; isolated aarch64 Linux/Python 3.11 container acceptance | Real peripherals, systemd startup/recovery, other host architectures |
| ESP32 SDK 0.1.0 / C124 USB example | C++ host suites, canonical protocol, actual firmware-consumer simulated USB/PTY checks and ESP32-S3 cross-compilation | C124 flashing, USB enumeration, observed GPIO35 RGB and GPIO41 button, disconnect/recovery |
| Home Assistant diagnostics 0.1.0a1 | Read-only fixture/loopback MCP client and package tests; upstream MCP reuse | Real Home Assistant installation, selected exposed entities and Grok client acceptance |
| Existing Grok Bot | Dedicated computer installation observed; local-client acceptance remains separate | Inspectable native requests/results for the exact supported connector; mobile clients |
| Remote HTTPS MCP service | No Grok Gadgets implementation | Auth design, TLS, scoped access, isolation, revocation and negative tests before activation |
| Community recognition | Consent/identity/merged-contribution fixture logic, bounded offline tests | Approved identity backend, platform permissions and moderator activation |

Remote authenticated HTTPS/OAuth, device setup, Wi-Fi and voice entry points remain future work. The public website and daily repository-data refresh are active. Reddit has initial community content. A hosted gadget gateway and automatic contributor recognition are not active. Physical device operation remains unverified.

Record each new test in the appropriate issue. Include the exact version or hash. Remove private information from the evidence.

Use the [hosting FAQ](../getting-started/hosting.md) to separate local software acceptance, cloud reachability/native invocation, remote transport security and physical verification. A working tunnel or an HTTP response cannot close all four gates.

During publication setup, Intel Python 3.13 selected a cryptography source build. That build failed with the installed old Rust toolchain. Native arm64 Python 3.11 installed the pinned wheels and passed gateway and Home Assistant checks. Intel Mac setup remains unverified. This result does not mean that every Intel installation fails.
