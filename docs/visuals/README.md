# Visual sources and evidence

Original project vectors, created from maintained architecture and board records. Each flow has an editable `.mmd` source; SVG cards provide an accessible static explanation rather than a runtime-dependent diagram. Read order follows the visible numbers. The contribution and no-hardware sequences are ordered; the responsibility map lists separate owners.

The overview lists the browser, export, kit, gateway and SDK software. Grok native receipts, the authenticated cloud-to-local route and real Home Assistant remain separate pending paths; Home Assistant can connect directly to Grok using upstream MCP. The command lifecycle ends with a distinct physical observation that cannot be inferred from an ACK.

[ESP32-S3 kit reference](esp32-s3-kit-reference.svg) is an original conceptual illustration. It shows the ordered AYWHP ESP32-S3 DevKitC-style board with ESP32-S3-WROOM-1-N16R8 and USB-C, ApTechDeals 840-point breadboard and jumper wires, and Robocraze 0.96-inch 128×64 OLED advertised as SPI/I²C with four pins. It is not a wiring guide. Board pin mapping, display controller, voltage and interface must be confirmed after delivery. An external LED and button are optional additional parts if the board has no suitable built-in parts. The current light simulator does not prove OLED operation.

![Actual browser customization/export panel.](simulator-playground.jpg)

This screenshot was captured from the running local website on 5 October 2026, with the actual customization/export panel open. It shows software simulation only, no account information or physical device. The exported `my-light.json` document was saved from the visible JSON fallback; a browser download-event capture timed out. SHA256 of the image: `c3215addc08a33a6d12b72727f9a034ca96c2743bd1ad26159bac70ac39a7dd2`. [Community artwork provenance](brand-provenance.md) distinguishes original artwork from third-party reference marks.
