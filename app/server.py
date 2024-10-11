import sys
import os
import json

from flask import Flask , jsonify , render_template, send_file, abort

from services.load_api import load_api
# from shared_utils import MANAGED_NAM_DICT

# # PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = '.'


# templates
template_dir = os.path.join(PROJECT_ROOT,'templates')

app = Flask(__name__,template_folder=template_dir)

#basic config
app.config['JSON_AS_ASCII'] = False #utf8
app.config['JSON_SORT_KEYS'] = False #prevent sorting json



app.register_blueprint(load_api)

if __name__ == "__main__":

    try:
        resolv_port=os.environ['RESOLVER_PORT']
    except KeyError:
        resolv_port=7000    

    app.run(host='0.0.0.0', port=resolv_port)