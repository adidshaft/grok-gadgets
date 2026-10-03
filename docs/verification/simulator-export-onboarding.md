# Simulator export-to-kit correction

HARD-SIM-EXPORT-001 / S1 is in progress. Starting hub 3266a05 and gateway fa062a1. Reproduction extracted the current checked-in kit and replaced its protected simulator-config.json with valid customized settings. The readable installer exited 1: `Hash mismatch: simulator-config.json`. Raw evidence: artifacts/verification/export-onboarding/collision.log.

The bundled default must remain integrity checked. Corrected flow will export my-light.json separately, then pass --config ./my-light.json. Browser download/copy/fallback and actual clean installation/MCP acceptance remain to verify. Local simulation only; no Grok, mobile or physical claim.
