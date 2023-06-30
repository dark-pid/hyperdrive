#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   libs.py
@Time    :   2022/04/21 11:03:55
@Author  :   Thiago Nóbrega 
@Contact :   thiagonobrega@gmail.com
'''

import os
import time
import logging

import secrets

import solcx
from web3.exceptions import TransactionNotFound

def compile_all(contracts,output_values=["abi",'bin',"bin-runtime"],solc_version="0.8.13"):
    """
    """

    solcx.set_solc_version('0.8.13')
    compiled =  solcx.compile_files(contracts,
                                    output_values=output_values,
                                    solc_version=solc_version,
                                    optimize=True
                                    )

    return compiled


def compile_contract(contract_name,contracts,output_values=["abi",'bin',"bin-runtime","evm"],solc_version="0.8.13"):
# def compile_contract(contract_name,contracts,output_values=["abi",'bin',"evm"],solc_version="0.8.13"):
    """
    """
    compiled =  compile_all(contracts,
                            output_values=output_values,
                            solc_version=solc_version
                            )

    for k in compiled.keys():
        if k.endswith(str(os.sep + contract_name)):
            return compiled[k]
    
    raise Exception('This shouldnt happend')

def get_contract(contract_name,contracts_dicts):
    contract_name = contract_name.split('.')[0]
    for k in contracts_dicts.keys():
        if k.endswith(':'+contract_name):
            return contracts_dicts[k]
    
    raise Exception('This shouldnt happend')

def populate_file_list(dir,files):
    """
        Private method to populate a list with full path of the smartcontrats
    """
    lista = []
    for i in files:
        lista.append( os.path.join(dir,i) )
    return lista

def deploy_contract_besu(account,w3,contract_interface,chain_id,gas=500000):
   
   sc = w3.eth.contract( abi=contract_interface['abi'],
                           bytecode=contract_interface['bin']
                        )

   est_gas = sc.constructor().estimateGas()
   tx_const = sc.constructor().buildTransaction(get_tx_params(w3,est_gas,account,chain_id=chain_id))
   signed_tx = account.signTransaction(tx_const)
   tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

   tx_receipt = None
   iter_count = 1

   tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

   return tx_receipt['contractAddress']


def deploy_contract_besu_original(account,w3, contract_interface,gas=500000):
   
   sc = w3.eth.contract( abi=contract_interface['abi'],
                           bytecode=contract_interface['bin']
                        )

   #   'gas': 6612388,   
   # 'gasPrice': w3.eth.gasPrice
   tx_params = {'from': account.address,
               'nonce': w3.eth.getTransactionCount(account.address),
               'gas': gas,
               # 'gasPrice': 1100, #//ETH per unit of gas
               # BESU_MIN_GAS_PRICE=1337
               # 'gasLimit': '0x24A22' #//max number of gas units the tx is allowed to use
               }

   tx_const = sc.constructor().buildTransaction(tx_params)
   signed_tx = account.signTransaction(tx_const)
   tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

   tx_receipt = None
   iter_count = 1

   # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

   while tx_receipt == None or iter_count < 30:
      logging.debug("Trying.. " + str(iter_count) + "/30 ...")
      time.sleep(2)
      try:
         tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
         iter_count += 1
         return tx_receipt['contractAddress']
      except TransactionNotFound:
         iter_count += 1

   # tx_receipt['status'] 0x1 funcionou 0x0 nao foi feito o deploy
   if iter_count >= 29:
      logging.debug('Transacao lascou')
      
   return tx_receipt['contractAddress']

###
### gen privatekey
###

def gen_pk():
    """
        method to generate private keys to the block
    """
    priv = secrets.token_hex(32)
    return "0x" + priv



###
### Invoke the contract methods
###

def get_tx_params(w3,gas,account,chain_id=1337,min_gas_price='100'):
    # nonce = w3.eth.getTransactionCount(acount.address)
    nonce = w3.eth.getTransactionCount(w3.toChecksumAddress(account.address))
    tx_params = {'from': account.address,
                # 'to': contractAddress,
                'nonce': nonce,
                'gas': gas * 2,
                'gasPrice': w3.toWei(min_gas_price, 'gwei'), # defaul min gas price to besu (nao funciona w3.eth.gas_price)
                'chainId': chain_id
    }
    return tx_params


def invoke_contract(w3,account,chain_id,
                    smart_contract_method,*args):

    est_gas = smart_contract_method(*args).estimateGas()
    tx_params = get_tx_params(w3,est_gas,account,chain_id=chain_id)
    tx = smart_contract_method(args).buildTransaction(tx_params)
    signed_tx = account.signTransaction(tx)
    # send the transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

def invoke_contract(w3,account,chain_id,
            smart_contract,method,*args):
    """
        invoke_contract(w3,account,61, st_service , 'set_db' ,(contract_addr) )
    """

    #get the gas needed
    est_gas = smart_contract.get_function_by_name(method)(*args).estimateGas()
    #gen the tc header
    tx_params = get_tx_params(w3,est_gas,account,chain_id=chain_id)
    #build the transaction
    tx = smart_contract.get_function_by_name(method)(*args).buildTransaction(tx_params)
    #sign the transatiopn
    signed_tx = account.signTransaction(tx)
    # send the transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

def invoke_contract_experimental(w3,account,chain_id,
            smart_contract,method,*args):
    """
        invoke_contract(w3,account,61, st_service , 'set_db' ,(contract_addr) )
    """

    #get the gas needed
    est_gas = smart_contract.get_function_by_name(method)(*args).estimateGas()
    #gen the tc header
    tx_params = get_tx_params(w3,est_gas,account,chain_id=chain_id)
    #build the transaction
    tx = smart_contract.get_function_by_name(method)(*args).buildTransaction(tx_params)
    #sign the transatiopn
    signed_tx = account.signTransaction(tx)
    # send the transaction
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt , est_gas