# Ready to contribute

These are scoped software/documentation improvements, ready without hardware, an account, or sibling repositories. Use the GitHub issue links and stable IDs below in your branch and commits. Check [CONTRIBUTING](../../CONTRIBUTING.md) first.

| ID | Starting file and current behavior | Requested result | Acceptance and focused check |
| --- | --- | --- | --- |
| DOC-GLOSSARY-001 | `docs/architecture/overview.md` uses gateway, SDK, MCP, state and event without a linked newcomer glossary | Add `docs/getting-started/glossary.md`, six short definitions plus a light command example; link from architecture and the docs index | Explain reported state versus physical observation, avoid claiming a browser Grok connection; `python3 scripts/check.py`, website environment and `python website/build.py` |
| DOC-TROUBLE-001 | `docs/getting-started/simulator-kit.md` explains setup but has no compact symptom-to-fix lookup | Add a troubleshooting table for missing Python, wrong folder, overwritten protected default, invalid config and disconnected simulator | Reproduce each error using an extracted kit or the existing regression evidence; give exact safe fixes and preserve checksum validation; `python3 scripts/check.py`, `python scripts/test_simulator_kit.py` |
| WEB-COPY-001 | `website/documents.py` renders setup snippets as selectable text without a copy button | Add keyboard/touch copy controls to command snippets with a readable success/failure announcement | Copy exact text, preserve no-JavaScript selection, no copying secrets from outside the snippet, 44px touch target and focused success/failure test; `node --test website/test_simulator.cjs`, `python -m unittest discover -s website`, `python website/build.py` |

The glossary and troubleshooting tasks are documentation improvements, not claimed runtime defects. The copy control is an enhancement. Each PR should include the changed page, exact check results, and any unresolved platform limitation. Windows/Intel Mac, physical C124, real systemd and real Home Assistant verification are separate opportunities with additional prerequisites.

## Open the ready tasks

- [DOC-GLOSSARY-001](https://github.com/adidshaft/grok-gadgets/issues/1)
- [DOC-TROUBLE-001](https://github.com/adidshaft/grok-gadgets/issues/2)
- [WEB-COPY-001](https://github.com/adidshaft/grok-gadgets/issues/36)

## Future feature proposals

These cross-repository proposals came from a source review on 5 October 2026. They are
scoped backlog items, not completed work or verification claims. Check each issue for
design constraints and current status before starting.

| ID | Repository | Proposal |
| --- | --- | --- |
| FUT-GW-TOKEN-001 | [Gateway #12](https://github.com/adidshaft/grok-gadgets-gateway/issues/12) | Rotate a device credential while preserving identity, receipts, and secret handling |
| FUT-GW-USB-001 | [Gateway #13](https://github.com/adidshaft/grok-gadgets-gateway/issues/13) | Reopen a USB device by an explicit stable identity after its OS path changes |
| FUT-GW-RETIRE-001 | [Gateway #14](https://github.com/adidshaft/grok-gadgets-gateway/issues/14) | Retire offline device records while preserving retry evidence through retention |
| FUT-LIN-CANCEL-001 | [Linux SDK #12](https://github.com/adidshaft/grok-gadgets-linux-sdk/issues/12) | Add compatible cooperative cancellation and bounded cleanup outcomes for handlers |
| FUT-LIN-SENSOR-001 | [Linux SDK #13](https://github.com/adidshaft/grok-gadgets-linux-sdk/issues/13) | Provide a simulated background sensor example with bounded event and shutdown behavior |
| FUT-ESP-PREFLIGHT-001 | [ESP32 SDK #13](https://github.com/adidshaft/grok-gadgets-esp32-sdk/issues/13) | Explain registration failures and account for credentials in the hello frame budget |
| FUT-HA-COMPAT-001 | [Home Assistant #9](https://github.com/adidshaft/grok-gadgets-home-assistant/issues/9) | Capture sanitized discovery fixtures from pinned upstream releases |
| FUT-KIT-WIN-001 | [Hub #52](https://github.com/adidshaft/grok-gadgets/issues/52) | Verify the exact simulator ZIP in a clean native Windows environment |
