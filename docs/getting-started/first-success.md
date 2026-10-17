# First success without hardware

Install the released gateway and try its simulated light on Mac or Linux. You need Python 3.11 or later and two terminals. You need no board, account or API key. Windows installation is not verified yet.

## 1. Install and start

In a new working directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install grok-gadgets-gateway==0.1.0a16
.venv/bin/grok-gadgets-gateway --version
.venv/bin/grok-gadgets-gateway init
.venv/bin/grok-gadgets-gateway serve --simulator
```

Leave this terminal open. `serve` listens on your own computer at `127.0.0.1:8766/mcp`. The token created by `init` stays on that computer.

## 2. Rehearse a command

In a second terminal, from the same working directory:

```sh
.venv/bin/grok-gadgets-gateway rehearse
```

Look for `Rehearsal passed`. The command lists the simulated device, sets its virtual light and reads its reported state through the gateway's MCP tools. It checks software behavior, not a physical effect or native Grok Bot connection.

If it says `no authenticated gateway answers`, check that `serve` is still running. If it says the token is missing, run `init` again. If it finds no light, start `serve` with `--simulator`.

## Go further

- [Customize the virtual light in your browser](https://grokgadgets.org/playground).
- [Build the owner-tested OLED kit](repeat-the-kit.md).
- [How we verify the kit and local command route](../public/how-we-verify.md).
- [Contribute from a source checkout](../../CONTRIBUTING.md) if you want to change the gateway.
