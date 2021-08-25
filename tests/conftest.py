"""Define dynamic fixtures."""
import json

import pytest

from .common import TEST_IP_ADDRESS, load_fixture


@pytest.fixture(name="device_server")
def device_server_fixture(aresponses, device_info):
    """Define a fixture to an aresponses server that represents a device."""
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

    return aresponses


@pytest.fixture(name="device_info", scope="session")
def device_info_fixture():
    """Define a fixture to return device data."""
    return json.loads(load_fixture("device_info.json"))


@pytest.fixture(name="ir_sensor_value", scope="session")
def ir_sensor_value_fixture():
    """Define a fixture to return IR sensor data."""
    return json.loads(load_fixture("ir_sensor_value.json"))


@pytest.fixture(name="meteo_sensor_value", scope="session")
def meteo_sensor_value_fixture():
    """Define a fixture to return Meteo sensor data."""
    return json.loads(load_fixture("meteo_sensor_value.json"))


@pytest.fixture(name="sensor_list", scope="session")
def sensor_list_fixture():
    """Define a fixture to return a list of onboard sensors."""
    return json.loads(load_fixture("sensor_list.json"))
