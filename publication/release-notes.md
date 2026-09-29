# Grok Gadgets 0.1.0-alpha.1 — proposed unpublished release

A self-hosted local alpha exclusively for the existing Grok Bot direction: gateway/MCP software C124 simulator, separate Linux and ESP32 SDKs, C124 USB firmware compilation, upstream Home Assistant integration diagnostics, source-driven project website, and offline opt-in recognition logic.

See compatibility/tested-components.json and docs/verification/local-handoff.md for exact commits and observed test evidence before approval. Simulation, build, runtime, actual Grok, physical, and independent reproduction are different claims.

Known limitations: no actual Grok desktop/mobile verification, no physical C124 observations, no real Home Assistant entities, no independent second tester, no approved remote connection or public deployment, no activated identity backend or Reddit app. Wi-Fi requires a secure supported transport and is tracked separately. Alpha framing, queues, and deduplication are bounded; no durable exactly-once execution guarantee.

Install from component READMEs. Begin with the gateway demo before hardware. Closing a client does not necessarily stop the gateway; shutting down its host does. Static website hosting cannot run the gateway or identity-linking service.
