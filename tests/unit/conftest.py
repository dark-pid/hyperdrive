import pytest
from.core import HyperDriveAPI


@pytest.fixture(scope="session")
def hyperdrive_api():
    hyperdrive_api = HyperDriveAPI()
    return hyperdrive_api