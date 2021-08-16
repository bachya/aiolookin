# 📶 aiolookin: an asyncio-based, Python3 library for LOOK.in devices

[![CI](https://github.com/bachya/aiolookin/workflows/CI/badge.svg)](https://github.com/bachya/aiolookin/actions)
[![PyPi](https://img.shields.io/pypi/v/aiolookin.svg)](https://pypi.python.org/pypi/aiolookin)
[![Version](https://img.shields.io/pypi/pyversions/aiolookin.svg)](https://pypi.python.org/pypi/aiolookin)
[![License](https://img.shields.io/pypi/l/aiolookin.svg)](https://github.com/bachya/aiolookin/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/aiolookin/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/aiolookin)
[![Maintainability](https://api.codeclimate.com/v1/badges/a683f20d63d4735ceede/maintainability)](https://codeclimate.com/github/bachya/aiolookin/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`aiolookin` is a Python 3, asyncio-friendly library for interacting with
[LOOK.in](https://look-in.club/en) devices.

# Python Versions

`aiolookin` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8
* Python 3.9

# Installation

```python
pip install aiolookin
```

# Usage

```python
import asyncio

from aiolookin import async_get_device


async def main() -> None:
    """Create the aiohttp session and run the example."""
    device = await async_get_device("<IP ADDRESS>")


asyncio.run(main())
```

By default, the library creates a new connection to Notion with each coroutine. If you
are calling a large number of coroutines (or merely want to squeeze out every second of
runtime savings possible), an
[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection
pooling:

```python
import asyncio

from aiohttp import ClientSession

from aiolookin import async_get_device


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        device = await async_get_device("<IP ADDRESS>")

        # Get to work...


asyncio.run(main())
```

## The `Device` Object

Each `Device` object obtained by `async_get_device` has a series of useful properties:

* `device_id`: the unique identifier of the device
* `device_mode`: either `Executor` or `Sensor`
* `eco_mode_enabled`: whether eco mode is enabled
* `firmware`: the current firmware version
* `homekit_enabled`: whether HomeKit is enabled
* `internal_temp_c`: the device's internal temperature (in Celsius)
* `mrdc`: the MRDC number (currently unknown what this does)
* `name`: the name of the device
* `power_mode`: the power mode of the device (A/C, battery)
* `status`: the current status of the device
* `type`: the type of device
* `voltage`: the voltage being applied to the device (in millivolts)

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/aiolookin/issues)
  or [initiate a discussion on one](https://github.com/bachya/aiolookin/issues/new).
2. [Fork the repository](https://github.com/bachya/aiolookin/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `script/test`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
