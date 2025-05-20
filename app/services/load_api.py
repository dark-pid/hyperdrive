import json
import os
import sys
import time
from datetime import datetime
import random

import configparser
from hexbytes import HexBytes

from flask import Blueprint, jsonify , redirect , request
from ipfspy.ipfshttpapi import IPFSApi

from dark import DarkMap, DarkGateway

from util.validation import is_valid_url
from util.bc import url_exists
from util.ipfs import add_to_ipfs
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


def check_account(data):
    dnam_pk = data.get('dnam_pk').strip()
    account = Account.from_key(dnam_pk)
    dnam_wallet = account.address
    dark_gw, dark_map = get_bc_gateway(dnam_pk)
    return account, dnam_wallet, dark_gw, dark_map

@load_api.route('/load', methods=['post'])
def load_data():
    data = request.json
    items = data.get('items', [])
    erros = []
    dnam_pk = ''
    load_time = 0
    r_time = 0

    try:
        account, dnam_wallet, dark_gw, dark_map = check_account(data)
        # dnam_pk = data.get('dnam_pk').strip()
        # account = Account.from_key(dnam_pk)
        # dnam_wallet = account.address
        # dark_gw, dark_map = get_bc_gateway(dnam_pk)
    except AttributeError:
        # sem a chave
        erros.append("No private key identified")
    except Exception:
        erros.append("Invalid private key.")
    except ValueError:
        erros.append("Invalid private key")

    if len(erros) > 0:
        resp = {'erros' :  erros , 'params' : str(data)}
        return jsonify(resp), 500


    processados = []
    nao_processados = []
    start_time = time.time()
    for item in items:
        oai_id = item.get('oai_id')
        url = item.get('url')

        item_data = {'oai_id' : oai_id , 'requested_url' : url}


        if oai_id and ( is_valid_url(url) and url_exists(url,dark_map) == False ):
            try: 
                ark_hash_obj = shared_utils.get_pid(dnam_wallet,dark_map)
                ark_hash_hex_val = ark_hash_obj.hex()

                item_data['ark_hash'] = ark_hash_hex_val
            
                tx = dark_map.async_set_url(ark_hash_obj,url)
                txr = tx.hex()
                item_data['tx_recipt'] = txr
                processados.append(item_data)
            except Exception as e: 
                item_data['error'] = 'blockchain error'
                item_data['error_desc'] = str(e)
                nao_processados.append(item_data)
        else:
            if not is_valid_url(url):
                item_data['error'] = 'invalid url'
            else:
                item_data['error'] = 'URL already exists and set to other ark'
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

@load_api.route('/update', methods=['post'])
def update_metadata():
    data = request.json
    items = data.get('items', [])
    erros = []
    update_time = 0

    try:
        account, dnam_wallet, dark_gw, dark_map = check_account(data)
    except AttributeError:
        # sem a chave
        erros.append("No private key identified")
    except Exception:
        erros.append("Invalid private key")
    except ValueError:
        erros.append("Invalid private key")
    
    # caso tenha parametros invalidos
    if len(erros) > 0:
        resp = {'erros' :  erros , 'params' : str(data)}
        return jsonify(resp), 500
    
    processados = []
    nao_processados = []
    start_time = time.time()
    for item in items:

        # recuperar o pid
        parametros_validos = True
        try:
            dark_id = item.get('dark_id')
            if not dark_id:
                item['error'] = 'No valid dark_id provided'
                nao_processados.append(item)
                parametros_validos = False
        except ValueError as e:
            erros.append('No dark_id provided')
            item['error'] = 'No valid dark_id provided'
            nao_processados.append(item)
            parametros_validos = False
        try:
            update_url = item.get('url')
            item['update_url'] = update_url
            del item['url']

            if not update_url:
                item['error'] = 'No url provided'
                nao_processados.append(item)
                parametros_validos = False
            if not is_valid_url(update_url):
                item['error'] = 'invalid URL'
                nao_processados.append(item)
                parametros_validos = False

            # chek whether the url already exists
            if url_exists(update_url,dark_map):
                item['error'] = 'URL already exists and set to other ark'
                nao_processados.append(item)
                parametros_validos = False

        except ValueError as e:
            item['error'] = 'No url provided'
            nao_processados.append(item)
            parametros_validos = False
        
        if parametros_validos:
            try:
                dark_pid = dark_map.get_pid_by_ark(dark_id)
            except Exception as e:
                item['error'] = 'dark_id not found'
                nao_processados.append(item)
                break
                # resp = jsonify({'status' : 'Unable to recovery (' + str(dark_id) + ')', 'block_chain_error' : str(e)},)
                # resp_code = 500 # colocar um erro especifico?

            item['update_url'] = update_url

            if is_valid_url(update_url):
                try:
                    ark_hash_obj = dark_pid.pid_hash
                    ark_hash_hex_val = ark_hash_obj.hex()
                    item['ark_hash'] = ark_hash_hex_val
                    tx = dark_map.async_set_url(ark_hash_obj,update_url)
                    txr = tx.hex()
                    item['tx_recipt'] = txr
                    item['previous_url'] = dark_pid.external_url
                    processados.append(item)
                except Exception as e: 
                    item['error'] = 'bockchain error'
                    item['error_desc'] = str(e)
                    nao_processados.append(item)
            else:
                item['error'] = 'invalid url'
                nao_processados.append(item)
                # print("aqui")

        
    end_time = time.time()
    update_time = end_time - start_time

    response = {
            "wallet_addr": account.address ,
            "action": 'update',
            "update_time" : update_time,
            "timestamp": datetime.now().timestamp(),
            "updated_pids": processados
    }

    if len(nao_processados) != 0:
        response["not_updated_pids"] = nao_processados
        

    # 
    os.makedirs('logs', exist_ok=True)
    timestamp = int(time.time())
    random_digits = random.randint(000, 999)
    filename = f"logs/update_{time.strftime('%Y-%m-%d')}_{dnam_wallet[2:]}_{timestamp}_{random_digits}.json"
    with open(filename, 'w') as f:
        json.dump(response, f, indent=4)

    return jsonify(response), 200

@load_api.route('/set/metadata', methods=['post'])
def add_metadata():
    """
    Recebe uma lista de metadados, faz upload de cada um no IPFS e associa ao PID na blockchain.
    Espera JSON com:
    {
        "dnam_pk": "<private_key>",
        "items": [
            {
                "dark_id": "<ark>",
                "metadata": "<conteúdo do metadata>"
            },
            ...
        ]
    }
    """
    data = request.json
    items = data.get('items', [])
    erros = []
    upload_time = 0

    try:
        account, dnam_wallet, dark_gw, dark_map = check_account(data)
    except AttributeError:
        erros.append("No private key identified")
    except Exception:
        erros.append("Invalid private key")
    except ValueError:
        erros.append("Invalid private key")

    if len(erros) > 0:
        resp = {'erros': erros, 'params': str(data)}
        return jsonify(resp), 500

    processados = []
    nao_processados = []
    start_time = time.time()
    api = IPFSApi()

    for item in items:
        dark_id = item.get('dark_id')
        metadata = item.get('metadata')
        item_result = {'dark_id': dark_id}

        if not dark_id or not metadata:
            item_result['error'] = 'dark_id or metadata missing'
            nao_processados.append(item_result)
            continue

        try:
            pid_obj = dark_map.get_pid_by_ark(dark_id)
            resp, obj = add_to_ipfs(metadata, api)
            ps = dark_map.get_payload_schema_by_name('DC', 'none')
            pid_hash = pid_obj.pid_hash
            payload_schema_id = HexBytes(ps.get_id())
            payload_ipfs_addr = obj[1]['Hash']
            bctx = dark_map.async_set_payload(pid_hash, payload_schema_id, payload_ipfs_addr)
            item_result['ipfs_hash'] = payload_ipfs_addr
            item_result['status'] = 'uploaded'
            item_result['dark_tx'] = str(bctx)
            processados.append(item_result)
        except Exception as e:
            item_result['error'] = str(e)
            nao_processados.append(item_result)

    end_time = time.time()
    upload_time = end_time - start_time

    response = {
        "wallet_addr": account.address,
        "action": 'upload_metadata',
        "upload_time": upload_time,
        "timestamp": datetime.now().timestamp(),
        "uploaded": processados
    }
    if nao_processados:
        response["not_uploaded"] = nao_processados

    os.makedirs('logs', exist_ok=True)
    timestamp = int(time.time())
    random_digits = random.randint(0, 999)
    filename = f"logs/upload_metadata_{time.strftime('%Y-%m-%d')}_{dnam_wallet[2:]}_{timestamp}_{random_digits}.json"
    with open(filename, 'w') as f:
        json.dump(response, f, indent=4)

    return jsonify(response), 200