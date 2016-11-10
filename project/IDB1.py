# pylint: disable=W0401,W0123,W0614,W0612,W0613,W0611
#!/usr/bin/env python
"""Implementation of flask app for serving HTML pages"""

import os
import subprocess
import re
from flask import Flask, send_from_directory, jsonify, \
    make_response, request, send_file, render_template
from models import *
import requests
import json as jsonlib
from statistics import get_github_stats

DEFAULT_PAGE = 10
convert_names = {'name':'Name', 'university_name':'University','major_name':'Major',
    'num_undergrads':'Number of Undergraduates','ethnicity_name':'Ethnicity',
    'cost_to_attend':'Cost to Attend', 'grad_rate':'Graduation Rate',
    'public_or_private':'Public/Private', 'city_name':'City', 'majors':'Major',
    'ethnicities':'Ethnicity', 'population':'Population', 'uni_count':'University Count',
    'maj_count':'Major Count', 'avg_tuition':'Average Tuition', 'universities':'University',
    'top_city':'Top City', 'top_city_amt':'Top City Amount', 'top_university':'Top University',
    'top_university_amt':'Top University Amount', 'major_num_students':'Major Number of Students',
    'ethnicity_num_students':'Ethnicity Number of Students', 'top_major':'Top Major',
    'top_ethnicity':'Top Ethnicity'}
plural_names = {University:'universities', City:'cities', Major:'majors',
    Ethnicity:'ethnicities'}
model_names = {University:'University', City:'City', Major:'Major', Ethnicity:'Ethnicity'}

@APP.route('/')
def render_home():
    """Return index.html page when no path is given"""
    return send_file('templates/index.html')

@APP.route('/githubstats')
def render_github_stats():
    """Render github statistics for group members"""
    return jsonify(get_github_stats())

@APP.route('/angular-advanced-searchbox.html')
def render_searchbox():
    return send_file('templates/angular-advanced-searchbox.html')

@APP.errorhandler(404)
@APP.errorhandler(500)
def error_page(error):
    """Error handler for Flask"""
    return "error"

# @APP.route('/image/<string:name>')
# def get_image(name):
#     response = requests.get('http://api.duckduckgo.com/?q=' + name + '&format=json&pretty=1').text
#     values = jsonlib.load(response)
#     return values['Image']


@APP.route('/api/runUnitTests')
def run_tests():
    """Trigger running unit tests"""
    return subprocess.getoutput('python3 tests.py')

@APP.route('/api/<string:model_name>/id/<int:id_param>')
def lookup_model(model_name, id_param):
    """Return information for a model given the model type and ID"""
    model = get_association(get_model(model_name), id_num=id_param)
    # if model is None:
        # return error_page()
    return jsonify(results=model.attributes())

@APP.route('/api/<string:model_name>/name/<string:name>')
def lookup_model_by_name(model_name, name):
    """Return information for a model given the model type and name"""
    name = name.title()
    model = get_association(get_model(model_name), name=name)
    # if model is None:
        # return error_page()

    return jsonify(results=model.attributes())

@APP.route('/model/<string:model_name>/start/<int:start>/number/<int:num_items>/attr/<string:attr>/reverse/<string:is_reverse>')
def pagination_sort(model_name, start, num_items, attr, is_reverse):
    """Server side pagination with sorting"""
    if is_reverse == 'true':
        is_reverse = '.desc()'
    else:
        is_reverse = ''
    remove_duplicates = ".filter(text(\"assoc_university=1\"))"
    paginate = ".offset(start).limit(num_items).all()"
    if attr == 'undefined':
        if model_name == 'University' or model_name == 'City':
            list_models = eval(('{0}.query' + paginate).format(model_name))
        else:
            list_models = eval(('{0}.query' + remove_duplicates + paginate).format(model_name))
    else:
        if model_name == 'University' or model_name == 'City':
            list_models = eval(('{0}.query.order_by({0}.{1}{2})' + paginate) \
                .format(model_name, attr, is_reverse))
        else:
            list_models = eval(('{0}.query' + remove_duplicates \
            + '.order_by({0}.{1}{2})' + paginate).format(model_name, attr, is_reverse))

    json_list = []
    for i in list_models:
        json_list.append(i.attributes())
    if model_name == 'University' or model_name == 'City':
        row_count = eval('{0}.query.count()'.format(model_name))
    else:
        row_count = eval('{0}.query.count()'.format(model_name)) // 2
    num_pages = row_count // num_items
    num_pages += (1 if row_count % num_items else 0)
    return jsonify(results=json_list, numpages=num_pages)

@APP.route('/search/<string:query>')
def get_search(query):
    university_columns = ['university_name', 'num_undergrads', 'cost_to_attend', 'grad_rate',
        'public_or_private', 'city_name', 'major_name', 'major_num_students',
        'ethnicity_name', 'ethnicity_num_students']
    city_columns = ['university_name','city_name','population','avg_tuition','top_university',
        'top_major','top_ethnicity','major_name','major_num_students','ethnicity_name',
        'ethnicity_num_students']
    andResults = []
    orResults = []
    city_university_search(andResults, University, 'AND', query, university_columns, 'university_name')
    city_university_search(orResults, University, 'OR', query, university_columns, 'university_name')
    # city_university_search(andResults, City, 'AND', query, city_columns, 'city_name')
    # city_university_search(orResults, City, 'OR', query, city_columns, 'city_name')
    return jsonify(orResults=[], andResults=andResults)

def city_university_search(results, model, op, query, columns, param):
    q_array = query.split()
    if model == University:
        sql = "SELECT * FROM (SELECT U.id_num,MU.university_name,U.num_undergrads,U.cost_to_attend,U.grad_rate,U.public_or_private,U.city_name,MU.major_name,MU.num_students AS major_num_students,EU.ethnicity_name,EU.num_students AS ethnicity_num_students FROM \"UNIVERSITY\" AS U JOIN \"MAJORTOUNIVERSITY\" MU ON U.id_num=MU.university_id JOIN \"ETHNICITYTOUNIVERSITY\" EU ON U.id_num=EU.university_id) sq WHERE sq::text ILIKE '%%" + q_array[0] + "%%'"
    else:
        sql = "SELECT * FROM (SELECT U.name AS university_name,C.id_num,MC.city_name,C.population,C.avg_tuition,C.top_university,C.top_major,C.top_ethnicity,MC.major_name,MC.num_students AS major_num_students,EC.ethnicity_name,EC.num_students AS ethnicity_num_students FROM \"CITY\" AS C JOIN \"MAJORTOCITY\" MC ON C.id_num=MC.city_id JOIN \"ETHNICITYTOCITY\" EC ON C.id_num=EC.city_id JOIN \"UNIVERSITY\" U ON U.city_id=C.id_num) sq WHERE sq::text ILIKE '%%" + q_array[0] + "%%'"
    for q in q_array[1:]:
        sql += (" " + op + " sq::text ILIKE '%%" + q + "%%'")
    model_results = DB.engine.execute(sql + ';')
    model_results_iter = iter(model_results)
    try:
        row = next(model_results_iter)
        while True:
            result = {}
            result['Context'] = ""
            for col in columns:
                temp_str = convert_names[col] + ': ' + str(eval(('row.{0}').format(col))) + '\n'
                result['Context'] += temp_str
            old_row = row
            try:
                row = next(model_results_iter)
            except StopIteration:
                row = None
            while row and eval(('row.{0}').format(param))==eval(('old_row.{0}').format(param)):
                for col in columns:
                    temp_str = convert_names[col] + ': ' + str(eval(('row.{0}').format(col))) + '\n'
                    if temp_str not in result['Context']:
                        result['Context'] += temp_str
                row = next(model_results_iter)
            for q in q_array:
                pattern = re.compile(q, re.IGNORECASE)
                result['Context'] = pattern.sub("<b>"+q+"</b>", result['Context'])
            temp_array = result['Context'].split('\n')
            result['Context'] = ""
            for temp in temp_array:
                if '<b>' in temp:
                    result['Context'] += temp + '<br>'
            result['model'] = model_names[model]
            result['name'] = eval(('old_row.{0}').format(param))
            result['plural'] = plural_names[model]
            result['id_num'] = old_row.id_num
            results.append(result)
    except StopIteration:
        pass

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
