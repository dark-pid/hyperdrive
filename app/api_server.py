import sys
import os
from flask import Flask, jsonify, render_template, send_file, abort
# from flask import render_template, request, Flask, g, send_from_directory, abort, jsonify
from instance_app import create_app
from api.query_api import queries_blueprint
from api.core_api import core_api_blueprint
from api.user_api import user_api_blueprint 
from util.auth_middleware import authentication_middleware
from flask_swagger_ui import get_swaggerui_blueprint

app = create_app()

# basic config
app.config['JSON_AS_ASCII'] = False  # utf8
app.config['JSON_SORT_KEYS'] = False  # prevent sorting json

# swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name' : "hiperdrive API"
    }
)

app.before_request(authentication_middleware)

# blueprint registry
app.register_blueprint(queries_blueprint)
app.register_blueprint(core_api_blueprint)
app.register_blueprint(user_api_blueprint)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

@app.route('/')


def index():
    return render_template('home.html')



if __name__ == "__main__":
    # TODO: RECUPERAR A PORTA DO ENV
    app.run(host='0.0.0.0', port=8080)
