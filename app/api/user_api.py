from flask import Blueprint, request, make_response, jsonify

from util.responses import success_response, error_response

from database_methods import authenticate


user_api_blueprint = Blueprint("user_api", __name__, url_prefix="/user")


@user_api_blueprint.post("/login")
def user_login():

    api_auth_key = None

    data = request.get_json()

    if len(data) == 0:
        return make_response(error_response(action="authenticate", error_message="No parameter has been passed", error_code=400))

    user_email = data.get("email")
    user_password = data.get("password")

    api_auth_key = authenticate(user_email, user_password)

    return jsonify({
        "api_auth_key": api_auth_key
    })
