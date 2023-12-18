from flask_bcrypt import check_password_hash
from configure_database import User


def check_user_existence(email, password):

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        return True
    else:
        return False


var1 = check_user_existence('emailusuario1@example.com', 'senha123')
var2 = check_user_existence('emailusuario1@example.com', 'senha124')

print(var1)

print(var2)
