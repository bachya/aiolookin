"""Define dynamic fixtures."""
import json

import pytest

from .common import load_fixture


@pytest.fixture(name="device_info", scope="session")
def device_info_fixture():
    """Load the controller state fixture data."""
    return json.loads(load_fixture("device_info.json"))
