#!/usr/bin/env python
"""Implementation of flask app for serving HTML pages"""

import os
import sys
import requests
from flask import Flask, render_template, send_from_directory, jsonify, make_response, request
from models import *
DEFAULT_PAGE = 10

@APP.route('/')
def render_home():
    """Return index.html page when no path is given"""
    return render_template('index.html')

@APP.route('/about/')
def render_about():
    """Return HTML page stored in templates directory"""
    return render_template('about.html')

@APP.route('/index/')
def render_index():
    """Return HTML page stored in templates directory"""
    return render_template('index.html')

# # We assume this will always list out database entries
# @APP.route('/detail/')
# def render_detail():
#     """Return HTML page stored in templates directory"""
#     myUni_all = University.query.all()
#     return render_template('detail.html', myUni_all = myUni_all)


# @APP.route('/university/')
# def render_uni_table():
#     """Return HTML page stored in templates directory"""
#     entries = University.query.all()
#     return render_template('table.html', entries=jsonify(entries), title="Universities")
#
# @APP.route('/city/')
# def render_city_table():
#     """Return HTML page stored in templates directory"""
#     entries = City.query.all()
#     return render_template('table.html', entries=entries, title="Cities")
#
# @APP.route('/major/')
# def render_major_table():
#     """Return HTML page stored in templates directory"""
#     entries = Major.query.all()
#     return render_template('table.html', entries=entries, title="Majors")
#
# @APP.route('/ethnicity/')
# def render_ethnicity_table():
#     """Return HTML page stored in templates directory"""
#     entries = Ethnicity.query.all()
#     return render_template('table.html', entries=entries, title="Ethnicities")

# @APP.route('/<string:page_name>/')
# def render_static(page_name):
#     """Return HTML page stored in templates directory"""
# return render_template('%s' % page_name)

@APP.route('/<string:model_name>/')
def render_models(model_name):
    if model_name == 'university' or model_name == 'major' or model_name == 'city' or model_name == 'ethnicity':
        return make_response(open('templates/table.html').read())
    else:
        return render_template('index.html')

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
        models = eval('{0}.query.order_by({0}.{1}{2}).offset(offset).limit(page_size).all()'.format(model_name, sort_by, order))
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
