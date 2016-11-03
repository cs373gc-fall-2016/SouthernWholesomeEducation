#!/usr/bin/env python
"""Implementation of flask app for serving HTML pages"""

import os
import sys
import requests
from flask import Flask, render_template, send_from_directory, jsonify, make_response, request, send_file
from models import *
import requests
DEFAULT_PAGE = 10

COLUMN_KEYS = { "University": {
					"University": "name",
					"Number of Undergraduates": "num_undergrads",
					"Cost to Attend": "cost_to_attend",
					"Graduation Rate": "grad_rate",
					"Public/Private": "public_or_private"},
				"City": {
					"City": "name",
				  "Population": "population",
				  "Universities": "university_list",
				  "Ethnicities": "ethnicity_list",
				  "Majors": "major_list",
				  "Average Tuition": "avg_tuition"},
				"Major": {
					"Major": "name",
					"Total Number": "num_undergrads",
					"Top City": "top_city",
					"Average Percentage": "avg_percentage",
					"Number of Supported Universities": "assoc_university"},
				"Ethnicity": {
				  "Ethnicity": "name",
				  "Total Count": "total_count",
		      "Top City": "top_city",
				  "Top University": "top_university",
				  "Peak Year": "peak_year"}}

@APP.route('/')
def render_home():
    """Return index.html page when no path is given"""
    return send_file('templates/index.html')

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
        sort_by = COLUMN_KEYS[model_name][request.args['sort']]

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
