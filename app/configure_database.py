import os
import pandas as pd
from flask_bcrypt import Bcrypt
from database.variables_database import ConfigVariables
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Integer, String, Column, JSON, ForeignKey
from instance_app import app


config_variables = ConfigVariables()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

db.init_app(app)
bcrypt = Bcrypt(app)


csv_file_path = 'app/database/users.csv'
df = pd.read_csv(csv_file_path)


class User(db.Model):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(250))
    wallet_private_key = Column(String(250))

    transactions = relationship("Transaction", back_populates="user_account")


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tx_hash = Column(String(255))
    parameters = Column(JSON)
    status = Column(String(50))
    parent_tx = Column(JSON)

    user_account_id = Column(Integer, ForeignKey('user_account.id'))
    user_account = relationship("User", back_populates="transactions")


with app.app_context():
    db.create_all()


for index, row in df.iterrows():
    hashed_password = bcrypt.hashpw(
        row['password'].encode('utf-8'), bcrypt.gensalt())

    new_user = User(
        email=row['email'],
        password=hashed_password.decode('utf-8'),
        wallet_private_key=row['wallet_private_key']
    )
    db.session.add(new_user)

db.session.commit()
