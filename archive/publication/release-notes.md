# v0.1.0-alpha.1 release notes

Updated 6 October 2026. All five repository tags and GitHub pre-releases are published.
The hub release deployment succeeded and the live footer shows site `e0e07df4` and gateway
kit `ca4c5279`. No package registry uploads have been made. Each section is based on that
repository's `CHANGELOG.md`; the owner-approved plan is in *Release plan* below.

Every component is an experimental alpha. Evidence is software only: tests, builds and local
MCP calls. No Grok Bot session, flashed board, real Linux peripheral, systemd service or real
Home Assistant home has been verified. See the
[project status](../docs/public/support-matrix.md).

## grok-gadgets (hub) v0.1.0-alpha.1

- Website at <https://grok-gadgets.pages.dev/>, always deployed from `main`, with the site and
  kit builds in the footer. Component guides on the site are imported from each component's
  `main` at deploy time.
- New homepage: "Let your Grok Bot control lights, buttons and sensors you build." One status
  chip and one status page; three paths (No hardware, Linux, ESP32).
- The simulator kit is built from gateway `main`, pinned by a hash of the files it is built from.
- Nightly integrated acceptance, hub `dev` pushes and PRs targeting `dev` test component
  `dev` heads. Hub `main` pushes and PRs targeting `main` test component `main` heads.
  Manual runs can select `main`, `dev` or the recorded release pins.
- Maintainer and process records moved out of the public documentation index.

## grok-gadgets-gateway v0.1.0-alpha.1 (package 0.1.0a1)

- Six MCP tools for Grok Bot, over stdio or authenticated HTTP on `127.0.0.1`.
- `gadgets_command` waits up to 3 seconds for the device and returns the final status.
- Capability descriptions reach the model (`capability_descriptions`).
- Real subcommands, pasteable `init` settings with absolute paths, `enroll --rotate` and
  `--token-file`, clean shutdown on SIGTERM, no OAuth metadata in static-bearer mode.
- Five-minute first success that rehearses the Grok Bot tool calls, checked by CI every night.
- Protocol 0.1.0 README in sections, including `late_ack`. Wire format unchanged.

## grok-gadgets-linux-sdk v0.1.0-alpha.1 (package 0.1.0a1)

- `@gadget.command("What it does")` decorator API with schemas from type hints.
  `Device.capability` keeps working.
- `grok-linux-agent dev ./my_gadget.py`: an in-process gateway with loopback trust, no tokens
  to copy (`[gateway]` extra).
- `--token-file` is re-read on every connection, so a rotated token needs no restart.
- A slow handler gets a failed ACK and keeps the session; `late_ack` is non-fatal.
- CI runs the gateway integration tests against gateway `main` and the README quick start.

## grok-gadgets-esp32-sdk v0.2.0-alpha.1 (library 0.2.0)

- `grok::Gadget` for Arduino sketches; C124 and generic ESP32-S3 LED/button examples compile.
- `late_ack` and `unknown_command` no longer reset the USB session.
- PlatformIO and Arduino library manifests are prepared and checked in CI.
- CI runs the README quick start and the simulated USB link to gateway `main`.

## grok-gadgets-home-assistant v0.1.0-alpha.1 (package 0.1.0a1)

- `ha-probe`: read-only discovery of Home Assistant's own MCP server. It never calls a tool.
- CI checks the README quick start output field by field.

## Release plan (decided 6 October 2026)

| Repository | Tag | Package version | Release assets |
| --- | --- | --- | --- |
| grok-gadgets-gateway | `v0.1.0-alpha.1` | `0.1.0a1` | wheel, sdist, `SHA256SUMS` |
| grok-gadgets-linux-sdk | `v0.1.0-alpha.1` | `0.1.0a1` | wheel, sdist, `SHA256SUMS` |
| grok-gadgets-esp32-sdk | `v0.2.0-alpha.1` | library 0.2.0 | source only (no firmware binaries until redistribution material is complete) |
| grok-gadgets-home-assistant | `v0.1.0-alpha.1` | `0.1.0a1` | wheel, sdist, `SHA256SUMS` |
| grok-gadgets (hub) | `v0.1.0-alpha.1` | — | simulator kit ZIP and its manifest |

- **When:** once every open PR for the 6 October review has merged, all five `main` CI runs
  are green and the latest deploy succeeded.
- **Order:** gateway first (it owns the protocol). Then the Linux SDK, after a PR that pins
  its `[gateway]` extra to the gateway tag instead of `main`. Then ESP32 and Home Assistant.
  The hub goes last, after a PR that records the four tagged commits in
  `compatibility/tested-components.json` and in this file.
- **How:** annotated tags on the reviewed `main` merge commits; GitHub releases marked
  *pre-release*, titled `<repository> <tag>`, with the matching section above as the notes.
  Build artifacts from a clean checkout of the tag.
- **Not in this step:** PyPI, PlatformIO and Arduino Library Manager uploads. They need their
  own approval. Until the gateway is on PyPI, the Linux SDK's `[gateway]` extra installs the
  gateway from GitHub.
- **Later alphas:** `v0.1.0-alpha.2`, and so on, each with its own changelog section.

## Published release records — 6 October 2026

| Repository | Tag | Tagged commit |
| --- | --- | --- |
| grok-gadgets-gateway | [v0.1.0-alpha.1](https://github.com/adidshaft/grok-gadgets-gateway/releases/tag/v0.1.0-alpha.1) | `ca4c52798086f251028aa49af96c90aa0220be78` |
| grok-gadgets-linux-sdk | [v0.1.0-alpha.1](https://github.com/adidshaft/grok-gadgets-linux-sdk/releases/tag/v0.1.0-alpha.1) | `dc97532e74463d3d094be26dddd2bf05947ec0c6` |
| grok-gadgets-esp32-sdk | [v0.2.0-alpha.1](https://github.com/adidshaft/grok-gadgets-esp32-sdk/releases/tag/v0.2.0-alpha.1) | `73f32813b82c8c12caec285e087938a621c9ab82` |
| grok-gadgets-home-assistant | [v0.1.0-alpha.1](https://github.com/adidshaft/grok-gadgets-home-assistant/releases/tag/v0.1.0-alpha.1) | `1eac91c9bf40efd9cec3cdea99c9ffdc810cec4a` |
| grok-gadgets (hub) | [v0.1.0-alpha.1](https://github.com/adidshaft/grok-gadgets/releases/tag/v0.1.0-alpha.1) | `e0e07df41d041eb9139d309dd7e855fbac737a9a` |

The hub tagged merge commit is also recorded in its GitHub release notes. Its existing
compatibility evidence entry remains an earlier snapshot. These records do not add Grok
Bot, hardware, systemd or real-home verification; evidence remains software, builds and local MCP only.
