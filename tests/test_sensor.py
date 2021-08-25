"""Define tests for the device's onboard sensors."""
import json

import aiohttp
import pytest

from aiolookin import async_get_device
from aiolookin.errors import SensorError

from .common import TEST_IP_ADDRESS


@pytest.mark.asyncio
async def test_invalid_sensor_type(aresponses, device_server, sensor_list):
    """Test that requesting an unsupported sensor type throws the proper exception."""
    device_server.add(
        TEST_IP_ADDRESS,
        "/sensors",
        "get",
        aresponses.Response(
            text=json.dumps(sensor_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        device = await async_get_device(TEST_IP_ADDRESS, session=session)

        with pytest.raises(SensorError) as err:
            await device.sensor.async_get_sensor_value("Fake Sensor")
            assert "Unknown sensor type" in str(err)


@pytest.mark.asyncio
async def test_sensor_values(
    aresponses, device_server, ir_sensor_value, meteo_sensor_value, sensor_list
):
    """Test getting the latest value of a device's sensors."""
    device_server.add(
        TEST_IP_ADDRESS,
        "/sensors",
        "get",
        aresponses.Response(
            text=json.dumps(sensor_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    device_server.add(
        TEST_IP_ADDRESS,
        "/sensors/IR",
        "get",
        aresponses.Response(
            text=json.dumps(ir_sensor_value),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    device_server.add(
        TEST_IP_ADDRESS,
        "/sensors",
        "get",
        aresponses.Response(
            text=json.dumps(sensor_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    device_server.add(
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

        ir_data = await device.sensor.async_get_sensor_value("IR")
        assert ir_data["Protocol"] == "01"

        meteo_data = await device.sensor.async_get_sensor_value("Meteo")
        assert meteo_data["Humidity"] == "62"


@pytest.mark.asyncio
async def test_sensor_list(aresponses, device_server, sensor_list):
    """Test getting the list of sensors supported by the device."""
    device_server.add(
        TEST_IP_ADDRESS,
        "/sensors",
        "get",
        aresponses.Response(
            text=json.dumps(sensor_list),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        device = await async_get_device(TEST_IP_ADDRESS, session=session)
        sensors = await device.sensor.async_get_sensor_list()
        assert sensors == ["IR", "Meteo"]
