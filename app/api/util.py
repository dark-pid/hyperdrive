#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   util.py
@Time    :   2022/05/28 10:36:42
@Author  :   Thiago Nóbrega 
@Contact :   thiagonobrega@gmail.com
'''
import requests
import json

import pandas as pd
from web3 import Web3

from util import setup
from util.libs import invoke_contract


def extratc_metada_dspace(item_metada):
    authors = []
    title = ''
    url = []
    ext_pid = []
    search_keys = []

    for metada in item_metada:
        if metada['key'] == 'dc.contributor.author':
            authors.append(metada['value'].upper().strip())
        if metada['key'] == 'dc.title':
            title = metada['value'].upper()
        if metada['key'] == 'dc.identifier.uri':
            url.append(metada['value'])
        if metada['key'] == 'dc.identifier.other':
            ext_pid.append(metada['value'].strip())
        if metada['key'] == 'dc.subject':
            search_keys.append(metada['value'].upper().strip())
    
    return title,authors,url,ext_pid,search_keys

def summary(author_db,item_db):
    saida = []
    for a in author_db.keys():
        ida = Web3.toHex(author_db[a][:16])
        # print(len(b))
        # ida = eid
        formated_id = ida[2:10]+'-'+ida[10:14]+'-'+ida[14:18]+'-'+ida[18:22]+'-'+ida[22:]
        linha = ['person', formated_id , str(ida) ,str(a)]
        saida.append(linha)
    
    for b in item_db.keys():
        idb = Web3.toHex(b[:16])
        # idb = eid
        # print(len(b))
        formated_id = idb[2:10]+'-'+idb[10:14]+'-'+idb[14:18]+'-'+idb[18:22]+'-'+idb[22:]
        linha = ['article',formated_id, str(idb) ,str(item_db[b])]
        saida.append(linha)
    
    df = pd.DataFrame(saida)
    df.columns = [ 'types' , 'dpi_id' , 'id_16bytes' , 'desc']
    df.id_16bytes = df.id_16bytes.astype(str)
    df.dpi_id = df.dpi_id.astype(str)
    return df

def import_itens_dspace(w3,account,chain_id,
                        dpid_service,sets_service,
                        headers,url_base,itens):
    author_db = {}
    item_db = {}

    for item in itens:
        #TODO:LER OS COMENTARIOS ABAIXO E VER AS OPORTUNIDADES
        try:
            item_id = item['id']
        except KeyError: #falta de padrao ex uepb utiliza id unb utiliza uuid 
            item_id = item['uuid'] #pode ser utilizado esse no lugar do nosso
        
        cmd_url = '/items/'+str(item_id)+'/metadata'
        url = url_base + cmd_url
        # print(url)
        r = requests.get(url, headers=headers)
        item_metada = json.loads(r.text)
        title,authors,urls,ext_pid,search_keys = extratc_metada_dspace(item_metada)

        #pid
        recipt_tx = invoke_contract(w3,account,chain_id, dpid_service , 'assingUUID')
        pid_id = recipt_tx['logs'][0]['topics'][1]

        for key in search_keys:
            recipt_tx = invoke_contract(w3,account,chain_id, sets_service , 'get_or_create_search_term' , key )
            # sk_id = recipt_tx['logs'][0]['topics'][1]
            recipt_tx = invoke_contract(w3,account,chain_id, dpid_service , 'addSearchTerm' , pid_id[:16], key )
        
        for epid in ext_pid:
            recipt_tx = invoke_contract(w3,account,chain_id, dpid_service , 'addExternalPid' ,pid_id[:16],'CDD',epid)
        
        for url in urls:
            recipt_tx = invoke_contract(w3,account,chain_id, dpid_service , 'add_externalLinks', pid_id[:16], url)

        recipt_tx = invoke_contract(w3,account,chain_id, dpid_service , 'set_payload', pid_id[:16], title)

        item_db[pid_id] = url

        for author in authors:
            try:
                author_db[author]
            except KeyError:
                recipt_tx = invoke_contract(w3,account,chain_id, dpid_service , 'assingUUID')
                author_id = recipt_tx['logs'][0]['topics'][1]
                recipt_tx = invoke_contract(w3,account,chain_id, dpid_service , 'set_payload', author_id[:16], author)
                author_db[author] = author_id
        
        return author_db, item_db