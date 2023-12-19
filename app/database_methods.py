from flask_bcrypt import check_password_hash
from model import User
from instance_app import create_app

from flask_jwt_extended import create_access_token, create_refresh_token

from datetime import timedelta

app = create_app()


def authenticate(email, password):
    with app.app_context():

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(
                identity=user.id, expires_delta=timedelta(hours=6))

            refresh_token = create_refresh_token(identity=user.id)

            return access_token
        else:
            return False
