"""Test-only simulated MCP stdio recorder; no caller/Grok or physical attestation.

Example: python mcp-trace.py --output fresh.jsonl --run-id simulation-1
  --config my-light.json --kit-manifest extracted-kit/manifest.json --
  extracted-kit/.venv/bin/grok-gadgets-gateway --simulator
  --simulator-config my-light.json --test-controls

The operator supplies trusted installed code. Kit artifact hashes do not attest that
an installed executable is unmodified. Stderr is discarded, never captured verbatim.
"""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time

MAX_PACKET_BYTES = 65536
MAX_LOG_BYTES = 8 * 1024 * 1024
MAX_RECORDS = 10000
MAX_PENDING = 256
MAX_ARTIFACT_BYTES = 64 * 1024 * 1024
CHUNK_BYTES = 16384
EXIT_GRACE_SECONDS = 3
TOOLS = {
    "gadgets_list_devices",
    "gadgets_get_state",
    "gadgets_command",
    "gadgets_command_status",
    "gadgets_read_events",
    "gadgets_diagnostics",
    "test_simulator_control",
}
SECRET = re.compile(
    r"password|token|secret|credential|authorization|api.?key|cookie", re.I
)
IDENTIFIERS = {
    "jsonrpc",
    "method",
    "capability",
    "status",
    "code",
    "protocolVersion",
    "version",
    "action",
    "device_id",
    "command_id",
    "event_id",
    "session_id",
    "boot_id",
    "cursor",
    "next_cursor",
    "type",
    "model",
    "firmware",
    "sdk",
    "transport",
}
METHODS = {
    "initialize",
    "ping",
    "notifications/initialized",
    "notifications/cancelled",
    "notifications/progress",
    "tools/list",
    "tools/call",
}
NUMBERS = {
    "id",
    "r",
    "g",
    "b",
    "sequence",
    "limit",
    "code",
    "minimum",
    "maximum",
    "minLength",
    "maxLength",
    "schema_version",
    "response_delay_ms",
}
BOOLEANS = {
    "ok",
    "on",
    "pressed",
    "available",
    "simulated",
    "physical_verified",
    "grok_verified",
    "isError",
    "history_lost",
    "duplicate",
    "connected",
    "additionalProperties",
}


def fingerprint(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def bounded_read(path, limit):
    with Path(path).open("rb") as handle:
        data = handle.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Input exceeds its size limit")
    return data


def strict_json(data):
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value:
                raise ValueError("Duplicate JSON field")
            value[key] = item
        return value

    def constant(_):
        raise ValueError("Nonfinite JSON number")

    return json.loads(data, object_pairs_hook=pairs, parse_constant=constant)


def configuration(path, raw=None):
    raw = bounded_read(path, 4096) if raw is None else raw
    value = strict_json(raw)
    fields = {
        "schema_version",
        "device_id",
        "display_name",
        "initial_rgb",
        "response_delay_ms",
        "start_disconnected",
    }
    if (
        not isinstance(value, dict)
        or set(value) - fields
        or type(value.get("schema_version")) is not int
        or value["schema_version"] != 1
    ):
        raise ValueError("Expected bounded simulator configuration v1")
    if "device_id" in value and (
        not isinstance(value["device_id"], str)
        or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,63}", value["device_id"])
    ):
        raise ValueError("Invalid simulator identity")
    if "display_name" in value and (
        not isinstance(value["display_name"], str)
        or not 1 <= len(value["display_name"]) <= 80
        or not re.fullmatch(r"[ -~]*[!-~][ -~]*", value["display_name"])
    ):
        raise ValueError("Invalid simulator label")
    if "response_delay_ms" in value and (
        type(value["response_delay_ms"]) is not int
        or not 0 <= value["response_delay_ms"] <= 2000
    ):
        raise ValueError("Invalid simulator delay")
    if "start_disconnected" in value and type(value["start_disconnected"]) is not bool:
        raise ValueError("Invalid simulator availability")
    if "initial_rgb" in value:
        rgb = value["initial_rgb"]
        if (
            not isinstance(rgb, dict)
            or set(rgb) != {"r", "g", "b", "on"}
            or any(type(rgb[c]) is not int or not 0 <= rgb[c] <= 255 for c in "rgb")
            or type(rgb["on"]) is not bool
        ):
            raise ValueError("Invalid simulator RGB")
    return fingerprint(raw)


def kit_provenance(path):
    path = Path(path).resolve(strict=True)
    raw = bounded_read(path, 1024 * 1024)
    value = strict_json(raw)
    if (
        not isinstance(value, dict)
        or type(value.get("format_version")) is not int
        or value["format_version"] != 1
        or not isinstance(value.get("gateway_commit"), str)
        or not re.fullmatch(r"[0-9a-f]{40}", value["gateway_commit"])
        or not isinstance(value.get("package_version"), str)
        or not re.fullmatch(r"[0-9][A-Za-z0-9.+-]{0,40}", value["package_version"])
        or not isinstance(value.get("files"), list)
        or not 2 <= len(value["files"]) <= 20
    ):
        raise ValueError("Invalid extracted kit manifest")
    records = {}
    for item in value["files"]:
        if (
            not isinstance(item, dict)
            or set(item) != {"file", "bytes", "sha256"}
            or not isinstance(item["file"], str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,180}", item["file"])
            or item["file"] in records
            or type(item["bytes"]) is not int
            or not 0 <= item["bytes"] <= MAX_ARTIFACT_BYTES
            or not isinstance(item["sha256"], str)
            or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
        ):
            raise ValueError("Invalid kit artifact record")
        records[item["file"]] = item
    wheels = [name for name in records if name.endswith(".whl")]
    if (
        "source.tar" not in records
        or len(wheels) != 1
        or not wheels[0].startswith(
            "grok_gadgets_gateway-" + value["package_version"] + "-"
        )
    ):
        raise ValueError("Kit must identify one gateway wheel and source archive")
    selected = [records[name] for name in ["source.tar", wheels[0]]]
    for item in selected:
        artifact = path.parent / item["file"]
        if artifact.is_symlink() or not artifact.is_file():
            raise ValueError("Missing or unsafe kit artifact")
        if fingerprint(bounded_read(artifact, MAX_ARTIFACT_BYTES)) != {
            "bytes": item["bytes"],
            "sha256": item["sha256"],
        }:
            raise ValueError("Kit artifact hash mismatch")
    return {
        "manifest": fingerprint(raw),
        "gateway_commit": value["gateway_commit"],
        "package_version": value["package_version"],
        "artifacts": selected,
        "scope": "kit wheel/source bytes verified; installed code is operator supplied",
    }


def simulator_command(command, config):
    if not command:
        raise ValueError("A simulator child command is required")
    executable = Path(command[0]).absolute()
    if not executable.is_file():
        raise ValueError("Child executable must be an explicit existing path")
    arguments = command[1:]
    if executable.name in {"grok-gadgets-gateway", "grok-gadgets-gateway.exe"}:
        pass
    elif re.fullmatch(r"python(?:[0-9]+(?:\.[0-9]+)*)?(?:\.exe)?", executable.name):
        if arguments[:2] != ["-m", "grok_gadgets_gateway.cli"]:
            raise ValueError("Python child must launch the gateway CLI module")
        arguments = arguments[2:]
    else:
        raise ValueError("Only the trusted gateway simulator executable is allowed")
    seen = set()
    index = 0
    while index < len(arguments):
        flag = arguments[index]
        if (
            flag not in {"--simulator", "--simulator-config", "--test-controls"}
            or flag in seen
        ):
            raise ValueError("Only explicit simulator options are allowed")
        seen.add(flag)
        index += 1
        if flag == "--simulator-config":
            if (
                index == len(arguments)
                or Path(arguments[index]).resolve(strict=True) != config
            ):
                raise ValueError(
                    "Child configuration must match the fingerprinted file"
                )
            index += 1
    if not {"--simulator", "--simulator-config"} <= seen:
        raise ValueError("Explicit simulator and configuration flags are required")
    return [str(executable), *command[1:]]


def public_value(value, key="", depth=0):
    """Retain protocol/simulator structure, hash free text, strip credential metadata."""
    if SECRET.search(key) or key in {"_meta", "clientInfo"}:
        return "[redacted]"
    if depth > 16:
        return "[depth limit]"
    if isinstance(value, dict):
        result = {}
        for field, item in list(value.items())[:64]:
            label = (
                field
                if re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_.$:-]{0,63}", field)
                else "field-sha256-" + hashlib.sha256(field.encode()).hexdigest()
            )
            result[label] = public_value(item, field, depth + 1)
        if len(value) > 64:
            result["_omitted_fields"] = len(value) - 64
        return result
    if isinstance(value, list):
        result = [public_value(item, key, depth + 1) for item in value[:64]]
        if len(value) > 64:
            result.append({"omitted_items": len(value) - 64})
        return result
    if isinstance(value, str):
        if key == "text":
            try:
                decoded = strict_json(value)
                if isinstance(decoded, (dict, list)):
                    return public_value(decoded, depth=depth + 1)
            except (ValueError, RecursionError):
                pass
        if (
            (key == "name" and value in TOOLS)
            or (key == "method" and value in METHODS)
            or (
                key in IDENTIFIERS - {"method"}
                and re.fullmatch(r"[A-Za-z0-9._:/ -]{1,128}", value)
            )
        ):
            return value
        return {"redacted": "free text", **fingerprint(value.encode())}
    if isinstance(value, float) and not math.isfinite(value):
        return "[nonfinite]"
    if type(value) is bool and key not in BOOLEANS:
        return "[redacted scalar]"
    if type(value) in {int, float} and key not in NUMBERS:
        return "[redacted scalar]"
    return value


class Trace:
    def __init__(self, output, header):
        descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        self.file = os.fdopen(descriptor, "wb", buffering=0)
        self.lock = threading.RLock()
        self.started = time.monotonic_ns()
        self.sequence = self.size = self.omitted = 0
        self.failed = False
        self.closed = False
        self.pending = {}
        self.counts = {"client_to_child": 0, "child_to_client": 0}
        self.emit("run", header)

    def emit(self, kind, value, final=False):
        with self.lock:
            if self.failed or self.closed:
                return None
            sequence = self.sequence + 1
            record = {
                "seq": sequence,
                "monotonic_ns": time.monotonic_ns() - self.started,
                "kind": kind,
                **value,
            }
            data = (
                json.dumps(record, separators=(",", ":"), ensure_ascii=True) + "\n"
            ).encode()
            if not final and (
                self.size + len(data) > MAX_LOG_BYTES - 2048
                or sequence > MAX_RECORDS - 1
            ):
                self.omitted += 1
                return None
            if self.size + len(data) > MAX_LOG_BYTES:
                self.failed = True
                return None
            try:
                write_all(self.file.fileno(), data)
            except OSError:
                self.failed = True
                return None
            self.sequence = sequence
            self.size += len(data)
            return sequence

    def packet(self, direction, content, size, sha256, complete=True):
        with self.lock:
            self.counts[direction] += 1
            evidence = {
                "direction": direction,
                "bytes": size,
                "sha256": sha256,
                "complete": complete,
            }
            if content is None:
                return self.emit("oversized_packet", evidence)
            if not complete:
                return self.emit("incomplete_packet", evidence)
            try:
                value = strict_json(content)
                if not isinstance(value, dict) or value.get("jsonrpc") != "2.0":
                    raise ValueError("Not JSON-RPC")
                identifier = value.get("id")
                if identifier is not None and type(identifier) not in {str, int}:
                    raise ValueError("Invalid JSON-RPC identifier")
                request = isinstance(value.get("method"), str)
                response = ("result" in value) != ("error" in value)
                if request == response or (response and "id" not in value):
                    raise ValueError("Ambiguous JSON-RPC packet")
                key = hashlib.sha256(json.dumps(identifier).encode()).hexdigest()
                correlation = {}
                if response:
                    opposite = (
                        "client_to_child"
                        if direction == "child_to_client"
                        else "child_to_client"
                    )
                    correlation = self.pending.pop((opposite, key), {})
                kind = (
                    "notification"
                    if request and "id" not in value
                    else "request"
                    if request
                    else "result"
                    if "result" in value
                    else "error"
                )
                sequence = self.emit(
                    kind,
                    {
                        **evidence,
                        "rpc": public_value(value),
                        "correlation": correlation,
                    },
                )
                if request and "id" in value and sequence is not None:
                    if len(self.pending) >= MAX_PENDING:
                        self.pending.pop(next(iter(self.pending)))
                    self.pending[(direction, key)] = {
                        "request_seq": sequence,
                        "method": public_value(value["method"], "method"),
                        "tool": public_value(
                            value.get("params", {}).get("name"), "name"
                        )
                        if isinstance(value.get("params"), dict)
                        else None,
                    }
            except (ValueError, UnicodeError, RecursionError):
                self.emit("malformed_packet", evidence)

    def close(self, result):
        with self.lock:
            self.emit(
                "end",
                {
                    **result,
                    "packets": self.counts,
                    "omitted_records": self.omitted,
                    "trace_write_failed": self.failed,
                },
                final=True,
            )
            self.closed = True
            self.file.close()


class Packets:
    def __init__(self, trace, direction):
        self.trace, self.direction = trace, direction
        self.reset()

    def reset(self):
        self.buffer = bytearray()
        self.size = 0
        self.hash = hashlib.sha256()

    def feed(self, data):
        for piece in data.splitlines(keepends=True):
            self.hash.update(piece)
            self.size += len(piece)
            if self.buffer is not None:
                if self.size <= MAX_PACKET_BYTES:
                    self.buffer.extend(piece)
                else:
                    self.buffer = None
            if piece.endswith(b"\n"):
                self.finish()

    def finish(self, complete=True):
        if self.size:
            self.trace.packet(
                self.direction, self.buffer, self.size, self.hash.hexdigest(), complete
            )
        self.reset()


def write_all(descriptor, data):
    view = memoryview(data)
    while view:
        # Small writes avoid a large blocked pipe write coupling both relay directions.
        count = os.write(descriptor, view[:512])
        view = view[count:]


def relay(command, trace):
    """Pipe exact bytes; daemon input reader cannot hold shutdown on an open parent stdin."""
    try:
        environment = {
            key: value
            for key, value in os.environ.items()
            if key
            in {
                "PATH",
                "LANG",
                "LC_ALL",
                "SYSTEMROOT",
                "WINDIR",
                "TMPDIR",
                "TEMP",
                "TMP",
                "PYTHONUTF8",
                "PYTHONIOENCODING",
                "PYTHONUNBUFFERED",
            }
        }
        child = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=0,
            start_new_session=os.name != "nt",
            env=environment,
        )
    except OSError as exc:
        trace.close(
            {
                "exit_code": 127,
                "reason": "child launch failed",
                "error_type": type(exc).__name__,
            }
        )
        return 127
    eof = threading.Event()
    broken = threading.Event()
    interrupted = []

    def stop(number=signal.SIGTERM):
        if child.poll() is None:
            try:
                if os.name == "nt":
                    child.terminate()
                else:
                    os.killpg(child.pid, number)
            except ProcessLookupError:
                pass

    def transfer(source, destination, direction, input_side=False):
        packets = Packets(trace, direction)
        try:
            while True:
                data = os.read(source, CHUNK_BYTES)
                if not data:
                    break
                packets.feed(data)
                write_all(destination, data)
        except OSError:
            broken.set()
        finally:
            packets.finish(complete=False)
            if input_side:
                child.stdin.close()
                eof.set()

    reader = threading.Thread(
        target=transfer,
        args=(sys.stdin.fileno(), child.stdin.fileno(), "client_to_child", True),
        daemon=True,
    )
    writer = threading.Thread(
        target=transfer,
        args=(child.stdout.fileno(), sys.stdout.fileno(), "child_to_client"),
        daemon=True,
    )
    previous = {}

    def interrupt(number, _):
        interrupted.append(number)
        stop(number)

    for number in (signal.SIGTERM, signal.SIGINT):
        previous[number] = signal.signal(number, interrupt)
    reader.start()
    writer.start()
    deadline = None
    try:
        while child.poll() is None:
            if (eof.is_set() or broken.is_set() or interrupted) and deadline is None:
                deadline = time.monotonic() + EXIT_GRACE_SECONDS
                if broken.is_set():
                    stop()
            if deadline is not None and time.monotonic() >= deadline:
                stop(signal.SIGKILL)
            time.sleep(0.02)
        writer.join(EXIT_GRACE_SECONDS)
        if writer.is_alive():
            broken.set()
    finally:
        stop(signal.SIGKILL)
        child.wait()
        child.stdout.close()
        child.stdin.close()
        for number, handler in previous.items():
            signal.signal(number, handler)
        trace.close(
            {
                "exit_code": child.returncode,
                "stdin_closed": eof.is_set(),
                "relay_failed": broken.is_set(),
                "signal": interrupted[0] if interrupted else None,
            }
        )
    return (
        (child.returncode or int(broken.is_set()))
        if child.returncode >= 0
        else 128 - child.returncode
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--kit-manifest", required=True, type=Path)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if os.name == "nt":
            raise ValueError("POSIX stdio recorder; Windows is unverified")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", args.run_id):
            raise ValueError("Run ID must be a safe identifier of 1-64 characters")
        config = args.config.resolve(strict=True)
        config_bytes = bounded_read(config, 4096)
        header = {
            "run_id": args.run_id,
            "config": {
                **configuration(config, config_bytes),
                "snapshot": "private immutable launch copy",
            },
            "kit": kit_provenance(args.kit_manifest),
            "simulated": True,
            "physical_verified": False,
            "scope": "observed stdio; caller identity/Grok invocation requires independent receipts",
        }
        command = simulator_command(
            args.command[1:] if args.command[:1] == ["--"] else args.command, config
        )
        header["child_executable"] = fingerprint(
            bounded_read(command[0], MAX_ARTIFACT_BYTES)
        )
        trace = Trace(args.output, header)
    except (OSError, ValueError, RecursionError):
        parser.error(
            "Unsafe simulator invocation, invalid bounded inputs, or output already exists"
        )
    # The child reads the exact fingerprinted bytes even if the operator later edits
    # the original file. This changes only its local path, never the stdio bytes.
    try:
        with tempfile.TemporaryDirectory(prefix="grok-mcp-trace-") as temporary:
            snapshot = Path(temporary) / "simulator-config.json"
            with snapshot.open("xb") as handle:
                os.chmod(snapshot, 0o600)
                handle.write(config_bytes)
            command[command.index("--simulator-config") + 1] = str(snapshot)
            result = relay(command, trace)
    except OSError:
        if not trace.closed:
            trace.close(
                {"exit_code": 1, "reason": "private config snapshot unavailable"}
            )
        print(
            "Recorder could not prepare or clean its private config snapshot",
            file=sys.stderr,
        )
        result = 1
    if trace.failed:
        print("Trace incomplete: evidence output failed", file=sys.stderr)
        result = result or 1
    return result


if __name__ == "__main__":
    raise SystemExit(main())
