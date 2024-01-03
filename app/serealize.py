from flask_marshmallow import Marshmallow
from model import User, Transaction

ma = Marshmallow()


def configure(app):
    ma.init_app(app)


class UserSchema(ma.Schema):
    class Meta:
        model = User


class TransactionSchema(ma.Schema):
    class Meta:
        model = Transaction
