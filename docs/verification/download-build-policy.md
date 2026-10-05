# Current simulator download

The website download is a frozen, inspectable simulator build. Every website build validates its source commit, packaging inputs, successful gateway/default/custom installed-MCP acceptance, archive inventory and SHA-256 checksums. A clean changed gateway commit or changed kit input triggers a rebuild; dirty source, corruption or failed verification blocks promotion. End-of-build checks also reject a source/input change during verification.

The site is assembled in a separate staging directory. Links and kit integrity must pass before promotion; a failed build keeps the previous preview. Download and provenance links contain the gateway commit and archive hash, so an older cached artifact cannot appear to be the newly tested build.

Updates are tied to reviewed component pins. Prepared read-only integration checks test a component candidate with the other known-good pins. Promoting it requires a hub compatibility/documentation change and acceptance. The prepared Pages workflow is manual, main-only, and deploys only after the same run completes all fourteen integration groups and download/path checks. No scheduled refresh or deployment is active. Public CI execution and live HTTPS behavior remain post-approval gates.

Downloaded copies retain their own commit/checksum; upgrading means downloading the newer kit into a fresh folder and carrying over the separate `my-light.json`. The installer preserves protected defaults and never modifies an existing virtual environment. This policy does not promise automatic updates to already downloaded files, a Grok account connection, or physical verification.

Verification at this checkpoint: gateway 2af35fa07910a6111fa3100496128b3db707dfcd, archive SHA256 96d5004d1c3c5da8be08d4d90bc475240b03c3a21a5e917eef5b92c33992117a; six kit regressions passed, including a clean source commit advancing during verification and changed packaging inputs. The website built 59 pages; project-prefix rehearsal resolved 1632 local links and checked the versioned download hash. These are local software results.

The builder stages and validates the complete ZIP/manifest pair before promotion. An ordinary promotion write error restores the previous pair; an injected second-file failure regression verifies the old bytes remain intact. Content-addressed deployed downloads and the staged website retain their separate last-good protection.
