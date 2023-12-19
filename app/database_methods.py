from flask_bcrypt import check_password_hash
from model import User
from instance_app import create_app

app = create_app()


def check_user_existence(email, password):

    with app.app_context():
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            return True
        else:
            return False


var1 = check_user_existence('usuario1@example.com', 'senha123')
var2 = check_user_existence('usuario1@example.com', 'senha124')

print(var1)

print(var2)
