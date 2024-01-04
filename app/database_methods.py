from flask_bcrypt import check_password_hash
from model import User
from instance_app import create_app

from flask_jwt_extended import create_access_token

from datetime import timedelta

from util.config_manager import ConfigManager

config_manager = ConfigManager()

app = create_app()


class UserIsNone(Exception):
    pass


def authenticate(email, password):
    with app.app_context():

        try:
            AUTH_TOKEN_EXPIRATION_TIME = int(
                config_manager.get_auth_token_expiration_time())
        except (ValueError, TypeError):
            AUTH_TOKEN_EXPIRATION_TIME = 6

        user = User.query.filter_by(email=email).first()

        access_token = None

        if user != None and check_password_hash(user.password, password):
            access_token = create_access_token(
                identity=user.id, expires_delta=timedelta(hours=AUTH_TOKEN_EXPIRATION_TIME))

            return access_token
        else:
            return access_token
