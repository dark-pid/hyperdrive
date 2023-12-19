import os
from flask import Flask

from database.variables_database import ConfigVariables
from model import configure as config_db
from serealize import configure as config_ma

from flask_migrate import Migrate

# TODO: Definir melhor
# PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = '.'

config_variables = ConfigVariables()


USE_AUTH = os.environ.get('HYPERDRIVE_AUTH', 'true').lower() == 'true'

# templates
template_dir = os.path.join(PROJECT_ROOT, 'templates')


def create_app():
    app = Flask(__name__, template_folder=template_dir)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

    config_db(app)
    config_ma(app)

    Migrate(app, app.db)

    return app
