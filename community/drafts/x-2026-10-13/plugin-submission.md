# Grok Bot plugin submission

Open: https://x.ai/bot/marketplace/submit-a-plugin

First name: Aman
Last name: Pandey
Work email: adidshaft@kyokasuigetsu.xyz
Organization name: Kyoka Suigetsu
Organization handle: adidshaft
Website: grokgadgets.org
Logotype URL: https://raw.githubusercontent.com/adidshaft/grok-gadgets/main/docs/visuals/brand/logo-1024.png
Listed on: Grok Bot only
MCP server / repo: https://github.com/adidshaft/grok-gadgets-gateway

Brief description:

Grok Gadgets lets Grok Bot control real hardware. An open source MCP gateway gives Grok Bot six tools (list devices, send a command, check command status, read state, read events, diagnostics) for gadgets built with its ESP32, Linux/Raspberry Pi and Home Assistant SDKs.

Grok Bot signs in with OAuth, devices connect outward over TLS, and every sign-in can be revoked. Verified natively from the Grok Bot iPhone and Mac apps driving a real ESP32-S3 OLED. Apache-2.0, early alpha.

Testing instructions:

No hardware: pip install --pre grok-gadgets-gateway, then run init, serve --simulator and rehearse.
In-app: expose the gateway over HTTPS (docs/remote-access.md in the repo), add it in Grok Bot as a custom MCP server, approve sign-in with grok-gadgets-gateway oauth approve CODE, then ask Grok Bot to list your gadgets.
Guide: grokgadgets.org

Then tick "I've tested this plugin locally and in-app" and tap Submit Plugin.
