"""Get a device and print the latest values of its onboard sensors."""
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
        except LookInError as err:
            _LOGGER.error("There was an error while getting the device: %s", err)

        try:
            data = await device.sensor.async_get_ir_value()
            _LOGGER.info("Latest IR data: %s", data)
        except LookInError as err:
            _LOGGER.error("There was an error while getting IR data: %s", err)

        try:
            data = await device.sensor.async_get_meteo_value()
            _LOGGER.info("Latest Meteo data: %s", data)
        except LookInError as err:
            _LOGGER.error("There was an error while getting Meteo data: %s", err)


asyncio.run(main())
