# Simulator export-to-kit correction

HARD-SIM-EXPORT-001 / S1. Reproduction/tracking: 6bde2ba; implementation and regression: f6ebf33. Local functional acceptance and bounded independent review passed. Corrected25-artifact candidate20261004T194005-1791142805602319000 was certified against 7814184. Final evidence-only HEAD certification is required before goal closure; exact source HEADs/hashes live in artifacts/publication/latest.json and the referenced manifest.

## Failure and correction

The original browser downloaded customized settings as simulator-config.json. Copying them into the extracted kit replaced a protected default. The actual installer exited1: `Hash mismatch: simulator-config.json`. Raw before evidence: artifacts/verification/export-onboarding/collision.log. Earlier simulator-playground evidence proved custom JSON content under a separate manually chosen filename, not the unrenamed download flow.

The browser now exports my-light.json. Blob/download, displayed JSON, successful clipboard copy and denied-clipboard guidance use that distinct filename. The setup page and bundled README explain placing it alongside the unchanged default and passing --config ./my-light.json. No manifest/default verification was weakened.

## Corrected flow

1. Open [the local playground](http://127.0.0.1:4173/index.html#playground), expand Customize, set values, and export my-light.json. Copy JSON has the same content; save it under that name if downloading is unavailable.
2. Download and extract the current simulator kit. Place my-light.json in its grok-gadgets-simulator-kit folder. Preserve simulator-config.json and every other bundled file unchanged.
3. Use native Python3.11+ with matching dependency binary wheels. From that extracted folder:

```sh
python3 install.py
python3 install.py --install --config ./my-light.json
.venv/bin/python try_simulator.py --config ./my-light.json
```

The first command checks bundled integrity without installation. The second creates a new venv and downloads hashed binary dependencies. It refuses existing environments; use a fresh extraction for a fresh installation. The final command uses the actual installed wheel and official local MCP client, with opt-in test controls only for the demonstration. Offline startup is intentionally unavailable until the demo reconnects. Ordinary MCP launch settings printed by the installer omit test controls. On Windows the venv interpreter path is .venv\Scripts\python.exe; that installation remains unverified.

## Actual browser-to-kit evidence

Actual in-app browser file: my-light.json,236bytes, SHA256 `6b0c7b08fbbd252f9a91f03c9d513c947331cd14ae4e439b5159a804dc71406d`. Displayed and copied JSON match its bytes. Settings: onboarding-light / Onboarding light; RGB26/51/128,ontrue (50% of #3366ff); response delay125ms; startdisconnectedtrue. Actual website kit download matches separate manifest: SHA256 `94a868ccf69bc792c8865c520efae8b40e3f342236593d6af26bf97f4eb19e1f`, gateway `08f0f127205d23a75ed768cc6372d1329719a03c`.

Freshly extracted downloaded kit plus the separate actual browser file passed verify and --install. Native arm64 Python3.11.15 imported gateway from fresh venv site-packages under -I, not the source checkout. Official stdio MCP responses/assertions show configured discovery and initial state, offline command unavailable, reconnect restores initial state with new boot/session, blue executed/status/state readback, ordered button edges/cursor, off/readback, diagnostics physicalfalse. Review measured configured delay125ms against observed130.612ms; timing is not physical calibration.

Raw local evidence: artifacts/verification/export-onboarding/acceptance.json contains six file hashes/sizes; same folder contains collision.log, my-light.json, downloaded-kit.zip, verify.log, install.log, custom-mcp.jsonl and browser-copy.png. Reviewer independently matched all hashes and protected default bytes against ZIP/manifest. Pre-existing pinned Pydantic lifespan annotation warning is nonfatal; assertions completed. Tests are local simulation and actual local MCP software, not Grok/mobile/physical verification.

## Regression and integrated checks

- Node6/6: existing model regressions plus the browser-used export contract, complete customized setting round-trip and rejection of invalid export settings.
- Kit4/4: actual export function writes its emitted filename into an extracted ZIP, the real verifier accepts immutable defaults, and overwriting the original default still fails. Other tamper/inventory/traversal/symlink/freshness tests remain green. This dry-run test alone does not prove install/config/MCP; the actual fresh installed acceptance above supplies that evidence.
- Website12/12, publication11/11, Ruff lint/format and hubcheck passed. Website builds50 checked pages.
- `.venv/bin/python scripts/check-all.py`:14/14 groups passed on clean tracked source24729e0; raw artifacts/verification/20261004T193719-1791142639802012000/results.json records exact commands/source/diff state and logs. Includes new Node/kit checks and existing community, gateway, official MCP, Linux, installed-custom onboarding, HA fixtures, ESP host/contracts/USB. Gatewaye3cd6f0, Linuxbe66ea4, ESPe78fb1c, HAb06eb07 unchanged. No firmware source changed; compiled C124 provenance remains separate from host/USB regression checks.
- Kit was rebuilt from exact committed gateway source. Builder runs73 gateway tests and fresh installed default/custom offline MCP before replacing download. Website/kit freshness/provenance and final25-artifact publication certification are required after final source commits.

## Independent review and limits

Bounded read-only GPT-6.1 Sol High reviewer found no material functional defect in2f20398. It reran Node/kit/freshness checks; evaluated actual scene export/copy/fallback handlers with a lightweight VM; independently matched extracted defaults/customfile/evidence hashes and parsed MCP lifecycle. Dry-run regression scope was documented accurately; a stale inprogress verification note was replaced with this record. Review is another agent, not independent human installation.

No live Grok accounts operated, and no public push/publish/deployment/spending/automation/Reddit or physical-device action occurred. Actual Grok invocation receipts and mobile, hardware C124, real homes/peripherals/systemd, another human and public CI/deployment remain external gates. Downloaded copies remain snapshots; website builds run freshness gates and public cross-repository CI/deployment stays inactive.

## Requirement completion audit

1. Reproduction and labeled local issue: protected-default overwrite fails exactly as reported; 6bde2ba and collision.log.
2. Corrected filename/integrity: download/copy/fallback/guide all use my-light.json; unchanged default still hash protected; f6ebf33 and independent review.
3. Meaningful regression: browser-used export contract into actual extractedkit plus old overwrite-negative; Node6/kit4 pass, integrated acceptance/CI include them.
4. Actual browser and fresh install/MCP: actual file hash236bytes, clean installed site-packages, observed configured/offline/reconnect/command/state outcomes above and acceptance.json.
5. Affected/cross-repository checks and artifacts:14clean-source groups, affectedtests/lint/hubcheck pass; kit rebuilt/current/hashchecked,50page website and25artifact correctedcandidate certified. Final evidence-only candidate must additionally pass require-current before goalclosure.
6. Independent review: bounded read-only review of24729e0 and actualinstallation/receipts, no material finding; limitations and stale-note disposition recorded.
7. Tracking/process: issue, S1 rollup, migration export, currentcheckpoint, simulator evidence, review and journal updated. Historical acceptance is qualified, not represented as correct filename onboarding.

All implementation is locally committed; main integration and final currentHEAD certification are performed after this evidence closure. Unrelated assets/ preserved. Final external evidence pointer: artifacts/verification/export-onboarding/final.json.
