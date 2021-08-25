"""Define endpoints to manage sensor data."""
from typing import Any, Awaitable, Callable, Dict, List, cast

from .errors import SensorError


class SensorAPI:
    """Define a sensor data object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request = async_request

    async def async_get_sensor_value(self, sensor: str) -> Dict[str, Any]:
        """Get the latest value of a particular sensor."""
        sensor_list = await self.async_get_sensor_list()

        if sensor not in sensor_list:
            raise SensorError(f"Unknown sensor: {sensor}")

        data = await self._async_request("get", f"sensors/{sensor}")
        return cast(Dict[str, Any], data)

    async def async_get_sensor_list(self) -> List[str]:
        """Get the list of sensors supported by the device."""
        data = await self._async_request("get", "sensors")
        return cast(List[str], data)
