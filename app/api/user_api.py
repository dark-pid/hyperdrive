from flask import Blueprint, request, make_response, current_app

from util.responses import error_response, success_response_database, error_response_database
from config.BlockchainManager import BlockChainManager

from database_methods import authenticate


user_api_blueprint = Blueprint("user_api", __name__, url_prefix="/user")


@user_api_blueprint.post("/login")
def user_login():
    api_auth_key = None

    data = request.get_json()

    if len(data) == 0:
        return make_response(error_response(action="authenticate", error_message="No parameter has been passed", error_code=400))

    if len(data) < 2:
        return make_response(error_response(action="authenticate", error_message="Unspecified email or password", error_code=400))

    user_email = data.get("email")
    user_password = data.get("password")

    api_auth_key, refresh_auth_key = authenticate(user_email, user_password)


    ##
    # configuring blockchainManager
    ##

    # if you have the userPk put it here, in the parameter pass
    blockchain_manager = BlockChainManager()

    current_app.blockchain_manager = blockchain_manager

    if api_auth_key != None:

        response = success_response_database(
            action="athenticate", api_auth_key=api_auth_key, refresh_auth_key=refresh_auth_key)

        return response
    else:

        response = error_response_database(
            action="athenticate", error_code=400, error_message="invalid credentials")

        return response
