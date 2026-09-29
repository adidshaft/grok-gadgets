# Architecture and verification boundaries

The existing Grok Bot invokes MCP tools on the gateway. The gateway routes device commands to separately useful Linux and ESP32 SDK applications. Home Assistant uses its upstream MCP server directly where appropriate.

Canonical protocol 0.1.0 is owned by the gateway. Loopback TCP and USB bridge use 2048-byte LF-delimited JSON; credential injection happens on the host. Firmware stores no network credential. Device registration includes boot identity and capabilities. Poll returns at most one command, ack reports execution, and state/event frames report observations. Cursor epochs explicitly expose restart and dropped-history errors. Queues and deduplication windows are bounded.

Simulation controls require explicit opt-in and are absent from default MCP tool discovery. Simulator outputs label themselves. Device acknowledgement remains separate from human-observed physical effect. No remote endpoint, tunnel, paid API conversation, or alternative AI backend exists in this alpha.

The Grok cloud route cannot run a path on the local Mac. Actual account-level MCP transport/authentication/reachability and desktop/mobile observations remain separate gates. See the sibling Home Assistant feasibility record for current official-source findings.
