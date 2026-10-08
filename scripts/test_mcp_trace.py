"""Bounded recorder tests; actual MCP uses an existing local gateway environment."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import threading
import unittest
import zipfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/mcp-trace.py"
spec = importlib.util.spec_from_file_location("mcp_trace", SCRIPT)
trace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trace)


MCP_PROBE = r"""
import asyncio, json, pathlib, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# mcp 2 renamed result fields to snake_case; accept both so the probe runs on either.
def _field(result, name, old_name):
    return getattr(result, name) if hasattr(result, name) else getattr(result, old_name)

async def run():
    script, config, manifest, folder = map(pathlib.Path, sys.argv[1:])
    settings = json.loads(config.read_text())
    for controls in (False, True):
        output = folder / ("controls.jsonl" if controls else "ordinary.jsonl")
        arguments = [str(script), "--output", str(output), "--run-id", "official-mcp-probe",
                     "--config", str(config), "--kit-manifest", str(manifest), "--",
                     sys.executable, "-m", "grok_gadgets_gateway.cli", "--simulator",
                     "--simulator-config", str(config)]
        if controls:
            arguments.append("--test-controls")
        parameters = StdioServerParameters(command=sys.executable, args=arguments)
        async with stdio_client(parameters) as (read, write):
            async with ClientSession(read, write) as client:
                await client.initialize()
                async def call(name, arguments=None):
                    result = await client.call_tool(name, arguments or {})
                    assert not _field(result, "is_error", "isError"), result.content
                    return _field(result, "structured_content", "structuredContent") or json.loads(
                        result.content[0].text
                    )
                names = {tool.name for tool in (await client.list_tools()).tools}
                assert ("test_simulator_control" in names) is controls
                device = (await call("gadgets_list_devices"))["devices"][0]
                assert device["device_id"] == settings["device_id"]
                assert device["state"]["rgb"] == settings["initial_rgb"]
                assert device["simulated"] and not device["available"]
                request = {"device_id": settings["device_id"], "capability": "rgb.set",
                           "arguments": {"r": 0, "g": 0, "b": 255, "on": True}}
                assert (await call("gadgets_command", {**request, "command_id": "offline"}))["error"]["code"] == "unavailable"
                if not controls:
                    continue
                restored = (await call("test_simulator_control", {"action": "reconnect"}))["device"]
                assert restored["available"] and restored["boot_id"] != device["boot_id"]
                assert restored["state"]["rgb"] == settings["initial_rgb"]
                command = (await call("gadgets_command", {**request, "command_id": "blue"}))["command"]
                assert command["status"] == "executed" and command["simulated"]
                assert not command["physical_verified"] and command.get("duplicate") is False
                assert command["reported_state"]["rgb"] == request["arguments"]
                retry = (await call("gadgets_command", {**request, "command_id": "blue"}))["command"]
                assert retry == {**command, "duplicate": True}
                receipt = {key: value for key, value in command.items() if key != "duplicate"}
                assert (await call("gadgets_command_status", {"command_id": "blue"}))["command"] == receipt
                assert (await call("gadgets_get_state", {"device_id": settings["device_id"]}))["device"]["state"]["rgb"] == request["arguments"]
                for pressed in (True, False):
                    await call("test_simulator_control", {"action": "button", "pressed": pressed})
                events = await call("gadgets_read_events", {"device_id": settings["device_id"]})
                assert [event["data"]["pressed"] for event in events["events"]] == [True, False]
                assert (await call("gadgets_read_events", {"cursor": events["next_cursor"]}))["events"] == []
                await call("test_simulator_control", {"action": "disconnect"})
                assert (await call("gadgets_command", {**request, "command_id": "offline-again"}))["error"]["code"] == "unavailable"
                recovered = (await call("test_simulator_control", {"action": "reconnect"}))["device"]
                assert recovered["boot_id"] != restored["boot_id"]
                assert recovered["state"]["rgb"] == settings["initial_rgb"]
                assert not (await call("gadgets_diagnostics"))["report"]["physical_verified"]
        records = [json.loads(line) for line in output.read_text().splitlines()]
        assert records[0]["kind"] == "run" and records[-1]["kind"] == "end"
        assert records[-1]["exit_code"] == 0
        assert not records[-1]["trace_write_failed"] and not records[-1]["relay_failed"] and records[-1]["omitted_records"] == 0
        assert [record["seq"] for record in records] == list(range(1, len(records) + 1))
        assert [record["monotonic_ns"] for record in records] == sorted(record["monotonic_ns"] for record in records)
        results = [record for record in records if record["kind"] == "result"]
        assert results and all(record["correlation"].get("request_seq") for record in results)
        if controls:
            assert any(record["correlation"].get("tool") == "gadgets_read_events" for record in results)
    ordinary = [json.loads(line) for line in (folder / "ordinary.jsonl").read_text().splitlines()]
    assert ordinary[-1]["kind"] == "end" and ordinary[-1]["exit_code"] == 0
    assert not ordinary[-1]["trace_write_failed"] and not ordinary[-1]["relay_failed"] and ordinary[-1]["omitted_records"] == 0
    print(json.dumps({"official_mcp": "passed", "simulated": True, "physical_verified": False,
                      "scope": "local recorded MCP; no Grok caller attestation"}))

asyncio.run(run())
"""


class TraceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="mcp-trace-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.config = self.root / "my-light.json"
        self.config.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "device_id": "trace-light",
                    "display_name": "Trace light",
                    "initial_rgb": {"r": 26, "g": 51, "b": 128, "on": True},
                    "response_delay_ms": 0,
                    "start_disconnected": True,
                }
            )
        )
        self.manifest = self.root / "manifest.json"
        files = []
        for name, value in [
            ("source.tar", b"fixture source"),
            ("grok_gadgets_gateway-0.1.0a1-py3-none-any.whl", b"fixture wheel"),
        ]:
            (self.root / name).write_bytes(value)
            files.append({"file": name, **trace.fingerprint(value)})
        self.manifest.write_text(
            json.dumps(
                {
                    "format_version": 1,
                    "gateway_commit": "a" * 40,
                    "package_version": "0.1.0a1",
                    "files": files,
                }
            )
        )
        self.child = self.root / "grok-gadgets-gateway"
        self.output = self.root / "trace.jsonl"

    def console(self, source):
        self.child.write_text("#!" + sys.executable + "\n" + source)
        self.child.chmod(0o700)

    def command(self, extra=()):
        return [
            sys.executable,
            str(SCRIPT),
            "--output",
            str(self.output),
            "--run-id",
            "trace-test",
            "--config",
            str(self.config),
            "--kit-manifest",
            str(self.manifest),
            "--",
            str(self.child),
            "--simulator",
            "--simulator-config",
            str(self.config),
            *extra,
        ]

    def records(self):
        return [json.loads(line) for line in self.output.read_text().splitlines()]

    def test_transparent_binary_passthrough_and_bounded_packet_evidence(self):
        self.console(
            "import os,sys\nos.write(2,b'private-stderr-fixture')\nwhile True:\n data=os.read(0,16384)\n if not data:break\n os.write(1,data)\n"
        )
        request = b'{"jsonrpc":"2.0","id":1,"method":"ping"}\r\n'
        oversized = b"x" * (trace.MAX_PACKET_BYTES * 2) + b"\n"
        payload = request + b"\x00\xffmalformed\n" + oversized + b"partial"
        # Drain output independently: a blocking parent pipe write can itself deadlock
        # a duplex echo fixture before subprocess.communicate reaches its read event.
        process = subprocess.Popen(
            self.command(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)

        def send():
            try:
                process.stdin.write(payload)
                process.stdin.flush()
            finally:
                process.stdin.close()

        sender = threading.Thread(target=send, daemon=True)
        watchdog = threading.Timer(
            10, lambda: process.terminate() if process.poll() is None else None
        )
        sender.start()
        watchdog.start()
        try:
            output = process.stdout.read()
            errors = process.stderr.read()
            process.wait(timeout=5)
            sender.join(5)
        finally:
            watchdog.cancel()
            process.stdout.close()
            process.stderr.close()
        self.assertFalse(sender.is_alive())
        self.assertEqual(process.returncode, 0, errors)
        self.assertEqual(output, payload)
        self.assertNotIn(b"private-stderr-fixture", errors + self.output.read_bytes())
        records = self.records()
        for direction in ("client_to_child", "child_to_client"):
            oversized_record = next(
                record
                for record in records
                if record["kind"] == "oversized_packet"
                and record["direction"] == direction
            )
            self.assertEqual(
                oversized_record["sha256"], hashlib.sha256(oversized).hexdigest()
            )
            self.assertEqual(oversized_record["bytes"], len(oversized))
            self.assertTrue(
                any(
                    record["kind"] == "incomplete_packet"
                    and record["direction"] == direction
                    for record in records
                )
            )
        self.assertEqual(records[-1]["exit_code"], 0)
        if os.name != "nt":
            self.assertEqual(self.output.stat().st_mode & 0o777, 0o600)

    def test_fresh_log_rejection_and_device_options_never_launch(self):
        self.console("raise SystemExit('child must not start')\n")
        self.output.write_bytes(b"preserved")
        result = subprocess.run(
            self.command(), input=b"", capture_output=True, timeout=5
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.output.read_bytes(), b"preserved")
        self.output.unlink()
        for options in [
            ("--credentials", "private.json"),
            ("--device-port", "8765"),
            ("--simulator",),
            ("--host", "example.invalid"),
        ]:
            with self.subTest(options=options):
                result = subprocess.run(
                    self.command(options), input=b"", capture_output=True, timeout=5
                )
                self.assertEqual(result.returncode, 2)
                self.assertFalse(self.output.exists())
                self.assertNotIn(b"child must not start", result.stderr)

    def test_config_and_manifest_bounds_and_hashes(self):
        self.assertEqual(
            trace.configuration(self.config)["sha256"],
            hashlib.sha256(self.config.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            trace.kit_provenance(self.manifest)["gateway_commit"], "a" * 40
        )
        invalid = [
            '{"schema_version":1,"token":"private"}',
            '{"schema_version":true}',
            '{"schema_version":1,"response_delay_ms":true}',
            '{"schema_version":1,"schema_version":1}',
            '{"schema_version":1,"response_delay_ms":NaN}',
            '{"schema_version":1,"initial_rgb":{"r":true,"g":0,"b":0,"on":false}}',
        ]
        for value in invalid:
            self.config.write_text(value)
            with self.subTest(value=value), self.assertRaises(ValueError):
                trace.configuration(self.config)
        self.config.write_bytes(b" " * 4097)
        with self.assertRaises(ValueError):
            trace.configuration(self.config)
        (self.root / "source.tar").write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            trace.kit_provenance(self.manifest)

    def test_credential_environment_stripped_and_config_snapshot_is_exact(self):
        original = self.config.read_bytes()
        self.console(
            "import os,sys,pathlib,json\nos.write(1,b'ready\\n')\nsys.stdin.buffer.read(1)\nassert 'GROK_DEVICE_TOKEN' not in os.environ\nassert 'PYTHONPATH' not in os.environ\np=pathlib.Path(sys.argv[sys.argv.index('--simulator-config')+1])\nassert p.stat().st_mode & 0o777 == 0o600\nos.write(1,p.read_bytes())\n"
        )
        environment = {
            **os.environ,
            "GROK_DEVICE_TOKEN": "private-environment-fixture",
            "PYTHONPATH": "private-path-fixture",
        }
        process = subprocess.Popen(
            self.command(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=environment,
        )
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        self.assertEqual(process.stdout.readline(), b"ready\n")
        self.config.write_text('{"token":"changed-private-fixture"}')
        output, errors = process.communicate(b"x", timeout=8)
        self.assertEqual(process.returncode, 0, errors)
        self.assertEqual(output, original)
        self.assertEqual(
            self.records()[0]["config"]["sha256"], hashlib.sha256(original).hexdigest()
        )
        self.assertNotIn("private-environment-fixture", self.output.read_text())

    def test_eof_stops_uncooperative_child_and_write_failure_is_explicit(self):
        self.console("import sys,time\nsys.stdin.buffer.read()\ntime.sleep(60)\n")
        result = subprocess.run(
            self.command(), input=b"", capture_output=True, timeout=8
        )
        self.assertEqual(result.returncode, 128 + signal.SIGKILL)
        self.assertTrue(self.records()[-1]["stdin_closed"])
        self.output.unlink()
        recorder = trace.Trace(self.output, {"run_id": "write-failure"})
        with patch.object(
            trace, "write_all", side_effect=OSError("fixture private failure")
        ):
            recorder.emit("request", {})
        self.assertTrue(recorder.failed)
        recorder.close({"exit_code": 0})
        self.assertNotIn("private failure", self.output.read_text())

    def test_correlations_redaction_chunk_boundaries_and_log_ceiling(self):
        recorder = trace.Trace(self.output, {"run_id": "unit"})
        incoming = trace.Packets(recorder, "client_to_child")
        outgoing = trace.Packets(recorder, "child_to_client")
        request = {
            "jsonrpc": "2.0",
            "id": "private-id",
            "method": "tools/call",
            "params": {
                "name": "gadgets_get_state",
                "arguments": {
                    "device_id": "trace-light",
                    "access_token": "private-token-fixture",
                },
                "_meta": {"secret": "private-meta-fixture"},
            },
        }
        data = (json.dumps(request) + "\n").encode()
        incoming.feed(data[:9])
        incoming.feed(data[9:])
        response = {
            "jsonrpc": "2.0",
            "id": "private-id",
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(
                            {
                                "password": "private-password-fixture",
                                "state": {
                                    "rgb": {"r": 26, "g": 51, "b": 128, "on": True}
                                },
                            }
                        ),
                    }
                ]
            },
        }
        outgoing.feed((json.dumps(response) + "\n").encode())
        with (
            patch.object(trace, "MAX_RECORDS", 5),
            patch.object(trace, "MAX_LOG_BYTES", 8192),
        ):
            for _ in range(20):
                incoming.feed(b'{"jsonrpc":"2.0","method":"ping"}\n')
            recorder.close({"exit_code": 0})
        raw = self.output.read_text()
        for secret in [
            "private-token-fixture",
            "private-meta-fixture",
            "private-password-fixture",
            "private-id",
        ]:
            self.assertNotIn(secret, raw)
        records = self.records()
        result = next(record for record in records if record["kind"] == "result")
        self.assertEqual(result["correlation"]["request_seq"], 2)
        self.assertEqual(result["correlation"]["tool"], "gadgets_get_state")
        self.assertEqual(
            result["rpc"]["result"]["content"][0]["text"]["state"]["rgb"]["r"], 26
        )
        self.assertLessEqual(len(records), 5)
        self.assertLessEqual(self.output.stat().st_size, 8192)
        self.assertGreater(records[-1]["omitted_records"], 0)

    @unittest.skipIf(
        os.name == "nt", "POSIX signal/console fixture; Windows unverified"
    )
    def test_signal_cleanup_and_early_child_exit_with_parent_stdin_open(self):
        self.console(
            "import os,time\nos.write(1,(str(os.getpid())+'\\n').encode())\ntime.sleep(60)\n"
        )
        process = subprocess.Popen(
            self.command(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        child_pid = int(process.stdout.readline())
        process.send_signal(signal.SIGTERM)
        _, errors = process.communicate(timeout=8)
        self.assertEqual(process.returncode, 128 + signal.SIGTERM, errors)
        with self.assertRaises(ProcessLookupError):
            os.kill(child_pid, 0)
        self.assertEqual(self.records()[-1]["signal"], signal.SIGTERM)
        self.output.unlink()
        self.console("import os\nos.write(1,b'early exit\\n')\n")
        process = subprocess.Popen(
            self.command(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.wait(timeout=8)
        output, errors = process.communicate(timeout=3)
        self.assertEqual(process.returncode, 0, errors)
        self.assertEqual(output, b"early exit\n")
        self.assertEqual(self.records()[-1]["kind"], "end")

    def test_actual_official_mcp_gateway_simulation(self):
        gateway = ROOT.parent / "grok-gadgets-gateway"
        python = gateway / ".venv/bin/python"
        archive = ROOT / "website/downloads/grok-gadgets-simulator-kit.zip"
        if not python.exists() or not archive.exists():
            self.skipTest(
                "Actual MCP needs the prepared local gateway environment and kit"
            )
        kit = self.root / "kit"
        with zipfile.ZipFile(archive) as bundle:
            # Extract only the already named kit files needed for provenance, without path traversal.
            for name in ("manifest.json", "source.tar"):
                kit.mkdir(exist_ok=True)
                (kit / name).write_bytes(
                    bundle.read("grok-gadgets-simulator-kit/" + name)
                )
            manifest = json.loads((kit / "manifest.json").read_text())
            wheel = next(
                item["file"]
                for item in manifest["files"]
                if item["file"].endswith(".whl")
            )
            (kit / wheel).write_bytes(
                bundle.read("grok-gadgets-simulator-kit/" + wheel)
            )
        result = subprocess.run(
            [
                str(python),
                "-c",
                MCP_PROBE,
                str(SCRIPT),
                str(self.config),
                str(kit / "manifest.json"),
                str(self.root),
            ],
            capture_output=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        self.assertEqual(json.loads(result.stdout)["official_mcp"], "passed")
        self.assertEqual(
            self.records_from("controls.jsonl")[0]["kit"]["gateway_commit"],
            manifest["gateway_commit"],
        )

    def records_from(self, name):
        return [
            json.loads(line) for line in (self.root / name).read_text().splitlines()
        ]


if __name__ == "__main__":
    unittest.main()
