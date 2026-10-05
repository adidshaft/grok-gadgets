# Hosting documentation verification

**Date:** 5 October 2026. The hosting FAQ on `simplify-and-fix` was later shortened to a one-page status table. The checks below describe the earlier long form.

The canonical [hosting and remote access FAQ](../getting-started/hosting.md) explains who runs the gateway, what local `serve` is, and that Grok Bot has not used it.

## Imported component documentation

The FAQ and hosting guidance were propagated through the hub docs from these local component snapshots:

| Repository | Documentation commit |
| --- | --- |
| Gateway | `255a956166077f97108c949378f89b36a7724c87` |
| Linux SDK | `4477303dc64ce705f1ff1828e696fe51b54b7f35` |
| ESP32 SDK | `04b35d6110c18ad590e4510e0798a0a2011521dd` |
| Home Assistant | `6ba55362b3bc32e8ae07f3d1e4cf47202fcbc937` |

The Gateway change is documentation-only; its runtime source, protocol, project dependencies and lockfile are unchanged from `7e2acfad`. The SDK and Home Assistant changes are also documentation-only. No device port is exposed, and no tunnel or service was activated.

## Checks

- `python3 scripts/check.py`: 37 labeled issue records and Python syntax pass.
- Ruff check and format check for `scripts`, `website`, and `community`: pass (40 files formatted).
- `python3 -m unittest discover -s website -p 'test_*.py'`: 24 tests pass.
- `python3 website/build.py`: 62 pages built; links and fragments checked.
- `python3 scripts/check-social-preview.py website/dist`: crawler metadata and 1200×630 share image verified on 62 pages.
- `python3 scripts/check-pages-prefix.py`: 62 pages and 4,416 project-prefix links pass.
- `python3 scripts/build-simulator-kit.py --check`: current kit and archive hashes pass; archive SHA-256 `bc6ee4f2c2a5340fd9fc3ec5d1501dccd5646791fdf315cc710c1fbadda9601d`.
- `git diff --check`: pass.

The browser preview showed the FAQ in the Start here navigation, its page contents and the future route diagrams. These are local documentation and software checks only. Grok invocation, remote HTTPS security and physical-device operation remain separate gates. The documentation branch was not pushed or deployed.
