import json
import pytest
from .core import HyperDriveAPI


def test_create(hyperdrive_api) -> None:
    json_response  = hyperdrive_api.new_v1()
    # dict ok
    print(json_response)
    # print(json_response['ark'])
    # str error
    # response = json.loads(json_response)
    # assert response.get('ERROR') == None
    