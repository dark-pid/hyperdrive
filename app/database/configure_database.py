import os
from variables_database import ConfigVariables
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

config_variables = ConfigVariables()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

db = SQLAlchemy(app)


# classes utilizadas para criar as tabelas
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    naan = db.Column(db.String(50))
    organization = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    wallet_private_key = db.Column(db.String(256))

    def __init__(self, naan, organization, email, wallet_private_key):
        self.naan = naan
        self.organization = organization
        self.email = email
        self.wallet_private_key = wallet_private_key


with app.app_context():
    db.create_all()
