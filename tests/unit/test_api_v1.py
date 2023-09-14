import json
import pytest
import logging
import time
import datetime
 
from .core import HyperDriveAPI , check_basic_parameter


def test_create(hyperdrive_api) -> None:
    response  = hyperdrive_api.new_v1()
    # dict ok
    try:
        if type(response) == dict:
            assert response['ark'] != None
        else:
            raise Exception(response)
        
    except Exception as e:
        logging.error('Failed to create PID : '+ str(e))
        raise Exception(str(e))

def test_add_url(hyperdrive_api) -> None:
    # dict ok
    now_unix_timestamp = datetime.datetime.timestamp(datetime.datetime.now())*1000

    valid_ext_url = 'http://dark.io/'+str(now_unix_timestamp)
    
    post_data = {
        'external_url' : valid_ext_url
    }

    excepted_response = {
        "action": "add_external_url",
        "parameter": valid_ext_url,
    }

    try:
        response = hyperdrive_api.new_v1()
        if type(response) == dict:
            pid_ark = response['ark']
        else:
            raise Exception(response)
        
        response = hyperdrive_api.set(pid_ark, post_data)
        if type(response) == dict:
            check_basic_parameter(response=response, expected_pid=pid_ark , excepted_response=excepted_response)
        else:
            raise Exception(response)
        
    except Exception as e:
        logging.error('Failed to set external_url to PID : '+ str(e))
        raise Exception(str(e))

def test_add_external_pid(hyperdrive_api) -> None:
    # dict ok
    now_unix_timestamp = datetime.datetime.timestamp(datetime.datetime.now())*1000

    valid_ext_url = 'http://dark.io/'+str(now_unix_timestamp)
    
    post_data_set_url = {
        'external_url' : valid_ext_url
    }

    excepted_response_set_url = {
        "action": "add_external_url",
        "parameter": valid_ext_url,
    }

    post_data_add_pid = {
        'external_pid' : 'doi:/116.dark.' + str(now_unix_timestamp),
    }

    excepted_response_add_pid = {
        "action": "add_external_pid",
        "parameter": 'doi:/116.dark.' + str(now_unix_timestamp),
    }

    try:
        response = hyperdrive_api.new_v1()
        if type(response) == dict:
            pid_ark = response['ark']
        else:
            raise Exception(response)
        
        response = hyperdrive_api.set(pid_ark, post_data_set_url)
        if type(response) == dict:
            check_basic_parameter(response=response, expected_pid=pid_ark , excepted_response=excepted_response_set_url)
        else:
            raise Exception(response)
        
        response = hyperdrive_api.set(pid_ark, post_data_add_pid)
        if type(response) == dict:
            check_basic_parameter(response=response, expected_pid=pid_ark , excepted_response=excepted_response_add_pid)
            # assert response['pid'] == pid_ark
            # # assert response['action'] == excepted_response_add_pid['action']
            # assert response['parameter'] == excepted_response_add_pid['parameter'].split(':/')[1]
        else:
            raise Exception(response)
        
    except Exception as e:
        logging.error('Failed to set add external_pid to PID : '+ str(e))
        raise Exception(str(e))

def test_set_payload(hyperdrive_api) -> None:
    # dict ok
    now_unix_timestamp = datetime.datetime.timestamp(datetime.datetime.now())*1000

    valid_ext_url = 'http://dark.io/'+str(now_unix_timestamp)
    
    post_data_set_url = {
        'external_url' : valid_ext_url
    }

    excepted_response_set_url = {
        "action": "add_external_url",
        "parameter": valid_ext_url,
    }

    post_data_set_payload = {
        'payload' : '{' + f'name : name_{str(now_unix_timestamp)}, time : {str(now_unix_timestamp)}' + '}',
    }

    excepted_response_set_payload = {
        "action": "set_payload",
        'parameter' : '{' + f'name : name_{str(now_unix_timestamp)}, time : {str(now_unix_timestamp)}' + '}',
    }


    try:
        response = hyperdrive_api.new_v1()
        if type(response) == dict:
            pid_ark = response['ark']
        else:
            raise Exception(response)
        
        response = hyperdrive_api.set(pid_ark, post_data_set_url)
        if type(response) == dict:
            check_basic_parameter(response=response, expected_pid=pid_ark , excepted_response=excepted_response_set_url)
        else:
            raise Exception(response)
        
        response = hyperdrive_api.set(pid_ark, post_data_set_payload)

        if type(response) == dict:
            # check_basic_parameter(response=response, expected_pid=pid_ark , excepted_response=excepted_response_set_payload)
            pass
        else:
            raise Exception(response)
        
    except Exception as e:
        logging.error('Failed to set payload to PID : '+ str(e))
        raise Exception(str(e))


def test_set_over_draft(hyperdrive_api) -> None:
    # dict ok
    now_unix_timestamp = datetime.datetime.timestamp(datetime.datetime.now())*1000

    post_data_set_payload = {
        'payload' : '{' + f'name : name_{str(now_unix_timestamp)}, time : {str(now_unix_timestamp)}' + '}',
    }


    try:
        response = hyperdrive_api.new_v1()
        if type(response) == dict:
            pid_ark = response['ark']
        else:
            raise Exception(response)
        
        response = hyperdrive_api.set(pid_ark, post_data_set_payload)

        if type(response) == dict:
            raise Exception("operation executed over DRAFT PID")
        else:
            # o erro vem da blockchain, nao tratado
            #TODO : MELHORAR
            pass
        
    except Exception as e:
        logging.error('Failed to set payload to PID : '+ str(e))
        raise Exception(str(e))
