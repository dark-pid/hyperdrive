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


def create_pid():
    try:
        error_code = 200
        pid_hash = dark_map.sync_request_pid_hash()
        pid_ark = dark_map.convert_pid_hash_to_ark(pid_hash)
        resp = jsonify({"ark": pid_ark, "hash": Web3.toHex(pid_hash)})
    except Exception as e:
        error_code = 500
        resp = jsonify(
            {"status": "Unable to create a new PID", "block_chain_error": str(e)},
        )
    return resp, error_code


###
###

# curl.exe -H 'Content-Type: application/json'  -X POST http://127.0.0.1:8080/core/xpto -d "{\"pid\":\"xpto---\"}"
# curl -X POST http://10.220.0.15:8080/core/xpto -H 'Content-Type: application/json' -d '{"pid":"my_login"}'
# -d @example_post.json


@core_api_blueprint.route("/new", methods=("GET", "POST"))
def get_new():
    alternative_pid = None
    alternative_url = None
    resp, error_code = create_pid()

    # return erros imediatly
    if error_code != 200:
        return resp, error_code

    # check if there are arguments
    # TODO: COULD BE ASYNC METHODS
    # FIXME: multiplas acoes executadas tem que ter cuidado que elas podem dar erros espescificos e tem que ser melhor gerenciadas
    if request.method == "GET":
        alternative_pid = request.args.get(
            config_manager.EXTERNAL_PID_PARAMETER
        )  # , default=0, type=int)
        alternative_url = request.args.get(
            config_manager.EXTERNAL_URL_PARAMETER
        )  # , default=0, type=int)
    elif request.method == "POST":
        if request.is_json:
            content_type = request.headers.get("Content-Type")
            data = request.json
            alternative_pid = data.get(config_manager.EXTERNAL_PID_PARAMETER)
            alternative_url = data.get(config_manager.EXTERNAL_URL_PARAMETER)

    if alternative_pid != None:
        # TODO: implementar metodo
        print("ADICIONAR EXTERNAL PID (" + str(alternative_pid) + ") AO PID")
    if alternative_url != None:
        # TODO: implementar metodo
        print("ADICIONAR EXTERNAL URL (" + str(alternative_url) + ")AO PID")

    # novamente como reportar o erro aqui?
    return resp, error_code


@core_api_blueprint.get("/get/<dark_id>")
def get_pid(dark_id):
    resp_code = 200
    try:
        dark_pid = None
        if dark_id.startswith("0x"):
            dark_pid = dark_map.get_pid_by_hash(dark_id)
            # dark_object = dpid_db.caller.get(dark_id)
        else:
            dark_pid = dark_map.get_pid_by_ark(dark_id)

        resp_dict = dark_pid.to_dict()

        if len(dark_pid.externa_pid_list) == 0:
            del resp_dict["externa_pid_list"]

        resp = jsonify(resp_dict)
    except ValueError as e:
        resp = jsonify(
            {
                "status": "Unable to recovery (" + str(dark_id) + ")",
                "block_chain_error": str(e),
            },
        )
        resp_code = 500

    return resp, resp_code


@core_api_blueprint.get("/get/<nam>/<shoulder>")
def get_pid_by_noid(nam, shoulder):
    dark_id = nam + str("/") + shoulder
    return get_pid(dark_id)


# Set the external variable config_manager.set_url_validation("BASIC")
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


# Set the external variable config_manager.set_external_pid_validation("BASIC")
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


# Set the external variable config_manager.set_payload_validation("BASIC")
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


@core_api_blueprint.post("/set/<path:ark_id>")
def set_general(ark_id):
    if request.is_json:
        data = request.get_json()
        if len(data) == 0:
            return jsonify({"error": "No parameter has been passed"}), 405

        if len(data) > 1:
            return (
                jsonify(
                    {
                        "error": "Unable to execute multiple operations considering the Hyperdriver Synchronized Mode."
                    }
                ),
                400,
            )

        if "external_url" in data:
            external_url = data.get("external_url")
            return add_url(ark_id, external_url)

        if "external_pid" in data:
            pid = data.get("external_pid")
            return add_external_pid(ark_id, pid)

        if "payload" in data:
            payload = data
            return set_payload(ark_id, payload)

    return jsonify({"error": "Invalid or missing data in the request. Please check your input and try again."}), 400
