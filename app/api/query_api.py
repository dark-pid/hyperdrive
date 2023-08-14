import sys
import os
import configparser

from flask import Blueprint, Flask , jsonify , render_template, send_file, abort
# from flask import render_template, request, Flask, g, send_from_directory, abort, jsonify

from web3 import Web3

# import json
# from api.util import import_itens_dspace, summary
# from util import setup
# from util.libs import invoke_contract
from dark.gateway import DarkGateway

queries_blueprint = Blueprint('queries_api', __name__)

##
## configuring dARK GW
##

bc_config = configparser.ConfigParser()
deployed_contracts_config = configparser.ConfigParser()

# bc configuration
PROJECT_ROOT='./'
bc_config.read(os.path.join(PROJECT_ROOT,'config.ini'))
# deployed contracts config
deployed_contracts_config.read(os.path.join(PROJECT_ROOT,'deployed_contracts.ini'))

# gw
dark_gw = DarkGateway(bc_config,deployed_contracts_config)

# w3 = setup.load_blockchain_driver()
# deployed_contracts = setup.load_deployed_smart_contracts(w3)



dpid_db = dark_gw.deployed_contracts_dict['PidDB.sol']
epid_db = dark_gw.deployed_contracts_dict['ExternalPidDB.sol']


@queries_blueprint.get('/search/<term>')
def search(term):
    try:
        raise Exception("Deprecated")
        # deprecated
        # search_term = sete_db.caller.get(term) # o correto e mover isso para o servico
        # print(search_term)
        # search_term_id = Web3.toHex(search_term[0])
        # print(search_term_id)
        # raw_pids = sete_db.caller.get_pids(search_term_id)
        # pids = []
        # formated_pids = []
        # for pid in raw_pids:
        #     pid = Web3.toHex(pid)
        #     pids.append(pid)
        #     # fpid = str(pid[2:8])+'-'+str(pid[8:12])+'-'+str(pid[12:16])+'-'+str(pid[16:20])+'-'+str(pid[20:])
        #     # formated_pids.append(fpid)

        # resp = jsonify({'pids': pids})

    except ValueError as e:
        resp = jsonify({'status' : 'Unable to recovery (' + str(term) + ')', 'block_chain_error' : str(e)},)
    
    return resp, 200
