"""Get a device and print its info."""
import asyncio
import logging

from aiohttp import ClientSession

from aiolookin import async_get_device
from aiolookin.errors import LookInError

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            device = await async_get_device("172.16.20.236", session=session)
            _LOGGER.info("Device ID: %s", device.device_id)
            _LOGGER.info("Device Mode: %s", device.device_mode)
            _LOGGER.info("Eco Mode Enabled: %s", device.eco_mode_enabled)
            _LOGGER.info("Firmware: %s", device.firmware)
            _LOGGER.info("HomeKit Enabled: %s", device.homekit_enabled)
            _LOGGER.info("Internal Temperature (C): %s", device.internal_temp_c)
            _LOGGER.info("MRDC: %s", device.mrdc)
            _LOGGER.info("Name: %s", device.name)
            _LOGGER.info("Power Mode: %s", device.power_mode)
            _LOGGER.info("Status: %s", device.status)
            _LOGGER.info("Type: %s", device.type)
            _LOGGER.info("Voltage: %s", device.voltage)
        except LookInError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.run(main())
