import pandas as pd
from flask_bcrypt import Bcrypt
from model import db, User

from instance_app import create_app

app = create_app()


with app.app_context():
    bcrypt = Bcrypt(app)

    csv_file_path = 'database/users.csv'
    df = pd.read_csv(csv_file_path)
    db.create_all()

    for index, row in df.iterrows():
        password = row['password']
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        new_user = User(
            email=row['email'],
            password=hashed_password,
            wallet_private_key=row['wallet_private_key']
        )
        db.session.add(new_user)

    db.session.commit()
