# Grok Gadgets simulator kit

Run a virtual light and button on your computer. This kit checks Grok Gadgets locally. It does not connect to Grok Bot or operate hardware.

## Run it

Use Python 3.11 or later. Extract this ZIP and open a terminal in the extracted
folder. Inspect the source and compare the ZIP hash with the separate download
manifest before you run code.

```sh
python3 install.py
python3 install.py --install
.venv/bin/python try_simulator.py
```

The first command checks the included files. It does not install anything.
The second command downloads dependencies with hash checks into a new `.venv`.
Initialize the gateway, then start the simulated light:

```sh
.venv/bin/grok-gadgets-gateway init
.venv/bin/grok-gadgets-gateway serve --simulator --simulator-config ./simulator-config.json
```

In a second terminal, rehearse the calls that Grok Bot will make:

```sh
.venv/bin/grok-gadgets-gateway rehearse
```

The rehearsal checks discovery, light control, button events and recovery. It prints
simulated results. It does not connect to Grok Bot or operate hardware.

On Windows, use `.venv\Scripts\python.exe` for the last command. Windows and Intel
Mac installation remain unverified. On Apple Silicon, use native Python.

## Use your own settings

Export `my-light.json` from the [browser playground](https://grok-gadgets.pages.dev/#playground)
and place it in this folder. Keep the original kit files unchanged.

```sh
.venv/bin/python try_simulator.py --config ./my-light.json
```

No hardware, API key or cloud account is required. The demo enables simulation
test controls. Normal connector settings exclude those controls.

## Contents and limits

`manifest.json` identifies the gateway source commit, file hashes and software
checks. `source.tar` contains the committed gateway source. The wheel, source
distribution, hashed dependencies, installer and simulator configuration are
included. Original code is Apache-2.0; read the included license notices.

A Grok Bot cloud computer cannot reach a file or loopback server on your Mac. Grok Bot
compatibility, remote access and physical operation need separate verification.
No account connection or network exposure happens automatically.

For setup options and troubleshooting, use the
[simulator guide](https://grok-gadgets.pages.dev/doc-docs-getting-started-simulator-kit.html).
Downloaded kits are fixed snapshots. They do not update themselves.
