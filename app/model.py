from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Integer, String, Column, JSON, ForeignKey


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def configure(app):
    db.init_app(app)
    app.db = db


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
