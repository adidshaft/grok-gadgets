# Test-only MCP trace helper

`scripts/mcp-trace.py` is a POSIX stdio observer for a reviewed installed gateway simulator. It is not a gateway feature, authentication mechanism or native-Grok attestation. Never use it to wrap real-device transports. The helper verifies the extracted inner kit manifest's gateway wheel/source bytes; that does not establish that an installed executable is unmodified. First verify the reviewed ZIP checksum and installer inventory.

In a supported, scoped test environment, place this reviewed script next to a fresh extracted kit and use explicit paths:

```sh
python3 mcp-trace.py --output fresh-run.jsonl --run-id simulator-check-1 \
  --config my-light.json --kit-manifest grok-gadgets-simulator-kit/manifest.json -- \
  /absolute/path/grok-gadgets-simulator-kit/.venv/bin/grok-gadgets-gateway \
  --simulator --simulator-config my-light.json --test-controls
```

The operator's MCP client owns stdin/stdout. The wrapper relays bytes unchanged, discards child stderr, strips credential environment values, takes a private snapshot of the exact configuration bytes and writes a new mode0600 file. It records bounded JSON-RPC requests/results and correlations; credentials, client metadata and free text are redacted or hashed. Malformed/oversized packets retain only size/hash evidence. Explicit simulation controls exist only for this test invocation; return to the ordinary six-tool command afterward.

An interpretable complete trace requires an `end` record with exit0, `relay_failed: false`, `trace_write_failed: false`, and `omitted_records: 0`, plus matching configuration/kit hashes and required request/result pairs. Inspect before sharing; all raw account/run logs remain private by default. Native Grok evidence also needs independent client receipts or a directly inspected registration/execution route proving who invoked the trace. A local MCP test run cannot satisfy that requirement.

Eight local regressions include actual official-MCP simulator discovery/state/LED/error/retry/event/disconnect/recovery, byte transparency, redaction, limits, frozen config, EOF/signals and failed-log reporting. Run `.venv/bin/python scripts/test_mcp_trace.py`; a standalone hub without the gateway environment explicitly skips only the actual-MCP test. Windows behavior remains unverified. The dedicated Grok launch run did not upload/register this helper because a supported scoped connector reload was unavailable.
