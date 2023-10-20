import pytest
import json
from app.util.validation import ValidationUtil

# external url validation tests

def test_add_url_valid():

    url = "http://www.hyperdrive.com/123456"
    assert ValidationUtil.check_url(url) is True

def test_add_url_invalid():

    url = "hello 123"
    assert ValidationUtil.check_url(url) is False

def test_add_empty_url():

    url = ""
    assert ValidationUtil.check_url(url) is False

def test_check_url_invalid_none():

    url = None
    assert ValidationUtil.check_url(url) is False

# external pid validation tests

def mock_validation_pid(external_pid):

    if external_pid.startswith("doi:/"):
        valid_pid = external_pid.split(":/")[1]
        return valid_pid
    else:
        return False

def test_mock_validation_pid_valid_pid():

    external_pid = "doi:/116.jdakt.7892"
    result = mock_validation_pid(external_pid)
    assert result == "116.jdakt.7892"

def test_mock_validation_pid_invalid_pid():

    external_pid = "DOIXPTO"
    result = mock_validation_pid(external_pid)
    assert result is False

def test_mock_validation_pid_empty_pid():

    external_pid = ""
    result = mock_validation_pid(external_pid)
    assert result is False

# payload validation tests
def mock_validation_payload(payload):

    if type(payload) != dict:
        try:
            payload = json.loads(payload)
            return payload
        except Exception:
            return False
    else:
        return payload

def test_mock_validation_payload_valid_dict():

    payload = {"key": "value", "number": 42}
    result = mock_validation_payload(payload)
    assert result == payload

def test_mock_validation_payload_valid_json_str():

    payload_str = '{"key": "value", "number": 42}'
    result = mock_validation_payload(payload_str)
    assert result == json.loads(payload_str)

def test_mock_validation_payload_invalid_json_str():

    payload_str = "{x : y}"
    result = mock_validation_payload(payload_str)
    assert result is False

def test_mock_validation_payload_invalid_type():

    payload = 123
    result = mock_validation_payload(payload)
    assert result is False
