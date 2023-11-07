import json
import os
import configparser

from flask import Blueprint, Flask, jsonify, render_template, send_file, abort, request
from web3 import Web3

from dark import DarkMap, DarkGateway
from util.validation import ValidationUtil
from util.responses import success_response, error_response
from util.config_manager import ConfigManager

# configurando classe das váriaveis externas
config_manager = ConfigManager()
async_mode = config_manager.get_operation_mode()

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
deployed_contracts_config.read(os.path.join(
    PROJECT_ROOT, "deployed_contracts.ini"))


# gw
dark_gw = DarkGateway(bc_config, deployed_contracts_config)

#
dark_map = DarkMap(dark_gw)

###
# methods
###


# Set the external variable -> config_manager.set_url_validation("BASIC")
def add_url(ark_id, external_url):
    try:
        VERIFICATION_METHOD = config_manager.get_url_validation()
    except:
        VERIFICATION_METHOD = None

    try:
        key_action = "external url"
        action = "add_url"
        pid = None

        if ark_id.startswith("0x"):
            pid = dark_map.get_pid_by_hash(ark_id)
        else:
            pid = dark_map.get_pid_by_ark(ark_id)

        if VERIFICATION_METHOD == "BASIC":
            if ValidationUtil.check_url(external_url) == False:
                return error_response(action, "Sorry, the URL provided is not valid. Make sure it is in the correct format. Please review and try again.", 400, op_mode=async_mode.lower(), key_action=key_action, pid=pid, parameter=external_url, parameter=external_url)
        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if len(external_url) == 0:
                return error_response(action, "Sorry, the URL cannot be empty. Please provide a valid URL and try again.", 400, op_mode=async_mode.lower(), key_action=key_action, pid=pid, parameter=external_url)
        else:
            return error_response(action, "the method could not be implemented", 501, op_mode=async_mode.lower(), key_action=key_action, pid=pid, parameter=external_url)

        dark_map.sync_set_url(pid.pid_hash, external_url)

        response = success_response(action, "executed", pid=pid, op_mode=async_mode.lower(
        ), parameter=external_url, key_action=key_action)

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Set the external variable -> config_manager.set_external_pid_validation("BASIC")
def add_external_pid(ark_id, external_pid):
    try:
        VERIFICATION_METHOD = config_manager.get_external_pid_validation()

    except:
        VERIFICATION_METHOD = None

    try:
        key_action = "external_pid"
        action = "add_external_pid"
        pid = None

        if ark_id.startswith("0x"):
            pid = dark_map.get_pid_by_hash(ark_id)
        else:
            pid = dark_map.get_pid_by_ark(ark_id)

        if VERIFICATION_METHOD == "BASIC":
            if external_pid.startswith("doi:/") == False:
                return error_response(action, "Sorry, the PID provided is not valid. Make sure it is correct and try again.", 400, op_mode=async_mode.lower(), key_action=key_action, pid=pid, parameter=external_pid)

        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if len(external_pid) == 0:
                return error_response(action, "Sorry, PID cannot be empty. Please provide a valid PID and try again.", 400, op_mode=async_mode.lower(), key_action=key_action, pid=pid, parameter=external_pid)
        else:
            return error_response(action, "queued", "the method could not, be implemented", 501, op_mode=async_mode.lower(), key_action=key_action, pid=pid, parameter=external_pid)

        valid_pid = external_pid.split(":/")[1]
        dark_map.sync_add_external_pid(pid.pid_hash, valid_pid)

        response = success_response(
            action, "executed", pid=pid, op_mode=async_mode.lower(), parameter=external_pid, key_action=key_action)

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Set the external variable -> config_manager.set_payload_validation("BASIC")
def set_payload(ark_id, payload):
    try:
        VERIFICATION_METHOD = config_manager.get_payload_validation()

    except:
        VERIFICATION_METHOD = None

    try:
        key_action = "payload"
        action = "set_payload"
        pid = None

        if ark_id.startswith("0x"):
            pid = dark_map.get_pid_by_hash(ark_id)
        else:
            pid = dark_map.get_pid_by_ark(ark_id)

        if VERIFICATION_METHOD == "BASIC":
            if type(payload) != dict:
                try:
                    payload = json.loads(payload)
                except Exception as e:
                    return error_response(action, "Sorry, the payload provided is not valid JSON. Make sure it is correct and try again", 400, op_mode=async_mode.lower(), key_action=key_action, pid=pid, parameter=payload)

        elif VERIFICATION_METHOD == "NONE" or VERIFICATION_METHOD == None:
            if type(payload) != dict or len(payload) == 0:
                return error_response(action, "Sorry, the provided payload cannot be empty. Please provide a valid payload and try again", 400, op_mode=async_mode.lower(), key_action=key_action, pid=pid, parameter=payload)
        else:
            return error_response(action, "the method could not be implemented", 501, op_mode=async_mode.lower(), key_action=key_action, pid=pid, parameter=payload)

        dark_map.sync_set_payload(pid.pid_hash, payload)

        response = success_response(
            action, "executed", pid=pid, op_mode=async_mode.lower(), parameter=payload, key_action=key_action)

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500
