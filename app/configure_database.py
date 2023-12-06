import os
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


class User(db.Model):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    naan = Column(String(50))
    organization = Column(db.String(50))
    email = Column(String(120), unique=True, nullable=False)
    wallet_private_key = Column(String, ForeignKey('wallet.private_key'))

    transactions = relationship("Transaction", back_populates="user_account")

    wallet = relationship("Wallet", back_populates="user_account")


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tx_hash = Column(String(255))
    parameters = Column(JSON)
    status = Column(String(50))
    parent_tx = Column(String(255))

    user_account_id = Column(Integer, ForeignKey('user_account.id'))
    user_account = relationship("UserAccount", back_populates="transactions")


class Wallet(db.Model):
    __tablename__ = 'wallet'

    private_key = Column(String(255), unique=True, primary_key=True)

    noid_provider_id = Column(Integer, ForeignKey('noid_provider.id'))
    noid_provider = relationship("NoidProvider", back_populates="wallet")

    section_mapping_authority_id = Column(
        String, ForeignKey('section_mapping_authority.id'))
    section_mapping_authority = relationship(
        "SectionMappingAuthority", back_populates="wallet_responsable")

    decentralized_name_mapping_authority_id = Column(
        String(255), ForeignKey('decentralized_name_mapping_authority.id'))
    decentralized_name_mapping_authority = relationship(
        "DecentralizedNameMappingAuthority", back_populates="wallet_responsable")


class NoidProvider(db.Model):
    __tablename__ = 'noid_provider'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nam = Column(String(255))
    dnam = Column(String(255))
    sec_nam = Column(String(255))
    sep_token = Column(String(1))
    noid_len = Column(Integer)

    decentralized_name_mapping_authority_id = Column(String(255), ForeignKey(
        'decentralized_name_mapping_authority.id'))
    decentralized_name_mapping_authority = relationship(
        "DecentralizedNameMappingAuthority", back_populates="noid_provider")

    wallet_id = Column(String, ForeignKey('wallet.private_key'))
    wallet = relationship("Wallet", back_populates="noid_provider")

    def gen(self):
        generated_value = f"{self.nam}_{self.dnam}_{self.sec_nam}"
        return generated_value


class DecentralizedNameMappingAuthority(db.Model):
    __tablename__ = 'decentralized_name_mapping_authority'

    id = Column(String(255), primary_key=True)
    ror_id = Column(String(255))
    shoulder_prefix = Column(String(255))
    noid_provider_addr = Column(String(255))
    responsable = Column(String(255))
    section_authorities = Column(String(255))

    noid_provider_id = Column(Integer, ForeignKey('noid_provider.id'))
    noid_provider = relationship(
        "NoidProvider", back_populates="decentralized_name_mapping_authority")

    section_mapping_authorities = relationship(
        "SectionMappingAuthority", back_populates="decentralized_name_mapping_authority")

    wallet_responsable_id = Column(String, ForeignKey('wallet.private_key'))
    wallet_responsable = relationship(
        "Wallet", back_populates="decentralized_name_mapping_authority")


class SectionMappingAuthority(db.Model):
    __tablename__ = 'section_mapping_authority'

    id = Column(String(255), primary_key=True)
    ror_id = Column(String(255))
    shoulder_prefix = Column(String(255))
    dNMA_id = Column(String(255))
    noid_provider_addr = Column(String(255))
    responsable = Column(String(255))

    decentralized_name_mapping_authority_id = Column(
        String(255), ForeignKey('decentralized_name_mapping_authority.id'))
    decentralized_name_mapping_authority = relationship(
        "DecentralizedNameMappingAuthority", back_populates="section_mapping_authorities")

    wallet_responsable_id = Column(String, ForeignKey('wallet.private_key'))
    wallet_responsable = relationship(
        "Wallet", back_populates="section_mapping_authority")


with app.app_context():
    db.create_all()
