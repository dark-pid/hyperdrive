import pytest
from flask import jsonify
from app.util.validation import ValidationUtil
from app.util.config_manager import ConfigManager


config_manager = ConfigManager()


# tests for synchronous external url addition method

def mock_add_url(VERIFICATION_METHOD, external_url):
    try:
        # Simulates URL validation behavior
        if VERIFICATION_METHOD == "BASIC":
            if ValidationUtil.check_url(external_url) == False:
                return {"status": "error", "message": "invalid url"}, 400
        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if len(external_url) == 0:
                return {"status": "error", "message": "invalid url"}, 400
        else:
            return {"status": "error", "message": "the method could not be implemented"}, 400

        # Simulates a successful response
        return {"status": "success", "message": "executed"}, 200

    except Exception as e:
        # Simulates a generic error response
        return jsonify({"error": str(e)}), 400

def test_add_url_validation_success():
    config_manager.set_url_validation("BASIC")
    VERIFICATION_METHOD = config_manager.get_url_validation()
    result = mock_add_url(VERIFICATION_METHOD, "http://www.uol.com/123456")
    assert 200 in result

def test_add_url_validation_failure():
    config_manager.set_url_validation("BASIC")
    VERIFICATION_METHOD = config_manager.get_url_validation()
    result = mock_add_url(VERIFICATION_METHOD, "invalid_url")
    assert 400 in result
