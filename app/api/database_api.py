from configure_database import User, db
from flask import request, jsonify, Blueprint
from flask_bcrypt import Bcrypt
from instance_app import app


bcrypt = Bcrypt(app)

database_api_blueprint = Blueprint(
    "database_api", __name__, url_prefix="/data")


def add_user_to_database(email, password, wallet_private_key, ):
    new_user = User(email=email, password=password,
                    wallet_private_key=wallet_private_key)
    db.session.add(new_user)
    db.session.commit()


@database_api_blueprint.post('/add_user')
def add_user():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    wallet_private_key = data.get('wallet_private_key')

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    add_user_to_database(email, pw_hash, wallet_private_key)

    return jsonify({'message': 'User added successfully'})
