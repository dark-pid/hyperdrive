import os
from flask import Flask

# TODO: Definir melhor
# PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = '.'

# templates
template_dir = os.path.join(PROJECT_ROOT, 'templates')

app = Flask(__name__, template_folder=template_dir)
