from flask import request, jsonify
from util.config_manager import ConfigManager
from flask_jwt_extended import jwt_required

config_manager = ConfigManager()


def authentication_middleware():

    USE_AUTH = config_manager.get_hyperdrive_auth()

    if USE_AUTH == "TRUE":

        token = request.headers.get('Authorization')

        non_auth_routes = ['/','/user/login', '/core/get','/static/swagger.json']
        
        if request.path in non_auth_routes:
            return
        if request.endpoint == 'swagger' or request.path.startswith('/swagger'):
            return 
        try:
            jwt_required()(lambda: None)()

        except:

            return jsonify({'message': 'Invalid token'}), 401

        if not token:
            return jsonify({'message': 'Missing authentication token'}), 401
