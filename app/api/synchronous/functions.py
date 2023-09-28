import json
import os
import configparser

from flask import Blueprint, Flask, jsonify, render_template, send_file, abort, request
from web3 import Web3

from dark import DarkMap, DarkGateway
from util.validation import ValidationUtil
from util.config_manager import ConfigManager

# configurando classe das váriaveis externas
config_manager = ConfigManager()

core_api_blueprint = Blueprint("core_api", __name__, url_prefix="/core")

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
def add_url(ark_id, external_url):
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
                return jsonify({"error": "Invalid URL"}), 400
        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if len(external_url) == 0:
                return jsonify({"error": "Invalid URL"}), 400
        else:
            return jsonify({"error": "the method could not be implemented"}), 400

        dark_map.sync_set_url(pid.pid_hash, external_url)

        return (
            jsonify(
                {
                    "pid": str(pid.ark),
                    "action": "external_url_add",
                    "parameter": external_url,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Set the external variable -> config_manager.set_external_pid_validation("BASIC")
def add_external_pid(ark_id, external_pid):
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
                return jsonify({"error": "Invalid Pid"}), 400

        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if len(external_pid) == 0:
                return jsonify({"error": "Invalid Pid"}), 400
        else:
            return jsonify({"error": "the method could not be implemented"}), 400

        valid_pid = external_pid.split(":/")[1]
        dark_map.sync_add_external_pid(pid.pid_hash, valid_pid)

        return (
            jsonify(
                {
                    "pid": str(pid.ark),
                    "action": "external_pid_add",
                    "parameter": valid_pid,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Set the external variable -> config_manager.set_payload_validation("BASIC")
def set_payload(ark_id, payload):
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

        dark_map.sync_set_payload(pid.pid_hash, payload)

        return (
            jsonify(
                {
                    "pid": str(pid.ark),
                    "action": "payload_add",
                    "parameter": payload,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400
