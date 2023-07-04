import json
import os
import configparser

from flask import Blueprint, Flask , jsonify , render_template, send_file, abort, request
from web3 import Web3

from dark import DarkMap, DarkGateway
###
### varaivel de ambiente
###
#TODO: CRIAR UMA CLASS/config PARA ISSO
EXTERNAL_PID_PARAMETER = 'external_pid'
EXTERNAL_URL_PARAMETER = 'external_url'


core_api_blueprint = Blueprint('core_api', __name__, url_prefix='/core')

##
## configuring dARK GW
##

bc_config = configparser.ConfigParser()

# bc configuration
bc_config.read(os.path.join('./','config.ini'))
blockchain_net = bc_config['base']['blockchain_net']
blockchain_config = bc_config[blockchain_net]
# gw
dark_gw = DarkGateway(blockchain_net,blockchain_config)
# deployed contracts config
deployed_contracts_config = configparser.ConfigParser()
deployed_contracts_config.read(os.path.join('./','deployed_contracts.ini'))
# load deployed contracts
dark_gw.load_deployed_smart_contracts(deployed_contracts_config)
#
dark_map = DarkMap(dark_gw)

###
### methods 
###

def create_pid():
    try:
        error_code = 200
        pid_hash = dark_map.request_pid_hash()
        pid_ark = dark_map.convert_pid_hash_to_ark(pid_hash)
        resp = jsonify({'ark': pid_ark,
                        'hash': Web3.toHex(pid_hash)
                        })
    except Exception as e:
        error_code = 500 
        resp = jsonify({'status' : 'Unable to create a new PID',
                        'block_chain_error' : str(e)},)
    return resp,error_code

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
        alternative_pid = request.args.get(EXTERNAL_PID_PARAMETER)#, default=0, type=int)
        alternative_url = request.args.get(EXTERNAL_URL_PARAMETER)#, default=0, type=int)
    elif request.method == 'POST':
        if request.is_json:
            content_type = request.headers.get('Content-Type')
            data = request.json
            alternative_pid = data.get(EXTERNAL_PID_PARAMETER)
            alternative_url = data.get(EXTERNAL_PID_PARAMETER)
        
    
    if alternative_pid != None:
        #TODO: implementar metodo
        print("ADICIONAR EXTERNAL PID ("+str(alternative_pid)+") AO PID")
    if alternative_url != None:
        #TODO: implementar metodo
        print("ADICIONAR EXTERNAL URL ("+str(alternative_url)+")AO PID")
    
    #novamente como reportar o erro aqui?
    return resp, error_code

