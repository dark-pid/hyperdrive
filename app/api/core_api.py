import json
import os
import configparser
import asyncio

from flask import Blueprint, Flask, jsonify, render_template, send_file, abort, request
from web3 import Web3


from dark import DarkMap, DarkGateway
from util.validation import ValidationUtil
from util.config_manager import ConfigManager


# configurando classe das váriaveis externas
config_manager = ConfigManager()

core_api_blueprint = Blueprint("core_api", __name__, url_prefix="/core")

async_mode = config_manager.get_operation_mode()

if async_mode == "ASYNC":
    from util.asynchronus import add_url, add_external_pid, set_payload
else:
    from util.synchronous import add_url, add_external_pid, set_payload

## config responses class
from util.responses import success_response, error_response

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

        return success_response(dark_pid, op_mode="sync", status="executed", parameter=dark_id, action="get_pid")
    except Exception as e:

        resp_dict = {"status": "Unable to recovery (" + str(dark_id) + ")",
                     "block_chain_error": str(e)}
        resp_code = 500

        return error_response(dark_pid, op_mode="sync", action="get_pid", parameter=dark_id, error_code=resp_code, error_message=resp_dict)


@core_api_blueprint.get("/get/<nam>/<shoulder>")
def get_pid_by_noid(nam, shoulder):
    dark_id = nam + str("/") + shoulder
    return get_pid(dark_id)


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

            if async_mode == "ASYNC":
                return asyncio.run(add_url(ark_id, external_url))
            if async_mode == "SYNC":
                return add_url(ark_id, external_url)

        if "payload" in data:
            payload = data.get("payload")

            if async_mode == "ASYNC":
                return asyncio.run(set_payload(ark_id, payload))
            if async_mode == "SYNC":
                return set_payload(ark_id, payload)

    return (
        jsonify(
            {
                "error": "Invalid or missing data in the request. Please check your input and try again."
            }
        ),
        400,
    )

@core_api_blueprint.post("/add/<path:ark_id>")
def add_general(ark_id):
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

            if async_mode == "ASYNC":
                return asyncio.run(add_url(ark_id, external_url))
            if async_mode == "SYNC":
                return add_url(ark_id, external_url)

        if "external_pid" in data:
            pid = data.get("external_pid")

            if async_mode == "ASYNC":
                return asyncio.run(add_external_pid(ark_id, pid))
            if async_mode == "SYNC":
                return add_external_pid(ark_id, pid)

    return (
        jsonify(
            {
                "error": "Invalid or missing data in the request. Please check your input and try again."
            }
        ),
        400,
    )
