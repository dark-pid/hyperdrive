import json
import os
import configparser

from flask import (
    Blueprint,
    Flask,
    jsonify,
    render_template,
    send_file,
    abort,
    request,
    make_response,
)
from web3 import Web3

from dark import DarkMap, DarkGateway
from util.validation import ValidationUtil
from util.responses import success_response, error_response
from util.config_manager import ConfigManager


# configurando classe das váriaveis externas
config_manager = ConfigManager()
async_mode = config_manager.get_operation_mode()

##
# configuring dARK GW
##

bc_config = configparser.ConfigParser()
deployed_contracts_config = configparser.ConfigParser()

# bc configuration
PROJECT_ROOT = "./"
bc_config.read(os.path.join(PROJECT_ROOT, "config.ini"))
# deployed contracts config
deployed_contracts_config.read(os.path.join(PROJECT_ROOT, "deployed_contracts.ini"))


# gw
dark_gw = DarkGateway(bc_config, deployed_contracts_config)

#
dark_map = DarkMap(dark_gw)

###
### methods
###


# Set the external variable -> config_manager.set_url_validation("BASIC")
async def add_url(ark_id, external_url):
    try:
        VERIFICATION_METHOD = config_manager.get_url_validation()
    except:
        VERIFICATION_METHOD = None

    try:
        action = "add_url"
        pid = None
        if ark_id.startswith("0x"):
            pid = dark_map.get_pid_by_hash(ark_id)
        else:
            pid = dark_map.get_pid_by_ark(ark_id)

        if VERIFICATION_METHOD == "BASIC":
            if ValidationUtil.check_url(external_url) == False:
                return make_response(error_response(pid,async_mode.lower(), action, external_url, "Invalid URL", 400))
        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if len(external_url) == 0:
                return make_response(error_response(pid,async_mode.lower(), action, external_url, "Invalid URL", 400))
        else:
            return make_response(error_response(pid,async_mode.lower(), action, external_url, "the method could not be implemented", 400))

        tx_set = dark_map.async_set_url(pid.pid_hash, external_url)
        tx_status, tx_recipt = dark_gw.transaction_was_executed(tx_set)

        response = success_response(pid, async_mode.lower(), action, external_url, "queued")

        return response

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)


# Set the external variable -> config_manager.set_external_pid_validation("BASIC")
async def add_external_pid(ark_id, external_pid):
    try:
        VERIFICATION_METHOD = config_manager.get_external_pid_validation()

    except:
        VERIFICATION_METHOD = None

    try:
        action = "add_external_pid"
        pid = None
        
        if ark_id.startswith("0x"):
            pid = dark_map.get_pid_by_hash(ark_id)
        else:
            pid = dark_map.get_pid_by_ark(ark_id)

        if VERIFICATION_METHOD == "BASIC":
            if external_pid.startswith("doi:/") == False:
                return make_response(error_response(pid,async_mode.lower(), action, external_pid, "Invalid PID", 400))

        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if len(external_pid) == 0:
                return make_response(error_response(pid,async_mode.lower(), action, external_pid, "Invalid PID", 400))
        else:
            return make_response(error_response(pid,async_mode.lower(), action, external_pid,"queued" ,"the method could not, be implemented", 400))

        valid_pid = external_pid.split(":/")[1]
        tx_set = dark_map.async_set_external_pid(pid.pid_hash, valid_pid)
        tx_status, tx_recipt = dark_gw.transaction_was_executed(tx_set)

        response = success_response(pid, async_mode.lower(), action, external_pid, "queued")

        return response

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)


# Set the external variable -> config_manager.set_payload_validation("BASIC")
async def set_payload(ark_id, payload):
    try:
        VERIFICATION_METHOD = config_manager.get_payload_validation()

    except:
        VERIFICATION_METHOD = None

    try:
        action = "set_payload"
        pid = None
        if VERIFICATION_METHOD == "BASIC":
            payload = json.loads(payload)

            if type(payload) != dict or len(payload) == 0:
                return make_response(error_response(pid,async_mode.lower(), action, payload, "Invalid JSON payload", 400))

        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if type(payload) != dict or len(payload) == 0:
                return make_response(error_response(pid,async_mode.lower(), action, payload, "Invalid JSON payload", 400))
        else:
            return make_response(error_response(pid,async_mode.lower(), action, payload, "the method could not be implemented", 400))

        if ark_id.startswith("0x"):
            pid = dark_map.get_pid_by_hash(ark_id)
        else:
            pid = dark_map.get_pid_by_ark(ark_id)

        tx_set = dark_map.async_set_payload(pid.pid_hash, payload)
        tx_status, tx_recipt = dark_gw.transaction_was_executed(tx_set)

        response = success_response(pid, async_mode.lower(), action, payload,"queued")

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 400
