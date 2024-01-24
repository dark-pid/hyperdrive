from util.responses import success_response, error_response
import json
import os
import configparser
import asyncio

from flask import Blueprint, Flask, jsonify, render_template, send_file, abort, request, make_response
from web3 import Web3


from dark import DarkMap, DarkGateway
from util.validation import ValidationUtil
from util.config_manager import ConfigManager
from util.responses import success_response_create_pid, error_response

from config.BlockchainManager import BlockChainManager

# configurando classe das váriaveis externas
config_manager = ConfigManager()

core_api_blueprint = Blueprint("core_api", __name__, url_prefix="/core")

async_mode = config_manager.get_operation_mode()

if async_mode == "ASYNC":
    from util.asynchronus import add_url, add_external_pid, set_payload
else:
    from util.synchronous import add_url, add_external_pid, set_payload


##
# configuring blockchainManager
##

blockchain_manager = BlockChainManager()

dark_gw = blockchain_manager.dark_gw
dark_map = blockchain_manager.dark_map

###
# methods
###


def create_pid():
    try:
        action = "create_pid"
        error_code = 200
        pid_hash = dark_map.sync_request_pid_hash()
        pid_ark = dark_map.convert_pid_hash_to_ark(pid_hash)
        resp = success_response_create_pid(pid_ark, pid_hash, action)
    except Exception as e:
        message = f"block_chain_error : {str(e)}"
        status = "Unable to create a new PID"
        error_code = 500
        resp = error_response(action, message, error_code, status=status)
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

        return success_response(pid=dark_pid, op_mode="sync", status="executed", parameter=dark_id, key_action="get_pid", action="get_pid")
    except Exception as e:
        resp_code = 500
        status = f"Unable to recovery (' {str(dark_id)} ')"
        error_message = f"block_chain_error : {str(e)}"

        return error_response(pid=dark_pid, op_mode="sync", action="get_pid", parameter=dark_id, error_code=resp_code, error_message=error_message, status=status)


@core_api_blueprint.get("/get/<nam>/<shoulder>")
def get_pid_by_noid(nam, shoulder):
    dark_id = nam + str("/") + shoulder
    return get_pid(dark_id)


@core_api_blueprint.post("/set/<path:ark_id>")
def set_general(ark_id):
    pid = None

    if ark_id.startswith("0x"):
        pid = dark_map.get_pid_by_hash(ark_id)
    else:
        pid = dark_map.get_pid_by_ark(ark_id)

    if request.is_json:
        data = request.get_json()
        if len(data) == 0:
            return make_response(error_response(action="set", error_message="No parameter has been passed", error_code=400, pid=pid))

        if len(data) > 1:

            return make_response(error_response(action="set", error_message="Unable to execute multiple operations considering the Hyperdriver Synchronized Mode.", error_code=500, pid=pid))

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

    return make_response(error_response(action="set", error_message="Invalid or missing data in the request. Please check your input and try again.", error_code=400, pid=pid))


@core_api_blueprint.post("/add/<path:ark_id>")
def add_general(ark_id):
    pid = None

    if ark_id.startswith("0x"):
        pid = dark_map.get_pid_by_hash(ark_id)
    else:
        pid = dark_map.get_pid_by_ark(ark_id)

    if request.is_json:
        data = request.get_json()
        if len(data) == 0:
            return make_response(error_response(action="add", error_message="No parameter has been passed", error_code=400, pid=pid))

        if len(data) > 1:

            return make_response(error_response(action="add", error_message="Unable to execute multiple operations considering the Hyperdriver Synchronized Mode.", error_code=500, pid=pid))

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

    return make_response(error_response(action="add", error_message="Invalid or missing data in the request. Please check your input and try again.", error_code=400, pid=pid))

