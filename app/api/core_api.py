import json
import os
import configparser

from flask import Blueprint, Flask, jsonify, render_template, send_file, abort, request
from web3 import Web3

from dark import DarkMap, DarkGateway

from util.validation import ValidationUtil
###
# varaivel de ambiente
###
# TODO: CRIAR UMA CLASS/config PARA ISSO
EXTERNAL_PID_PARAMETER = 'external_pid'
EXTERNAL_URL_PARAMETER = 'external_url'
os.environ['HYPERDRIVE_EXTERNAL_PID_VALIDATION'] = "BASIC"

core_api_blueprint = Blueprint('core_api', __name__, url_prefix='/core')

##
# configuring dARK GW
##

bc_config = configparser.ConfigParser()
deployed_contracts_config = configparser.ConfigParser()

# bc configuration
PROJECT_ROOT = './'
bc_config.read(os.path.join(PROJECT_ROOT, 'config.ini'))
# deployed contracts config
deployed_contracts_config.read(os.path.join(
    PROJECT_ROOT, 'deployed_contracts.ini'))


# gw
dark_gw = DarkGateway(bc_config, deployed_contracts_config)

#
dark_map = DarkMap(dark_gw)

###
# methods
###


def create_pid():
    try:
        error_code = 200
        pid_hash = dark_map.sync_request_pid_hash()
        pid_ark = dark_map.convert_pid_hash_to_ark(pid_hash)
        resp = jsonify({'ark': pid_ark,
                        'hash': Web3.toHex(pid_hash)
                        })
    except Exception as e:
        error_code = 500
        resp = jsonify({'status': 'Unable to create a new PID',
                        'block_chain_error': str(e)},)
    return resp, error_code

###
###

# curl.exe -H 'Content-Type: application/json'  -X POST http://127.0.0.1:8080/core/xpto -d "{\"pid\":\"xpto---\"}"
# curl -X POST http://10.220.0.15:8080/core/xpto -H 'Content-Type: application/json' -d '{"pid":"my_login"}'
# -d @example_post.json


@core_api_blueprint.route('/new', methods=('GET', 'POST'))
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
    if request.method == 'GET':
        alternative_pid = request.args.get(
            EXTERNAL_PID_PARAMETER)  # , default=0, type=int)
        alternative_url = request.args.get(
            EXTERNAL_URL_PARAMETER)  # , default=0, type=int)
    elif request.method == 'POST':
        if request.is_json:
            content_type = request.headers.get('Content-Type')
            data = request.json
            alternative_pid = data.get(EXTERNAL_PID_PARAMETER)
            alternative_url = data.get(EXTERNAL_PID_PARAMETER)

    if alternative_pid != None:
        # TODO: implementar metodo
        print("ADICIONAR EXTERNAL PID ("+str(alternative_pid)+") AO PID")
    if alternative_url != None:
        # TODO: implementar metodo
        print("ADICIONAR EXTERNAL URL ("+str(alternative_url)+")AO PID")

    # novamente como reportar o erro aqui?
    return resp, error_code


@core_api_blueprint.get('/get/<dark_id>')
def get_pid(dark_id):
    resp_code = 200
    try:
        dark_pid = None
        if dark_id.startswith('0x'):
            dark_pid = dark_map.get_pid_by_hash(dark_id)
            # dark_object = dpid_db.caller.get(dark_id)
        else:
            dark_pid = dark_map.get_pid_by_ark(dark_id)

        resp_dict = dark_pid.to_dict()

        if len(dark_pid.externa_pid_list) == 0:
            del resp_dict['externa_pid_list']

        resp = jsonify(resp_dict)
    except ValueError as e:
        resp = jsonify({'status': 'Unable to recovery (' +
                       str(dark_id) + ')', 'block_chain_error': str(e)},)
        resp_code = 500

    return resp, resp_code


@core_api_blueprint.get('/get/<nam>/<shoulder>')
def get_pid_by_noid(nam, shoulder):
    dark_id = nam + str('/') + shoulder
    return get_pid(dark_id)


@core_api_blueprint.put("/set/set-external-pid/<path:ark_id>")
def update_external_pid(ark_id):

    try:
        VERIFICATION_METHOD = os.environ.get("HYPERDRIVE_PID_VALIDATION")

        if VERIFICATION_METHOD == None:
            raise ValueError("Hyperdrive Pid validation is None")
        if VERIFICATION_METHOD == "":
            raise ValueError("Hyperdrive Pid validation is empty")

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    try:
        pid = None

        if ark_id.startswith("0x"):
            pid = dark_map.get_pid_by_hash(ark_id)
        else:
            pid = dark_map.get_pid_by_ark(ark_id)

        external_pid = request.args.get("external_pid")

        if VERIFICATION_METHOD == "BASIC":

            if ValidationUtil.check_pid(external_pid) == False:
                return jsonify({"error": "Invalid Pid"}), 400
            else:
                valid_pid = external_pid[8:int(len(external_pid))]

        elif VERIFICATION_METHOD == "NONE":
            if len(external_pid) == 0:
                return jsonify({"error": "Invalid Pid"}), 400
        else:
            return jsonify({"error": "the method could not be implemented"}), 400

        dark_map.sync_add_external_pid(pid.pid_hash, valid_pid)

        return (
            jsonify({
                "pid": str(pid.ark),
                "action": "external_pid_add",
                "parameter": valid_pid,
            }), 200
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 400
