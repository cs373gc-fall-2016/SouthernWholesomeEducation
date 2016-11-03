#!/usr/bin/env python
"""Implementation of flask app for serving HTML pages"""

import os
from flask import send_file, send_from_directory, jsonify
from models import *

@APP.route('/')
def render_home():
    """Return index.html page when no path is given"""
    return send_file('templates/index.html')

@APP.route('/api/<string:model_name>/')
def api_models(model_name):
    model_name = model_name.title()
    list_models = get_models(model_name)
    json_list = []
    for i in list_models:
        json_list.append(i.attributes())
    return jsonify(results=json_list)


@APP.route('/favicon.ico')
def favicon():
    """Return the favicon.ico"""
    return send_from_directory(os.path.join(APP.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    APP.run()
