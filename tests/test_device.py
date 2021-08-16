"""Define tests for the device."""
import json
import logging

import aiohttp
import pytest

from aiolookin import async_get_device
from aiolookin.errors import RequestError

from .common import TEST_IP_ADDRESS


@pytest.mark.asyncio
async def test_api_error(aresponses):
    """Test the API returning a non-2xx HTTP code."""
    aresponses.add(
        TEST_IP_ADDRESS,
        "/device",
        "get",
        aresponses.Response(
            text="Bad Request",
            status=400,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(RequestError):
            await async_get_device(TEST_IP_ADDRESS, session=session)


@pytest.mark.asyncio
async def test_device_properties(aresponses, device_info):
    """Test getting device properties."""
    aresponses.add(
        TEST_IP_ADDRESS,
        "/device",
        "get",
        aresponses.Response(
            text=json.dumps(device_info),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        device = await async_get_device(TEST_IP_ADDRESS, session=session)
        assert device.device_id == "ABCD1234"
        assert device.device_mode == "Executor"
        assert device.eco_mode_enabled is True
        assert device.firmware == "2.36"
        assert device.homekit_enabled is True
        assert device.internal_temp_c == 53
        assert device.mrdc == "1234567890ABCDEF"
        assert device.name == "Test Device"
        assert device.power_mode == "5v"
        assert device.status == "Running"
        assert device.type == "Remote"
        assert device.voltage == 5889


@pytest.mark.asyncio
async def test_device_properties_new_session(aresponses, device_info):
    """Test getting device properties without an explicit ClientSession."""
    aresponses.add(
        TEST_IP_ADDRESS,
        "/device",
        "get",
        aresponses.Response(
            text=json.dumps(device_info),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    device = await async_get_device(TEST_IP_ADDRESS)
    assert device.device_id == "ABCD1234"
    assert device.device_mode == "Executor"
    assert device.eco_mode_enabled is True
    assert device.firmware == "2.36"
    assert device.homekit_enabled is True
    assert device.internal_temp_c == 53
    assert device.mrdc == "1234567890ABCDEF"
    assert device.name == "Test Device"
    assert device.power_mode == "5v"
    assert device.status == "Running"
    assert device.type == "Remote"
    assert device.voltage == 5889


@pytest.mark.asyncio
async def test_device_representation(aresponses, device_info):
    """Test that a device is represented as a string correctly."""
    aresponses.add(
        TEST_IP_ADDRESS,
        "/device",
        "get",
        aresponses.Response(
            text=json.dumps(device_info),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        device = await async_get_device(TEST_IP_ADDRESS, session=session)
        assert str(device) == "<Device type=Remote id=ABCD1234>"


@pytest.mark.asyncio
async def test_unknown_device_mode(aresponses, caplog, device_info):
    """Test that an unknown device mode is captured correctly."""
    caplog.set_level(logging.DEBUG)

    device_info["SensorMode"] = "2"

    aresponses.add(
        TEST_IP_ADDRESS,
        "/device",
        "get",
        aresponses.Response(
            text=json.dumps(device_info),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        device = await async_get_device(TEST_IP_ADDRESS, session=session)
        assert device.device_mode == "Unknown"
        assert any("Unknown device mode" in e.message for e in caplog.records)
