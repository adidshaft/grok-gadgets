# Current simulator download

The website download is a frozen, inspectable simulator build. Every website build validates its source commit, packaging inputs, successful gateway/default/custom installed-MCP acceptance, archive inventory and SHA-256 checksums. A clean changed gateway commit or changed kit input triggers a rebuild; dirty source, corruption or failed verification blocks promotion. End-of-build checks also reject a source/input change during verification.

The site is assembled in a separate staging directory. Links and kit integrity must pass before promotion; a failed build keeps the previous preview. Download and provenance links contain the gateway commit and archive hash, so an older cached artifact cannot appear to be the newly tested build.

Updates are tied to reviewed component pins. Prepared read-only integration checks test a component candidate with the other known-good pins. Promoting it requires a hub compatibility/documentation change and acceptance. The prepared Pages workflow is manual, main-only, and deploys only after the same run completes all fourteen integration groups and download/path checks. No scheduled refresh or deployment is active. Public CI execution and live HTTPS behavior remain post-approval gates.

Downloaded copies retain their own commit/checksum; upgrading means downloading the newer kit into a fresh folder and carrying over the separate `my-light.json`. The installer preserves protected defaults and never modifies an existing virtual environment. This policy does not promise automatic updates to already downloaded files, a Grok account connection, or physical verification.

Verification at this checkpoint: gateway 71cfecbaf1120b27e1956384861efda5f5a3eef6, archive SHA256 82fa91f366cf803e04b166f3db30adfb9fbcff7927fe9936d14b2355a6173859; five kit regressions passed, including a clean source commit advancing during verification and changed packaging inputs. The website built 57 pages; project-prefix rehearsal resolved 1576 local links and checked the versioned download hash. These are local software results.
