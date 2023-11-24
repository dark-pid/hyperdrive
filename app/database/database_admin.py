from .configure_database import User, db

# atualizar a função com chamada igual api e realizar teste pelo curl e postman


def add_user_to_database(naan, organization, email, wallet_private_key, ):
    new_user = User(naan=naan, organization=organization,
                    email=email, wallet_private_key=wallet_private_key)
    db.session.add(new_user)
    db.session.commit()
