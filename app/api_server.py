import sys
import os

from flask import Flask , jsonify , render_template, send_file, abort
# from flask import render_template, request, Flask, g, send_from_directory, abort, jsonify
from api.query_api import queries_blueprint


#TODO: Definir melhor
# PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = '.'

# templates
template_dir = os.path.join(PROJECT_ROOT,'templates')

app = Flask(__name__,template_folder=template_dir)

app.config['JSON_AS_ASCII'] = False #utf8
app.config['JSON_SORT_KEYS'] = False #prevent sorting json

app.register_blueprint(queries_blueprint)

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == "__main__":
    #TODO: RECUPERAR A PORTA DO ENV
    app.run(host='0.0.0.0', port=8080)