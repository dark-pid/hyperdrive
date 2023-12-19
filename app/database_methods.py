from flask_bcrypt import check_password_hash
from model import User
from instance_app import create_app

from flask import jsonify

from flask_jwt_extended import create_access_token, create_refresh_token

from util.responses import error_response_database

from datetime import timedelta

app = create_app()


class UserIsNone(Exception):
    pass


def authenticate(email, password):
    with app.app_context():

        user = User.query.filter_by(email=email).first()

        access_token = None
        refresh_token = None

        if user != None and check_password_hash(user.password, password):
            access_token = create_access_token(
                identity=user.id, expires_delta=timedelta(hours=6))

            refresh_token = create_refresh_token(identity=user.id)

            return access_token, refresh_token
        else:
            return access_token, refresh_token
