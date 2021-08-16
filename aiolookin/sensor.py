"""Define endpoints to manage sensor data."""
from typing import Any, Awaitable, Callable, Dict, cast

from .errors import SensorError


class Sensor:
    """Define a sensor data object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request = async_request

    async def _async_get_sensor_value(self, sensor_type: str) -> Dict[str, Any]:
        """Get the latest value of a particular sensor."""
        sensor_list = await self._async_request("get", "sensors")
        if sensor_type not in sensor_list:
            raise SensorError(f"Unknown sensor type: {sensor_type}")

        data = cast(
            Dict[str, Any], await self._async_request("get", f"sensors/{sensor_type}")
        )
        return data

    async def async_get_ir_value(self) -> Dict[str, Any]:
        """Get the latest value of the device's onboard IR sensor."""
        return await self._async_get_sensor_value("IR")

    async def async_get_meteo_value(self) -> Dict[str, Any]:
        """Get the latest value of the device's onboard Meteo sensor."""
        return await self._async_get_sensor_value("Meteo")
