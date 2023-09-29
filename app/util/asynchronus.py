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
from util.config_manager import ConfigManager

# configurando classe das váriaveis externas
config_manager = ConfigManager()

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
        pid = None
        if ark_id.startswith("0x"):
            pid = dark_map.get_pid_by_hash(ark_id)
        else:
            pid = dark_map.get_pid_by_ark(ark_id)

        if VERIFICATION_METHOD == "BASIC":
            if ValidationUtil.check_url(external_url) == False:
                return make_response(jsonify({"error": "Invalid URL"}), 400)
        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if len(external_url) == 0:
                return make_response(jsonify({"error": "Invalid URL"}), 400)
        else:
            return make_response(
                jsonify({"error": "the method could not be implemented"}), 400
            )

        tx_set = dark_map.async_set_url(pid.pid_hash, external_url)
        tx_status, tx_recipt = dark_gw.transaction_was_executed(tx_set)

        result = {
            "pid": str(pid.ark),
            "pid_hash_index": Web3.toHex(pid.pid_hash),
            "action": "add_url",
            "parameter": external_url,
            "transaction_hash": tx_recipt,
            "tx_status": tx_status,
            "status": "queued",
        }

        return result, 200

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)

# Set the external variable -> config_manager.set_external_pid_validation("BASIC")
async def add_external_pid(ark_id, external_pid):
    try:
        VERIFICATION_METHOD = config_manager.get_external_pid_validation()

    except:
        VERIFICATION_METHOD = None

    try:
        pid = None

        if ark_id.startswith("0x"):
            pid = dark_map.get_pid_by_hash(ark_id)
        else:
            pid = dark_map.get_pid_by_ark(ark_id)

        if VERIFICATION_METHOD == "BASIC":
            if external_pid.startswith("doi:/") == False:
                return make_response(jsonify({"error": "Invalid Pid"}), 400)

        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if len(external_pid) == 0:
                return make_response(jsonify({"error": "Invalid Pid"}), 400)
        else:
            return make_response(jsonify({"error": "the method could not be implemented"}), 400)

        valid_pid = external_pid.split(":/")[1]
        tx_set = dark_map.async_set_external_pid(pid.pid_hash, valid_pid)
        tx_status, tx_recipt = dark_gw.transaction_was_executed(tx_set)

        result = {
                    "pid": str(pid.ark),
                    "pid_hash_index": str(pid.__hash__),
                    "action":  "external_pid_add",
                    "parameter": valid_pid,
                    "transaction_hash": tx_recipt,
                    "tx_status": tx_status,
                    "status": "queued",
        }

        return result, 200

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)


# Set the external variable -> config_manager.set_payload_validation("BASIC")
async def set_payload(ark_id, payload):
    try:
        VERIFICATION_METHOD = config_manager.get_payload_validation()

    except:
        VERIFICATION_METHOD = None

    try:
        if VERIFICATION_METHOD == "BASIC":
            payload = json.loads(payload)

            if type(payload) != dict or len(payload) == 0:
                return jsonify({"error": "Invalid JSON payload"}), 400

        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if type(payload) != dict or len(payload) == 0:
                return jsonify({"error": "Invalid JSON payload"}), 400
        else:
            return jsonify({"error": "the method could not be implemented"}), 400

        if ark_id.startswith("0x"):
            pid = dark_map.get_pid_by_hash(ark_id)
        else:
            pid = dark_map.get_pid_by_ark(ark_id)

        tx_set = dark_map.async_set_payload(pid.pid_hash, payload)
        tx_status, tx_recipt = dark_gw.transaction_was_executed(tx_set)

        result = {
            "pid": str(pid.ark),
            "pid_hash_index": Web3.toHex(pid.pid_hash),
            "action": "set_payload",
            "parameter": payload,
            "transaction_hash": tx_recipt,
            "tx_status": tx_status,
            "status": "queued",
        }

        return result, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
