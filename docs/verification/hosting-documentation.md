# Hosting documentation verification

**Date:** 5 October 2026

The canonical [hosting and remote access FAQ](../getting-started/hosting.md) explains gateway and tunnel ownership, current local operation, customer and maker hosting options, future security requirements, and four distinct evidence gates. It includes three future-route diagrams and links to official Grok Bot and Cloudflare documentation. The docs keep the remote HTTPS service blocked and make no hosting product commitment.

## Imported component documentation

The FAQ and hosting guidance were propagated through the hub docs from these local component snapshots:

| Repository | Documentation commit |
| --- | --- |
| Gateway | `bd37127c640f89bb2e36fc98eb66f19feb0c1493` |
| Linux SDK | `521e5501fa070d56ca5cb4e79cef6f34baa12053` |
| ESP32 SDK | `73a63f65c278d9aadfb285a40c885ddeef2bb56b` |
| Home Assistant | `2d9930dc967bf0cc75f4d72f0c91f2e4c300676f` |

The Gateway change is documentation-only; its runtime source, protocol, project dependencies and lockfile are unchanged from `35bd7aae`. The SDK and Home Assistant changes are also documentation-only. No device port is exposed, and no tunnel or service was activated.

## Checks

- `python3 scripts/check.py`: 37 labeled issue records and Python syntax pass.
- Ruff check and format check for `scripts`, `website`, and `community`: pass (40 files formatted).
- `python3 -m unittest discover -s website -p 'test_*.py'`: 24 tests pass.
- `python3 website/build.py`: 62 pages built; links and fragments checked.
- `python3 scripts/check-social-preview.py website/dist`: crawler metadata and 1200×630 share image verified on 62 pages.
- `python3 scripts/check-pages-prefix.py`: 62 pages and 4,416 project-prefix links pass.
- `python3 scripts/build-simulator-kit.py --check`: current kit and archive hashes pass; archive SHA-256 `72eb4f9968c4695c07a0d1b91902abe2e8833f071f740670998aa59ae4e4bccb`.
- `git diff --check`: pass.

The browser preview showed the FAQ in the Start here navigation, its page contents and the future route diagrams. These are local documentation and software checks only. Grok invocation, remote HTTPS security and physical-device operation remain separate gates. The documentation branch was not pushed or deployed.
