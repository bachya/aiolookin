"""Define tests for the device's onboard sensors."""
import json

import aiohttp
import pytest

from aiolookin import async_get_device
from aiolookin.errors import CommandError

from .common import TEST_IP_ADDRESS


@pytest.mark.asyncio
async def test_command_list(aresponses, device_server, command_list):
    """Test getting the list of commands supported by the device."""
    device_server.add(
        TEST_IP_ADDRESS,
        "/commands",
        "get",
        aresponses.Response(
            text=json.dumps(command_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        device = await async_get_device(TEST_IP_ADDRESS, session=session)
        commands = await device.command.async_get_command_list()
        assert commands == ["IR"]


@pytest.mark.asyncio
async def test_command_action_list(
    aresponses, command_list, device_server, ir_command_action_list
):
    """Test getting the list of actions supported by the IR command."""
    device_server.add(
        TEST_IP_ADDRESS,
        "/commands",
        "get",
        aresponses.Response(
            text=json.dumps(command_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    device_server.add(
        TEST_IP_ADDRESS,
        "/commands/IR",
        "get",
        aresponses.Response(
            text=json.dumps(ir_command_action_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        device = await async_get_device(TEST_IP_ADDRESS, session=session)
        actions = await device.command.async_get_command_action_list("IR")
        assert actions == [
            "ac",
            "aiwa",
            "localremote",
            "nec1",
            "necx",
            "panasonic",
            "prontohex",
            "prontohex-blocked",
            "raw",
            "repeat",
            "samsung36",
            "saved",
            "sony",
        ]


@pytest.mark.asyncio
async def test_invalid_command_or_action(
    aresponses, device_server, command_list, ir_command_action_list
):
    """Test that requesting an unsupported command or action throws the proper exception."""
    device_server.add(
        TEST_IP_ADDRESS,
        "/commands",
        "get",
        aresponses.Response(
            text=json.dumps(command_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    device_server.add(
        TEST_IP_ADDRESS,
        "/commands",
        "get",
        aresponses.Response(
            text=json.dumps(command_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    device_server.add(
        TEST_IP_ADDRESS,
        "/commands/IR",
        "get",
        aresponses.Response(
            text=json.dumps(ir_command_action_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        device = await async_get_device(TEST_IP_ADDRESS, session=session)

        with pytest.raises(CommandError) as err:
            await device.command.async_send_command("Fake Command", "Fake Action")
            assert str(err) == "Unknown command: Fake Command"

        with pytest.raises(CommandError) as err:
            await device.command.async_send_command("IR", "Fake Action")
            assert str(err) == 'Unknown action for command "IR": Fake Action'


@pytest.mark.asyncio
async def test_send_command(
    aresponses, command_list, command_response, device_server, ir_command_action_list
):
    """Test that requesting an unsupported command or action throws the proper exception."""
    device_server.add(
        TEST_IP_ADDRESS,
        "/commands",
        "get",
        aresponses.Response(
            text=json.dumps(command_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    device_server.add(
        TEST_IP_ADDRESS,
        "/commands/IR",
        "get",
        aresponses.Response(
            text=json.dumps(ir_command_action_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    device_server.add(
        TEST_IP_ADDRESS,
        "/commands",
        "post",
        aresponses.Response(
            text=json.dumps(command_response),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        device = await async_get_device(TEST_IP_ADDRESS, session=session)
        data = await device.command.async_send_command("IR", "nec1", operand="123abc")
        assert data == {"success": "true"}
