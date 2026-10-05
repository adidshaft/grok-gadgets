# Grok Gadgets simulator kit

Use a virtual C124 RGB LED and button through the local Model Context Protocol (MCP) gateway. You do not need hardware, an API key, an exposed port or a hosted service. Original code uses Apache-2.0. This independent project is exclusively for Grok.

The [hosting FAQ](https://github.com/adidshaft/grok-gadgets/blob/main/docs/getting-started/hosting.md) explains who runs the gateway and tunnel. The kit provides local stdio MCP. It does not include a remote HTTPS MCP service. Do not expose its device port through a tunnel.

## Inspect first

The ZIP contains the Python wheel, source distribution (sdist), committed `source.tar`, installer, demonstration, settings, schema and license notices. It also contains `requirements.txt` with dependency hashes. The source archive includes `uv.lock`.

1. Inspect the source before you run code.
2. Compare the ZIP hash with the website's separate manifest.
3. Check `manifest.json` for the source commit, file hashes and sizes. `SHA256SUMS` also covers the manifest.

Hashes detect file changes. They do not prove who created the files.

`python3 install.py` checks the files. It does not install, download or start software.

`install.py --install` creates a new `.venv`. It downloads pinned runtime dependencies with hash checks. It then installs the included wheel without resolving more dependencies.

Installation uses isolated pip and needs matching binary wheels. It stops if those wheels are unavailable. It does not compile dependency source. On Apple Silicon, use native Python, not an Intel interpreter under Rosetta. Installation needs network access for the dependency wheels.

## Customize

1. Export `my-light.json` from the website. If download is unavailable, copy the displayed JSON into that file.
2. Copy the file into the extracted kit folder.
3. Pass `--config ./my-light.json` to use your settings.

You can also copy the bundled default to `my-light.json` and edit that copy with the included schema. Keep all original kit files unchanged for hash checks. Do not replace `simulator-config.json` with your export.

- Device ID and display name identify your virtual light.
- Starting RGB channels are integers 0–255; `on` is a boolean. Website brightness is converted into these channels; physical LED brightness is not being calibrated.
- Response delay is 0–2000 ms, applied before a simulated command acknowledgement.
- Offline startup lets you test an unavailable device. Reconnect resets the starting RGB/button state and creates a new session.
- No executable commands, credentials, network addresses or arbitrary capabilities belong in configuration.

## Try locally

Use Python 3.11+. The clean kit installation is tested with native Apple Silicon Python 3.11.15; Windows and Intel Mac kit installation remain unverified. In the extracted kit:

```sh
python3 install.py
python3 install.py --install --config ./my-light.json
.venv/bin/python try_simulator.py --config ./my-light.json
```

Omit `--config` to use the original default. Windows uses `.venv\Scripts\python.exe` for the last command. The demonstration calls MCP tools through the official local client. It checks results with assertions. It sends simulated button events, reconnects if needed, sets blue, then turns the light off.

This verifies local simulation. It does not verify Grok execution or physical operation. The demonstration enables test controls explicitly. Normal configuration excludes them.

## Experimental route to your existing Grok Bot

This route requires custom **Command MCP** in the Bot's cloud computer. Availability depends on the account and client. A developer-API conversation is not a substitute.

The dedicated desktop Bot reported simulator success on an earlier gateway build. A later installation of the configurable kit on the Bot's computer was observed. Neither a Bot-written report nor an installation record proves native tool invocation. Local MCP tests passed. Actual invocation records and mobile verification remain pending.

1. Inspect the kit.
2. Upload the ZIP, separate website hash manifest and exported configuration to the intended Bot.
3. Ask the Bot to unpack into a dedicated directory on its cloud computer, compare the ZIP hash, then run `python3 install.py` to verify contents. It must stop on a mismatch.
4. Ask it to install there with `python3 install.py --install --config /absolute/cloud/path/my-light.json`. This downloads hashed binary dependencies. Python 3.11+ and package access are required. The local Mac path cannot be used by the cloud computer.
5. Register only the simulator as a Command MCP server using the **absolute cloud executable path** printed by the installer, arguments `--simulator --simulator-config /absolute/cloud/path/my-light.json`, and empty environment. No listener, tunnel, account credentials or broader permissions are needed for the simulator. Do not weaken approval protections.
6. Ask for `gadgets_list_devices`, then `gadgets_get_state` using your configured ID. Ask: “Use the simulator connector to set my virtual light blue and read its command status and state.” Look for `simulated: true`, executed status and the matching blue state. Command receipts/diagnostics report `physical_verified: false`. Preserve actual tool evidence where the client exposes it; a Bot-written narrative alone is not independent verification.

The normal tools are:

- `gadgets_list_devices`
- `gadgets_get_state`
- `gadgets_command`
- `gadgets_command_status`
- `gadgets_read_events`
- `gadgets_diagnostics`

`rgb.set` is the only command capability. Button and state capabilities provide events or readings.

Start connected for normal use. Commands fail when the simulator starts disconnected. To test button, disconnect and reconnect operations, enable `--test-controls` explicitly. Remove it after the test. Button events do not promise automatic Bot activation.

Downloading the ZIP does not install a connector or change your account. The kit is not a hosted endpoint for Remote HTTPS MCP. A public authenticated gadget service, physical C124, Linux peripherals and Home Assistant need separate verification.

## Keeping the download current

The website build verifies the committed kit: gateway commit inside the manifest, input hashes, archive contents and the acceptance record. It does not rebuild the ZIP because a sibling gateway checkout moved.

Rebuild explicitly from the hub after gateway or kit-script changes:

```sh
python3 scripts/build-simulator-kit.py
python3 scripts/build-simulator-kit.py --check
.venv/bin/python website/build.py
```

`--check` fails if the sibling gateway HEAD, kit inputs or archive no longer match the stored kit. Uncommitted gateway changes are rejected. The rebuild runs the gateway tests and installs the kit in a fresh environment. It tests default and custom settings through the official MCP client.

Run these maintainer commands from the hub, not from the extracted kit.

A standalone hub checkout can use the stored kit if the archive and input hashes still match. Otherwise, use the gateway checkout to rebuild it. Rebuilds need internet access for dependencies. The build ID identifies the tested gateway source. The separate manifest lists artifact hashes.

The public website is deployed through the approved CI workflow. A gateway change does not update a downloaded copy or automatically change the hub's compatibility pin. Downloaded kits are fixed snapshots. They do not update or run code silently.
