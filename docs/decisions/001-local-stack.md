# ADR 001 — local alpha stack

Use Python official MCP SDK for gateway, Python separately installable Linux SDK, reusable C++ ESP32 SDK with pinned manufacturer-supported board toolchain, upstream Home Assistant MCP, and a dependency-light static website generated from canonical repository content. Device protocol 0.1.0 canonical schemas live in gateway; SDK copies must record source hash/version.

Loopback TCP and USB use newline-delimited JSON, 16 KiB maximum line. A hello registers identity/boot/capabilities; poll retrieves commands; ack records execution; state/events/heartbeat report observations. USB bridge injects host-stored device credential. Device acknowledgement does not prove physical effect. Remote authenticated Grok deployment is an external gate.
