from flask import jsonify
from web3 import Web3


def success_response(pid, op_mode, action, parameter,status, tx_receipt=None, tx_status=None):
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


def error_response(pid, op_mode, action, parameter, error_message, error_code):
    error_response = {
        "error": {
            "pid": str(pid.ark),
            "pid_hash_index": Web3.toHex(pid.pid_hash),
            "message": error_message,
            "error_code": error_code,
            "action": action,
            "parameter": {"pid": str(pid.ark), "external_url": parameter},
            "status": "rejected",
            "hyperdrive_op_mode": op_mode.lower(),
        }
    }
    return jsonify(error_response), error_code

def success_response_new(pid, pid_hash):
    response_data = {
        "pid": str(pid),
        "pid_hash_index": Web3.toHex(pid_hash),
        "action": "create_pid",
        "status": "executed"
    }

    return jsonify(response_data)

def error_response_new(error_code, e):
    response_data = {
        "action": "create_pid",
        "status": "Unable to create a new PID",
        "block_chain_error": str(e),
        "error_code": error_code,
    }

    return jsonify(response_data)
