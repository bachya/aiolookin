"""Define tests for the device's onboard sensors."""
import json

import aiohttp
import pytest

from aiolookin import async_get_device
from aiolookin.errors import SensorError

from .common import TEST_IP_ADDRESS


@pytest.mark.asyncio
async def test_invalid_sensor_type(
    aresponses, device_info, ir_sensor_value, sensor_list
):
    """Test that requesting an unsupported sensor type throws the proper exception."""
    sensor_list = []

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
    aresponses.add(
        TEST_IP_ADDRESS,
        "/sensors",
        "get",
        aresponses.Response(
            text=json.dumps(sensor_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        TEST_IP_ADDRESS,
        "/sensors/IR",
        "get",
        aresponses.Response(
            text=json.dumps(ir_sensor_value),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        device = await async_get_device(TEST_IP_ADDRESS, session=session)

        with pytest.raises(SensorError) as err:
            await device.sensor.async_get_ir_value()
            assert "Unknown sensor type" in str(err)


@pytest.mark.asyncio
async def test_sensor_values(
    aresponses, device_info, ir_sensor_value, meteo_sensor_value, sensor_list
):
    """Test getting the latest value of a device's sensors."""
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
    aresponses.add(
        TEST_IP_ADDRESS,
        "/sensors",
        "get",
        aresponses.Response(
            text=json.dumps(sensor_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        TEST_IP_ADDRESS,
        "/sensors/IR",
        "get",
        aresponses.Response(
            text=json.dumps(ir_sensor_value),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        TEST_IP_ADDRESS,
        "/sensors",
        "get",
        aresponses.Response(
            text=json.dumps(sensor_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        TEST_IP_ADDRESS,
        "/sensors/Meteo",
        "get",
        aresponses.Response(
            text=json.dumps(meteo_sensor_value),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        device = await async_get_device(TEST_IP_ADDRESS, session=session)

        ir_data = await device.sensor.async_get_ir_value()
        assert ir_data["Protocol"] == "01"

        meteo_data = await device.sensor.async_get_meteo_value()
        assert meteo_data["Humidity"] == "62"
