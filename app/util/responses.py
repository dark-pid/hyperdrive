from flask import jsonify
from web3 import Web3


def success_response(action, status, tx_receipt=None, tx_status=None, pid=None, key_action=None, parameter=None, op_mode=None):
    if op_mode == "sync":
        status = "executed"
    else:
        status = "queued"

    response_data = {
        "action": action,
        "status": status
    }

    if tx_receipt != None:
        response_data["transaction_hash"] = tx_receipt

    if tx_status != None:
        response_data["tx_status"] = tx_status

    if key_action != None:
        response_data["parameter"] = {
            "pid": str(pid.ark), key_action: parameter}

    if op_mode != None:
        response_data["hyperdrive_op_mode"] = op_mode.lower()

    if pid != None:
        response_data.update(
            {"pid": str(pid.ark), "pid_hash_index": Web3.toHex(pid.pid_hash)})

    return jsonify(response_data), 200


def error_response(action, error_message, error_code, op_mode=None, status=None, key_action=None, pid=None, parameter=None):
    error_response = {
        "error": {
            "message": error_message,
            "error_code": error_code,
            "action": action,
            "status": "rejected" if status == None else status
        }
    }

    if key_action != None:
        error_response["parameter"] = {
            "pid": str(pid.ark), key_action: parameter}

    if op_mode != None:
        error_response["hyperdrive_op_mode"] = op_mode.lower()

    if pid != None:
        error_response["error"].update(
            {"pid": str(pid.ark), "pid_hash_index": Web3.toHex(pid.pid_hash)})

    return jsonify(error_response), error_code


def success_response_create_pid(pid, pid_hash, action):
    response_data = {
        "pid": str(pid),
        "pid_hash_index": Web3.toHex(pid_hash),
        "action": action,
        "status": "executed"
    }

    return jsonify(response_data)


def success_response_database(action, api_auth_key, refresh_auth_key):
    response_data = {
        "op_mode": "sync",
        "action": action,
        "status": "Executed",
        "api_auth_key": api_auth_key,
        "refresh_auth_key": refresh_auth_key
    }

    return jsonify(response_data), 200


def error_response_database(action, error_message, error_code):
    error_response = {
        "error": {
            "op_mode": "sync",
            "action": action,
            "status": "Rejected",
            "error_code": error_code,
            "error_message": error_message
        }
    }

    return jsonify(error_response), error_code
