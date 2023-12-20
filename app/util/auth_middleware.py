from flask import request, jsonify
from util.config_manager import ConfigManager

config_manager = ConfigManager()

USE_AUTH = config_manager.get_hyperdrive_auth()


def authentication_middleware():
    if USE_AUTH == "True":

        token = request.headers.get('Authorization')
        print(token)

        non_auth_routes = ['/user/login', '/core/get']

        if request.path in non_auth_routes:
            return

        if not token:
            return jsonify({'message': 'Missing authentication token'}), 401
