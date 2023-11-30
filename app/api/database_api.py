from configure_database import User, db
from flask import request, jsonify, Blueprint


database_api_blueprint = Blueprint(
    "database_api", __name__, url_prefix="/data")


def add_user_to_database(naan, organization, email, wallet_private_key, ):
    new_user = User(naan=naan, organization=organization,
                    email=email, wallet_private_key=wallet_private_key)
    db.session.add(new_user)
    db.session.commit()


@database_api_blueprint.post('/add_user')
def add_user():
    data = request.get_json()

    naan = data.get('naan')
    organization = data.get('organization')
    email = data.get('email')
    wallet_private_key = data.get('wallet_private_key')

    add_user_to_database(naan, organization, email, wallet_private_key)

    return jsonify({'message': 'User added successfully'})
