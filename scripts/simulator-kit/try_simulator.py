"""Assertion-backed local MCP demonstration. No Grok or physical device calls."""

import argparse
import asyncio
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from grok_gadgets_gateway.simulator_config import load_config


def _field(result, name, old_name):
    """mcp 2 renamed result fields to snake_case; accept both so the kit runs on either."""
    return getattr(result, name) if hasattr(result, name) else getattr(result, old_name)


async def demo(path):
    config = load_config(path)
    device_id = config["device_id"]
    params = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "grok_gadgets_gateway.cli",
            "--simulator",
            "--simulator-config",
            str(path),
            "--test-controls",
        ],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as client:
            await client.initialize()

            async def call(name, arguments=None):
                result = await client.call_tool(name, arguments or {})
                assert not _field(result, "is_error", "isError"), result.content
                value = _field(
                    result, "structured_content", "structuredContent"
                ) or json.loads(result.content[0].text)
                print(
                    json.dumps(
                        {"tool": name, "arguments": arguments or {}, "result": value}
                    )
                )
                return value

            device = (await call("gadgets_list_devices"))["devices"][0]
            assert device["device_id"] == device_id and device["simulated"]
            assert device["display_name"] == config["display_name"]
            assert device["state"]["rgb"] == config["initial_rgb"]
            assert device["available"] is not config["start_disconnected"]
            request = {
                "device_id": device_id,
                "capability": "rgb.set",
                "arguments": {"r": 0, "g": 0, "b": 255, "on": True},
            }
            if config["start_disconnected"]:
                assert (
                    await call(
                        "gadgets_command", {**request, "command_id": "kit-offline"}
                    )
                )["error"]["code"] == "unavailable"
                await call("test_simulator_control", {"action": "reconnect"})
            command = (
                await call("gadgets_command", {**request, "command_id": "kit-blue"})
            )["command"]
            assert (
                command["status"] == "executed"
                and command["simulated"]
                and not command["physical_verified"]
                and command.get("duplicate") is False
            )
            assert command["reported_state"]["rgb"] == request["arguments"]
            assert (await call("gadgets_get_state", {"device_id": device_id}))[
                "device"
            ]["state"]["rgb"] == request["arguments"]
            receipt = {
                key: value for key, value in command.items() if key != "duplicate"
            }
            assert (await call("gadgets_command_status", {"command_id": "kit-blue"}))[
                "command"
            ] == receipt
            for pressed in (True, False):
                await call(
                    "test_simulator_control", {"action": "button", "pressed": pressed}
                )
            events = await call("gadgets_read_events", {"device_id": device_id})
            assert [event["data"]["pressed"] for event in events["events"]] == [
                True,
                False,
            ]
            assert (
                await call(
                    "gadgets_read_events",
                    {"device_id": device_id, "cursor": events["next_cursor"]},
                )
            )["events"] == []
            await call(
                "gadgets_command",
                {
                    **request,
                    "arguments": {"r": 0, "g": 0, "b": 0, "on": False},
                    "command_id": "kit-off",
                },
            )
            assert not (await call("gadgets_get_state", {"device_id": device_id}))[
                "device"
            ]["state"]["rgb"]["on"]
            assert not (await call("gadgets_diagnostics"))["report"][
                "physical_verified"
            ]
    print(
        json.dumps(
            {
                "evidence": "Local official MCP client over stdio",
                "simulated": True,
                "grok_verified": False,
                "physical_verified": False,
            }
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parent / "simulator-config.json",
    )
    asyncio.run(demo(parser.parse_args().config.resolve()))
