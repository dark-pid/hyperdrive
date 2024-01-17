from flask import Blueprint, request, make_response

from util.responses import error_response, success_response_database, error_response_database

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

    api_auth_key = authenticate(user_email, user_password)

    if api_auth_key != None:

        response = success_response_database(
            action="authenticate", api_auth_key=api_auth_key)

        return response
    else:

        response = error_response_database(
            action="authenticate", error_code=400, error_message="invalid credentials")

        return response
