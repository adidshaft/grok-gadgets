# Grok Gadgets simulator kit

Apache-2.0 original code. A virtual C124 RGB LED and button, through the real MCP gateway. No hardware, API key, exposed port or hosted service is required. This is an independent Grok-only project.

## Inspect first

The ZIP includes the wheel, sdist, exact committed `source.tar`, `uv.lock` inside that source, hashed `requirements.txt`, this readable installer/demo, default settings, schema and license notices. See `manifest.json` for source commit, hashes and sizes; `SHA256SUMS` also covers the manifest. Compare the ZIP hash with the website's separate manifest before trusting it. Hashes detect changed files, not a trusted author by themselves.

`python3 install.py` verifies the files; it does not install, download or start anything. `install.py --install` is an explicit opt-in that creates a new `.venv`, downloads pinned runtime dependencies with hash checking, and installs the included wheel without dependency resolution. Inspect source before running code. Installation uses isolated pip and requires matching binary wheels; it stops rather than compiling dependency source. On Apple Silicon, use native Python rather than an Intel interpreter under Rosetta. Runtime dependency wheels are downloaded during installation; this ZIP is not a fully offline dependency cache.

## Customize

Export `simulator-config.json` from the website, or copy/edit the default using the included schema. Keep the original kit files unchanged for hash verification; put customized settings in a separate file such as `my-light.json`.

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

Omit `--config` to use the original default. Windows uses `.venv\Scripts\python.exe` for the last command. The demonstration calls real MCP tools using the official local client and prints assertion-backed simulated results. It injects test-only button events, reconnects if needed, sets blue and ends off. This proves local simulated MCP behavior, not that Grok invoked anything or that a physical device operated. Test controls are opt-in for that demonstration only; ordinary configuration excludes them.

## Use your existing Grok Bot

Requires an account/client that offers custom **Command MCP** in the Bot's cloud computer. Availability is account-dependent. No developer-API conversation is substituted. Our dedicated desktop Bot reports successful simulator operation on an earlier gateway build. This configurable kit is locally MCP-tested and has not been run inside Grok; inspectable invocation receipts and mobile verification remain pending.

1. Inspect the kit. Upload the ZIP, its separate website hash manifest and your exported configuration to the Bot you intend to use.
2. Ask the Bot to unpack into a dedicated directory on its cloud computer, compare the ZIP hash, then run `python3 install.py` to verify contents. It must stop on a mismatch.
3. Ask it to install there with `python3 install.py --install --config /absolute/cloud/path/my-light.json`. This downloads hashed binary dependencies. Python 3.11+ and package access are required. The local Mac path cannot be used by the cloud computer.
4. Register only the simulator as a Command MCP server using the **absolute cloud executable path** printed by the installer, arguments `--simulator --simulator-config /absolute/cloud/path/my-light.json`, and empty environment. No listener, tunnel, account credentials or broader permissions are needed for the simulator. Do not weaken approval protections.
5. Ask for `gadgets_list_devices`, then `gadgets_get_state` using your configured ID. Ask: “Use the simulator connector to set my virtual light blue and read its command status and state.” Look for `simulated: true`, executed status and the matching blue state. Command receipts/diagnostics report `physical_verified: false`. Preserve actual tool evidence where the client exposes it; a Bot-written narrative alone is not independent verification.

The six ordinary tools are gadgets_list_devices, gadgets_get_state, gadgets_command, gadgets_command_status, gadgets_read_events and gadgets_diagnostics. `rgb.set` is the only command capability; button/state are event/read capabilities. Starting disconnected intentionally makes ordinary commands fail. Start connected for ordinary use, or explicitly opt into `--test-controls` for test-only button/disconnect/reconnect operations, then remove it afterward. No automatic button-triggered Bot waking is promised.

No automatic connector installation or account changes occur from downloading this ZIP. If your client only supports Remote HTTPS MCP, this kit is not a hosted endpoint. A public authenticated service, physical C124, Linux peripherals and Home Assistant are separate future routes.

## Keeping the download current

The website build checks the gateway source commit, kit input hashes, archive contents and acceptance record before copying the download. With the sibling gateway checkout present, a changed committed source or kit input triggers a rebuild. Uncommitted gateway work is rejected. A rebuild runs the gateway suite, installs the extracted kit in a fresh environment and exercises its default and custom/offline settings through the official MCP client. A failure stops the site build before a stale download is published as current.

```sh
python3 scripts/build-simulator-kit.py --check
.venv/bin/python website/build.py
```

These are maintainer commands from the hub, not commands inside the extracted kit. A standalone hub checkout can use the checked-in kit only when it matches the pinned compatibility commit and unchanged inputs; otherwise it requires the gateway checkout to regenerate it. Refresh takes internet access to install hashed dependencies. The visible build ID identifies the tested gateway source; the separate manifest identifies every artifact hash.

This keeps the local build current on rebuild. A public website cannot update itself while unpublished: approved repository CI and deployment must later run these same gates whenever the gateway or kit changes. Downloaded copies remain snapshots; they do not update or run code silently.
