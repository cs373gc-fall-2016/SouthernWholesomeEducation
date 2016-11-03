#!/usr/bin/env python
"""Implementation of flask app for serving HTML pages"""

import os
import sys
import requests
from flask import Flask, render_template, send_from_directory, jsonify, make_response, request, send_file
from models import *
DEFAULT_PAGE = 10

@APP.route('/')
def render_home():
    """Return index.html page when no path is given"""
    return send_file('templates/index.html')



@APP.route('/api/<string:model_name>/id/<int:id_param>')
def lookup_model(model_name, id_param):
    model = get_association(get_model(model_name), id_num=id_param)

    return jsonify(results=model.attributes())

@APP.route('/api/<string:model_name>/name/<string:name>')
def lookup_model_by_name(model_name, name):
    model = get_association(get_model(model_name), name=name)

    return jsonify(results=model.attributes())

@APP.route('/api/<string:model_name>/')
@APP.route('/api/<string:model_name>/<int:page>')
def api_models(model_name, page=0):
    model_name = model_name.title()
    json = {'page': page}
    page_size = DEFAULT_PAGE
    if 'page_size' in request.args:
        page_size = int(request.args['page_size'])
    json['page_size'] = page_size

    offset = (page - 1) * page_size if page > 0 else 0
    json['total_entries'] = get_count(model_name)

    if 'sort' in request.args:
        sort_by = request.args['sort']

        order = ".desc()" if request.args['order'] == 'desc' else ""
        models = eval('{0}.query.distinct({0}.name).order_by({0}.{1}{2}).offset(offset).limit(page_size).all()'.format(model_name, sort_by, order))
    else:
        models = eval('{0}.query.offset(offset).limit(page_size).all()'.format(model_name))

    list_models = models
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
