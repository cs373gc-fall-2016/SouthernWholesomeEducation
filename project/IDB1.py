# pylint: disable=W0401,W0123,W0614,W0612,W0613,W0611
#!/usr/bin/env python
"""Implementation of flask app for serving HTML pages"""

import os
from flask import Flask, send_from_directory, jsonify, \
    make_response, request, send_file
from models import *
DEFAULT_PAGE = 10

@APP.route('/')
def render_home():
    """Return index.html page when no path is given"""
    return send_file('templates/index.html')



@APP.route('/api/<string:model_name>/id/<int:id_param>')
def lookup_model(model_name, id_param):
    """Return information for a model given the model type and ID"""
    model = get_association(get_model(model_name), id_num=id_param)

    return jsonify(results=model.attributes())

@APP.route('/api/<string:model_name>/name/<string:name>')
def lookup_model_by_name(model_name, name):
    """Return information for a model given the model type and name"""
    name = name.title()
    model = get_association(get_model(model_name), name=name)

    return jsonify(results=model.attributes())

@APP.route('/api/<string:model_name>/')
@APP.route('/api/<string:model_name>/<int:page>')
def api_models(model_name, page=0):
    """Return list of models for the Models table page"""
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
        models = eval('{0}.query.distinct({0}.name).order_by({0}.{1}{2}). \
            offset(offset).limit(page_size).all()'.format(model_name, sort_by, order))
    else:
        models = eval('{0}.query.offset(offset).limit(page_size).all()'.format(model_name))

    list_models = models
    json_list = []
    for i in list_models:
        json_list.append(i.attributes())
    return jsonify(results=json_list)


@APP.route('/api/<string:model_name>/num_pages')
def get_num_pages(model_name):
    """Return number of pages"""
    return jsonify(result=5)


@APP.route('/favicon.ico')
def favicon():
    """Return the favicon.ico"""
    return send_from_directory(os.path.join(APP.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    APP.run()
