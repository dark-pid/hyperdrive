import os
from database.variables_database import ConfigVariables
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Column, JSON
from api_server import app


config_variables = ConfigVariables()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

db.init_app(app)


# classes utilizadas para criar as tabelas, polir todas se necessário
# falta testar no banco de dados
class User(db.Model):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    naan = Column(String(50))
    organization = Column(db.String(50))
    email = Column(String(120), unique=True, nullable=False)
    wallet_private_key = Column(String(256))


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tx_hash = Column(String(255))
    parameters = Column(JSON)
    status = Column(String(50))
    parent_tx = Column(String(255))


class Wallet(db.Model):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    private_key = Column(String(255))


class NoidProvider(db.Model):
    __tablename__ = 'noid_provider'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nam = Column(String(255))
    dnam = Column(String(255))
    sec_nam = Column(String(255))
    sep_token = Column(String(1))
    noid_len = Column(Integer)

    def gen(self):
        # Implemente a lógica específica do método gen aqui se necessário
        generated_value = f"{self.nam}_{self.dnam}_{self.sec_nam}"
        return generated_value


class DecentralizedNameMappingAuthority(db.Model):
    __tablename__ = 'decentralized_name_mapping_authority'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ror_id = Column(String(255))
    shoulder_prefix = Column(String(255))
    noid_provider_addr = Column(String(255))
    responsable = Column(String(255))
    section_authorities = Column(String(255))


class SectionMappingAuthority(db.Model):
    __tablename__ = 'section_mapping_authority'

    id = Column(Integer, primary_key=True, autoincrement=True)
    shoulder_prefix = Column(String(255))
    dNMA_id = Column(String(255))
    noid_provider_addr = Column(String(255))
    responsable = Column(String(255))


with app.app_context():
    db.create_all()
