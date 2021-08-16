"""Define anything needed to connect to a LOOK.in device."""
import json
from typing import Any, Dict, Optional

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .const import LOGGER
from .errors import RequestError

DEFAULT_TIMEOUT = 10

DEVICE_MODE_EXECUTOR = "Executor"
DEVICE_MODE_SENSOR = "Sensor"
DEVICE_MODE_UNKNOWN = "Unknown"

DEVICE_MODE_MAP = {
    "0": DEVICE_MODE_EXECUTOR,
    "1": DEVICE_MODE_SENSOR,
}


class Device:
    """Define the device."""

    def __init__(
        self, ip_address: str, *, session: Optional[ClientSession] = None
    ) -> None:
        """Initialize."""
        self._device_info: Dict[str, str] = {}
        self._ip_address = ip_address
        self._session = session

    def __repr__(self) -> str:
        """Return a string representation of the device."""
        return f"<Device type={self.type} id={self.device_id}>"

    @property
    def device_id(self) -> str:
        """Return the device id."""
        return self._device_info["ID"]

    @property
    def device_mode(self) -> str:
        """Return the device mode."""
        raw_mode = self._device_info["SensorMode"]
        if raw_mode not in DEVICE_MODE_MAP:
            LOGGER.debug("Unknown device mode value: %s", raw_mode)
            return DEVICE_MODE_UNKNOWN
        return DEVICE_MODE_MAP[raw_mode]

    @property
    def eco_mode_enabled(self) -> bool:
        """Return whether the device has Eco mode enabled."""
        return self._device_info["EcoMode"] == "on"

    @property
    def firmware(self) -> str:
        """Return the device firmware."""
        return self._device_info["Firmware"]

    @property
    def homekit_enabled(self) -> bool:
        """Return whether the device is HomeKit-enabled."""
        return bool(self._device_info["HomeKit"])

    @property
    def internal_temp_c(self) -> int:
        """Return the device's internal temperature in C."""
        return int(self._device_info["Temperature"])

    @property
    def mrdc(self) -> str:
        """Return the MRDC (?)."""
        return self._device_info["MRDC"]

    @property
    def name(self) -> str:
        """Return the name."""
        return self._device_info["Name"]

    @property
    def power_mode(self) -> str:
        """Return the power mode."""
        return self._device_info["PowerMode"]

    @property
    def status(self) -> str:
        """Return the status."""
        return self._device_info["Status"]

    @property
    def type(self) -> str:
        """Return the device type."""
        return self._device_info["Type"]

    @property
    def voltage(self) -> int:
        """Return the current voltage in millivolts."""
        return int(self._device_info["CurrentVoltage"])

    async def _async_request(
        self, method: str, endpoint: str, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make an API request."""
        url = f"http://{self._ip_address}/{endpoint}"
        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        assert session

        data: Dict[str, Any] = {}

        try:
            async with session.request(method, url, **kwargs) as resp:
                data = await resp.json()
                resp.raise_for_status()
        except (ClientError, json.decoder.JSONDecodeError) as err:
            raise RequestError(f"Error while requesting {url}: {err}") from err
        finally:
            if not use_running_session:
                await session.close()

        LOGGER.debug("Received data for %s: %s", url, data)

        return data

    async def async_update_device_info(self) -> None:
        """Get the latest device info.

        Intended to be called right after instantiating the object.
        """
        self._device_info = await self._async_request("get", "device")


async def async_get_device(
    ip_address: str, *, session: Optional[ClientSession] = None
) -> Device:
    """Get a fully initialized device."""
    device = Device(ip_address, session=session)
    await device.async_update_device_info()
    return device
