# Grok Gadgets

Independent, Apache-2.0 gadgets exclusively for the existing Grok Bot. **Unpublished local alpha**: simulator/MCP acceptance, separately useful Linux and ESP32 SDKs, C124 firmware compilation, Home Assistant integration diagnostics, website and community preparation.

Actual Grok connectivity, mobile clients and physical hardware remain unverified. The target is M5Stack AtomS3 Lite C124 with a USB-C data cable. Linux SDK software passed on actual Linux Docker; that does not verify physical peripherals or systemd.

Five sibling repositories: this project hub, [gateway](../grok-gadgets-gateway/README.md), [Linux SDK](../grok-gadgets-linux-sdk/README.md), [ESP32 SDK](../grok-gadgets-esp32-sdk/README.md), [Home Assistant](../grok-gadgets-home-assistant/README.md).

Run the local acceptance suite:

```sh
python3 scripts/check-all.py
```

Run the simulator demo:

```sh
cd ../grok-gadgets-gateway
uv sync --locked
uv run python -m grok_gadgets_gateway.demo
```

Website from the hub:

```sh
python3 website/build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory website/dist
```

Open http://127.0.0.1:4173. Developer lint: `uvx --from ruff==0.14.14 ruff check scripts website community`; formatting: replace check with `format --check`. No publication occurs.

[Complete local handoff and external gates](docs/verification/local-handoff.md) · [compatibility](compatibility/tested-components.json) · [roadmap](planning/milestones.json) · [labeled issues](planning/issues.json) · [publication package](publication/README.md) · [commit histories](publication/commit-summary.md) · [implementation brief](docs/implementation-plan.md).

Community policies/drafts and tested offline recognition logic are in [community](community/README.md). No live Reddit change or ongoing automation is active. No public repositories, push, deployment or paid calls were made. Independent project; no xAI affiliation implied.
