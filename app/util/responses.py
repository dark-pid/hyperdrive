from flask import jsonify
from web3 import Web3


def success_response(pid, op_mode, action, parameter, status, tx_receipt=None, tx_status=None):
    if op_mode == "sync":
        status = "executed"
    else:
        status = "queued"

    response_data = {
        "pid": str(pid.ark),
        "pid_hash_index": Web3.toHex(pid.pid_hash),
        "action": action,
        "parameter": {"pid": str(pid.ark), action: parameter},
        "status": status,
        "hyperdrive_op_mode": op_mode.lower(),
    }

    if tx_receipt != None:
        response_data["transaction_hash"] = tx_receipt

    if tx_status != None:
        response_data["tx_status"] = tx_status

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


def success_response_create_pid(pid, pid_hash):
    response_data = {
        "pid": str(pid),
        "pid_hash_index": Web3.toHex(pid_hash),
        "action": "create_pid",
        "status": "executed"
    }

    return jsonify(response_data)
