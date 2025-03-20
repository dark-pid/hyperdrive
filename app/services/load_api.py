import json
import os
import sys
import time
import random

import configparser

from flask import Blueprint, jsonify , redirect , request

from dark import DarkMap, DarkGateway

from util.validation import is_valid_url
from eth_account import Account

import shared_utils 


##
## VARIABLES
##

PROJECT_ROOT='..'+os.sep+'config'+os.sep
load_api = Blueprint('load_api', __name__)#, url_prefix='/load')

##
## configuring dARK GW
##




def get_bc_gateway(account_pk):
    bc_config = configparser.ConfigParser()
    deployed_contracts_config = configparser.ConfigParser()
    bc_config.read(os.path.join(PROJECT_ROOT,'config.ini'))
    deployed_contracts_config.read(os.path.join(PROJECT_ROOT,'deployed_contracts.ini'))

    
    dark_gw = DarkGateway(bc_config,deployed_contracts_config,account_private_key=account_pk)
    dark_map = DarkMap(dark_gw)
    return dark_gw, dark_map


@load_api.route('/load', methods=['post'])
def check_json():
    data = request.json
    items = data.get('items', [])
    erros = []
    dnam_pk = ''
    load_time = 0
    r_time = 0

    try:
        dnam_pk = data.get('dnam_pk').strip()
        account = Account.from_key(dnam_pk)
        dnam_wallet = account.address
        dark_gw, dark_map = get_bc_gateway(dnam_pk)
    except AttributeError:
        # sem a chave
        erros.append("No private key identified")
    except Exception:
        erros.append("Invalid private key")
    except ValueError:
        erros.append("Invalid private key")



    processados = []
    nao_processados = []
    start_time = time.time()
    for item in items:
        oai_id = item.get('oai_id')
        url = item.get('url')

        item_data = {'oai_id' : oai_id , 'requested_url' : url}

        if oai_id and is_valid_url(url):
            try: 
                ark_hash_obj = shared_utils.get_pid(dnam_wallet,dark_map)
                ark_hash_hex_val = ark_hash_obj.hex()

                item_data['ark_hash'] = ark_hash_hex_val
            
                tx = dark_map.async_set_url(ark_hash_obj,url)
                txr = tx.hex()
                item_data['tx_recipt'] = txr
                processados.append(item_data)
            except Exception as e: 
                item_data['error'] = 'bockchain error'
                item_data['error_desc'] = str(e)
                nao_processados.append(item_data)
        else:
            item_data['error'] = 'invalid url'
            nao_processados.append(item_data)
    
    end_time = time.time()
    load_time = end_time - start_time


    if len(erros) > 0:
        resp = {'erros' :  erros , 'params' : str(data)}
        return jsonify(resp), 500
    
    # recuperando os arks
    start_time = time.time()
    saida = []
    for park in processados:
        ark_hash = park['ark_hash']
        ark = dark_map.get_pid_by_hash(ark_hash).to_dict()
        park['ark'] = ark['ark']
        park['ark_url'] = ark['external_url']
        
        saida.append(park)
    end_time = time.time()
    r_time = end_time - start_time
        
        

    if len(nao_processados) == 0:
        response = {
            "wallet_addr": account.address ,
            "ingested_pids": saida,
            "load_time" : load_time,
            "verify_time" : r_time
        }
    else:
        response = {
            "wallet_addr": account.address ,
            "ingested_pids": saida,
            "not_ingested_pids": nao_processados,
            "load_time" : load_time,
            "verify_time" : r_time
        }

    # 
    os.makedirs('logs', exist_ok=True)
    timestamp = int(time.time())
    random_digits = random.randint(000, 999)
    filename = f"logs/{time.strftime('%Y-%m-%d')}_{dnam_wallet[2:]}_{timestamp}_{random_digits}.json"
    with open(filename, 'w') as f:
        json.dump(response, f, indent=4)

    return jsonify(response), 200


