import sys
import os
import requests

from flask import Flask , jsonify , render_template, send_file, abort
# from flask import render_template, request, Flask, g, send_from_directory, abort, jsonify

from web3 import Web3

import json
# import json
# import pandas as pd
# from web3 import Web3

from api.util import import_itens_dspace, summary
from util import setup
from util.libs import invoke_contract
from api.query_api import queries_blueprint

#
w3 = setup.load_blockchain_driver()
deployed_contracts = setup.load_deployed_smart_contracts(w3)
dpid_db = deployed_contracts['PidDB.sol']
epid_db = deployed_contracts['ExternalPidDB.sol']
sete_db = deployed_contracts['SearchTermDB.sol']

dpid_service = deployed_contracts['PIDService.sol']
epid_service = deployed_contracts['ExternalPIDService.sol']
sets_service = deployed_contracts['SearchTermService.sol']

chain_id,min_gas_price,pk = setup.get_exec_parameters()
account = w3.eth.account.privateKeyToAccount(pk)

# novo
template_dir = os.path.join(setup.PROJECT_ROOT,'templates')
app = Flask(__name__,template_folder=template_dir)

app.config['JSON_AS_ASCII'] = False #utf8
app.config['JSON_SORT_KEYS'] = False #prevent sorting json

app.register_blueprint(queries_blueprint)

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)