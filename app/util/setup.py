#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   setup.py
@Time    :   2022/05/13 10:20:06
@Author  :   Thiago Nóbrega 
@Contact :   thiagonobrega@gmail.com
'''
import os
import configparser
import logging
import ast

from web3 import Web3, IPCProvider
from web3.middleware import geth_poa_middleware

# from eth_tester import PyEVMBackend
from web3.providers.eth_tester import EthereumTesterProvider

from .libs import compile_all,get_contract,deploy_contract_besu,populate_file_list,get_tx_params,invoke_contract

#TODO: Definir melhor
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

config_file = os.path.join(PROJECT_ROOT,'config.ini')
deployed_contracts_config = os.path.join(PROJECT_ROOT,'deployed_contracts.ini')


def load_blockchain_driver():
    """
        Load the blockchain driver.

        The drive is used to connect the application to the blockchain.
        The configuration is defined in config.ini file.
    """
    #debug
    logging.info(config_file)
    # print(config_file)

    config = configparser.ConfigParser()
    config.read(config_file)
    blockchain_net = config['base']['blockchain_net']

    if blockchain_net == 'EthereumTesterPyEvm':
        raise(Exception("Not Suported"))
        # return Web3(EthereumTesterProvider(PyEVMBackend()))
    elif 'dpi-' in blockchain_net:
        blockchain_config = config[blockchain_net]
        blockchain_config['url']
        w3 = Web3(Web3.HTTPProvider(blockchain_config['url']))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        return w3
    else:
        raise RuntimeError('This shouldnt happend :: Not implemented')

######
###### compile
######

def compile():
    logging.info("> Compiling Contracts")
    config = configparser.ConfigParser()
    config.read(config_file)

    DAPP_ROOT = os.path.join(PROJECT_ROOT, 'Dapp')
    LIB_PATH = os.path.join(DAPP_ROOT, config['smartcontracts']['lib_dir'])
    UTIL_PATH = os.path.join(DAPP_ROOT, config['smartcontracts']['util_dir'])
    DB_PATH = os.path.join(DAPP_ROOT, config['smartcontracts']['db_dir'])
    SERVICE_PATH = os.path.join(DAPP_ROOT, config['smartcontracts']['service_dir'])

    libs_path = populate_file_list(LIB_PATH,config['smartcontracts']['lib_files'].split())
    utils_path = populate_file_list(UTIL_PATH,config['smartcontracts']['utils_files'].split())
    dbs_paths = populate_file_list(DB_PATH,config['smartcontracts']['dbs_files'].split())
    services_path = populate_file_list(SERVICE_PATH,config['smartcontracts']['service_files'].split())
    
    compiled_contracts = compile_all(services_path + dbs_paths + utils_path + libs_path)
    logging.info("")
    return compiled_contracts

######
###### deploy
######

def deploy(w3,account,contract_name,compiled_contracts,chain_id):
    contract_interface = get_contract(contract_name,compiled_contracts)
    addr = deploy_contract_besu(account,w3,contract_interface,chain_id)
    # contracts_dicts[contract_name] = 
    return [addr,contract_interface]

def deploy_contracts(w3,compiled_contracts):
    config = configparser.ConfigParser()
    config.read(config_file)

    blockchain_net = config['base']['blockchain_net']
    logging.info("> Deployin Contracts to " + blockchain_net)

    if blockchain_net == 'EthereumTesterPyEvm':
        #transferindo fundo para uma conta nova
        pk = config['EthereumTesterPyEvm']['account_priv_key']
        chain_id = int(config['EthereumTesterPyEvm']['chain_id'])
        min_gas_price = int(config['EthereumTesterPyEvm']['min_gas_price'])
        # account = w3.eth.account.create(pk)
        account = w3.eth.account.privateKeyToAccount(pk)


        tx = { "from": w3.eth.accounts[0], 
                'to': account.address, 
                "value": Web3.toWei(10000, "ether"), 
                'gas': 21000 
        }
        w3.eth.send_transaction(tx)
        
    elif 'dpi-' in blockchain_net:
        pk = config[blockchain_net]['account_priv_key']
        account = w3.eth.account.privateKeyToAccount(pk)
        chain_id = int(config[blockchain_net]['chain_id'])
        #TODO: passar como parametro para os metodos de deploy
        min_gas_price = int(config[blockchain_net]['min_gas_price'])
    else:
        raise RuntimeError('This shouldnt happend :: Not implemented')
    
    acc_balance = str(Web3.fromWei(w3.eth.get_balance(account.address),'ether'))
    logging.info("    using account : " + account.address )
    logging.info("    account initial balance : " + acc_balance )

    # lista = config['smartcontracts']['lib_files'].split() +\
    lista = config['smartcontracts']['utils_files'].split() +\
            config['smartcontracts']['dbs_files'].split() +\
            config['smartcontracts']['service_files'].split()

    deployed_contract_dict = {}
    
    for contract_name in lista:
        if contract_name not in ['Entities.sol' , 'NoidProvider.sol']:
            logging.info("    deploying : " + str(contract_name) + "..." )
            deployed_contract_dict[str(contract_name)] = deploy(
                                                        w3,account,
                                                        contract_name,
                                                        compiled_contracts,
                                                        chain_id)
            
    logging.info("    deployed : " + str(len(lista)) + " contracts" )
    acc_balance = str(Web3.fromWei(w3.eth.get_balance(account.address),'ether'))
    logging.info("    account initial balance : " + acc_balance )
    logging.info("")
    return deployed_contract_dict

######
###### configuration
######

def configure_env(w3,deployed_contract_dict):
    config = configparser.ConfigParser()
    config.read(config_file)

    configured_contracts = {}
    
    if config['base']['blockchain_net'] == 'EthereumTesterPyEvm':
        blockchain_conf = config['EthereumTesterPyEvm']
    elif 'dpi-' in config['base']['blockchain_net']:
        blockchain_conf = config[config['base']['blockchain_net']]
    else:
        raise RuntimeError('This shouldnt happend :: Not implemented')
    
    chain_id = int(blockchain_conf['chain_id'])
    min_gas_price = int(blockchain_conf['min_gas_price'])
    pk = blockchain_conf['account_priv_key']

    ############## setup
    logging.info("> Configure env...")
    account = w3.eth.account.privateKeyToAccount(pk)
    acc_balance = str(Web3.fromWei(w3.eth.get_balance(account.address),'ether'))
    logging.info("    using account : " + account.address )
    logging.info("    account initial balance : " + acc_balance )

    ### Authorities Service
    logging.info("    Configuring AuthoritiesService:")
    auth_db_addr = deployed_contract_dict['AuthoritiesDB.sol'][0]
    contract_addr = deployed_contract_dict['AuthoritiesService.sol'][0]
    contract_interface = deployed_contract_dict['AuthoritiesService.sol'][1]
    auth_service = w3.eth.contract(address=contract_addr, abi=contract_interface["abi"])
    invoke_contract(w3,account,chain_id, auth_service , 'set_db' ,(auth_db_addr) )
    logging.info("        - db configured")
    logging.info("        - AuthoritiesService configured")
    configured_contracts['AuthoritiesService'] = auth_service
    

    ### pid db
    logging.info("    Configuring D-pi PiD Database:")
    # uuid_provider_addr = deployed_contract_dict['UUIDProvider.sol'][0]
    contract_addr = deployed_contract_dict['PidDB.sol'][0]
    contract_interface = deployed_contract_dict['PidDB.sol'][1]
    pid_db = w3.eth.contract(address=contract_addr, abi=contract_interface["abi"])
    # invoke_contract(w3,account,chain_id, pid_db , 'set_uuid_provider' ,(uuid_provider_addr) )
    # logging.info("        - uuid provider configured")
    configured_contracts['PidDB'] = pid_db
    
    ### Search TermService
    logging.info("    Configuring SearchTermService:")
    st_db_addr = deployed_contract_dict['SearchTermDB.sol'][0]
    contract_addr = deployed_contract_dict['SearchTermService.sol'][0]
    contract_interface = deployed_contract_dict['SearchTermService.sol'][1]
    st_service = w3.eth.contract(address=contract_addr, abi=contract_interface["abi"])
    invoke_contract(w3,account,chain_id, st_service , 'set_db' ,(st_db_addr) )
    logging.info("        - db configured")
    configured_contracts['SearchTermService'] = st_service

    #### ExternalPID Service
    logging.info("    Configuring ExternalPIDService:")
    epid_db_addr = deployed_contract_dict['ExternalPidDB.sol'][0]
    contract_addr = deployed_contract_dict['ExternalPIDService.sol'][0]
    contract_interface = deployed_contract_dict['ExternalPIDService.sol'][1]
    epid_service = w3.eth.contract(address=contract_addr, abi=contract_interface["abi"])
    invoke_contract(w3,account,chain_id, epid_service , 'set_db' ,(epid_db_addr) )
    logging.info("        - db configured")
    configured_contracts['ExternalPIDService'] = epid_service
    

    # D-pi PID Service
    logging.info("    Configuring D-pi PIDService:")
    pid_db_addr = deployed_contract_dict['PidDB.sol'][0]
    contract_addr = deployed_contract_dict['PIDService.sol'][0]
    contract_interface = deployed_contract_dict['PIDService.sol'][1]
    pid_service = w3.eth.contract(address=contract_addr, abi=contract_interface["abi"])
    invoke_contract(w3,account,chain_id, pid_service , 'set_db' ,(pid_db_addr) )
    logging.info("        - db configured")
    invoke_contract(w3,account,chain_id, pid_service , 'set_externalpid_service' ,(epid_service.address) )
    logging.info("        - ExternalPIDService configured")
    invoke_contract(w3,account,chain_id, pid_service , 'set_searchterm_service' ,(st_service.address) )
    logging.info("        - SearchTermService configured")
    invoke_contract(w3,account,chain_id, pid_service , 'set_auth_service' ,(auth_service.address) )
    logging.info("        - authoritiesService configured")
    configured_contracts['PIDService'] = pid_service

    ### all set
    acc_balance = str(Web3.fromWei(w3.eth.get_balance(account.address),'ether'))
    logging.info("    account final balance : " + acc_balance )
    logging.info("All set... Services configured.")
    logging.info("")
    return configured_contracts

###
###
### 
def get_exec_parameters():
    
    config = configparser.ConfigParser()
    config.read(config_file)

    bc_net = config['base']['blockchain_net'] 
    blockchain_conf = config[bc_net]

    chain_id = int(blockchain_conf['chain_id'])
    min_gas_price = int(blockchain_conf['min_gas_price'])
    pk = blockchain_conf['account_priv_key']
    return chain_id,min_gas_price,pk

def save_smart_contract(deployed_contracts):
    """
        Save the deployed smart contracts
        - inputs the deploed_contracts dict

        - It is essential to configure the contract prior to its usage
        - Please only use this method to save configured contracts
    """
    config = configparser.ConfigParser()

    for k in deployed_contracts.keys():
        addr = deployed_contracts[k][0] # addr
        v2 = deployed_contracts[k][1].copy()
        del v2['bin']
        del v2['bin-runtime']
        config[k] = { 'addr': addr , 'abi' : v2}

    with open(deployed_contracts_config, 'w') as configfile:
        config.write(configfile)

def load_deployed_smart_contracts(w3):
    """
        Save the deployed smart contracts
        - Ity is essential notice that it is important to configure the smart contract
    """
    

    c2 = configparser.ConfigParser()
    c2.read(deployed_contracts_config)

    contracts_dict = {}
    for k in list(c2.keys()):
        if k != 'DEFAULT':
            addr = c2[k]['addr']
            c_abi = ast.literal_eval(c2[k]['abi'])['abi']
            contracts_dict[k] = w3.eth.contract(address=addr, abi=c_abi)
    
    return contracts_dict



def setup_from_scratch():
    w3 = load_blockchain_driver()
    compiled_contracts = compile()
    deployed_contract_dict = deploy_contracts(w3,compiled_contracts)
    configured_contracts = configure_env(w3,deployed_contract_dict)



if __name__ == '__main__':

    import logging
    logging.basicConfig(level=logging.INFO)

    w3 = load_blockchain_driver()
    compiled_contracts = compile()
    deployed_contract_dict = deploy_contracts(w3,compiled_contracts)
    configured_contracts = configure_env(w3,deployed_contract_dict)

    #
    chain_id,min_gas_price,pk = get_exec_parameters()
    account = w3.eth.account.privateKeyToAccount(pk)


    pidService = configured_contracts['PIDService']
    r = invoke_contract(w3,account,chain_id, pidService , 'assingUUID' )
    pidDB = configured_contracts['PidDB']

    ###
    pid_db = compiled_contracts['/mnt/d/Dados/OneDrive/IBICT/workspace/D-pi/Dapp/db/PidDB.sol:PidDB']
    addr = configured_contracts['PidDB'].address
    
    pidDB = w3.eth.contract(address=addr, abi=pid_db["abi"])
    ###
    
    pidDB.get_function_by_name('count').call()
    
    account.address
    pidDB.caller.count()
    Web3.toHex(pidDB.caller.get_by_index(0))
    pid_id = r['logs'][0]['topics'][1][:16]

    pid_object = pidDB.caller.get(pid_id)

    #olhar no Entities libs as posicoes 0 ~ 9
    print('uuid='+Web3.toHex(pid_object[0]))
    print("owner="+pid_object[8])
    