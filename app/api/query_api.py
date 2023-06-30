import sys
import os
import requests

from flask import Blueprint, Flask , jsonify , render_template, send_file, abort
# from flask import render_template, request, Flask, g, send_from_directory, abort, jsonify

from web3 import Web3

import json

from api.util import import_itens_dspace, summary
from util import setup
from util.libs import invoke_contract


queries_blueprint = Blueprint('queries_api', __name__)

w3 = setup.load_blockchain_driver()
deployed_contracts = setup.load_deployed_smart_contracts(w3)
dpid_db = deployed_contracts['PidDB.sol']
epid_db = deployed_contracts['ExternalPidDB.sol']
sete_db = deployed_contracts['SearchTermDB.sol']


@queries_blueprint.get('/search/<term>')
def search(term):
    try:
        search_term = sete_db.caller.get(term) # o correto e mover isso para o servico
        print(search_term)
        search_term_id = Web3.toHex(search_term[0])
        print(search_term_id)
        raw_pids = sete_db.caller.get_pids(search_term_id)
        pids = []
        formated_pids = []
        for pid in raw_pids:
            pid = Web3.toHex(pid)
            pids.append(pid)
            # fpid = str(pid[2:8])+'-'+str(pid[8:12])+'-'+str(pid[12:16])+'-'+str(pid[16:20])+'-'+str(pid[20:])
            # formated_pids.append(fpid)

        resp = jsonify({'pids': pids})

    except ValueError as e:
        resp = jsonify({'status' : 'Unable to recovery (' + str(term) + ')', 'block_chain_error' : str(e)},)
    
    return resp, 200

@queries_blueprint.get('/get/<dark_id>')
def get_pid(dark_id):
    try:
        dark_object = None
        if dark_id.startswith('0x'):
            dark_object = dpid_db.caller.get(dark_id)
        else:
            dark_object = dpid_db.caller.get_by_noid(dark_id)
        
        external_pids = []
        for ext_pid in dark_object[3]:
            # print(ext_pid)
            # print(type(ext_pid))
            # epid = epid_db.caller.get(ext_pid)
            ext_pid = Web3.toHex(ext_pid)
            # epid = epid_db.functions.get(ext_pid).call()
            get_func = epid_db.get_function_by_signature('get(bytes32)')
            epid = get_func(ext_pid).call()
            
            
            # print(ext_pid)

            pid_object = {'id': ext_pid, 
                            'schema:' : epid[3] , 'value' : epid[2], 
                            'owner:' : epid[-1]
                        }
            external_pids.append(pid_object)
        
        external_links = []
        for ext_link in dark_object[5]:
            external_links.append(ext_link)

        payload = dark_object[-2]
        owner = dark_object[-1]
        # uuid = dpi_obect[0]
        noid = dark_object[1]
        
        resp_dict = {
                        'noid' : noid,
                        'external_pids' : external_pids,
                        'payload': payload,
                        'external_links' : external_links,
                        'owner' : owner,
                    }
        
        if len(external_links) == 0:
            del resp_dict['external_links']
        
        if len(external_pids) == 0:
            del resp_dict['external_pids']

        resp = jsonify(resp_dict)
    except ValueError as e:
        resp = jsonify({'status' : 'Unable to recovery (' + str(dark_id) + ')', 'block_chain_error' : str(e)},)
    # web3.exceptions.ValidationError:
    
    return resp, 200

@queries_blueprint.get('/get/<nam>/<shoulder>')
def get_pid_by_noid(nam,shoulder):
    dark_id = nam + str('/') + shoulder
    return get_pid(dark_id)