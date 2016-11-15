# pylint: disable=W0401,W0123,W0614,W0612,W0613,W0611,E1101,W0603,R0913,R0914,R0912
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
CONVERT_NAMES = {'name':'Name', 'university_name':'University', 'major_name':'Major', \
    'num_undergrads':'Student Number', 'ethnicity_name':'Ethnicity', \
    'cost_to_attend':'Yearly Tuition', 'grad_rate':'Graduation Rate', \
    'public_or_private':'Public/Private', 'city_name':'City', 'majors':'Major', \
    'ethnicities':'Ethnicity', 'population':'Population', 'uni_count':'University Count', \
    'maj_count':'Major Count', 'avg_tuition':'Average Tuition', 'universities':'University', \
    'top_city':'Top City', 'top_city_amt':'Top City Amount', 'top_university':'Top University', \
    'top_university_amt':'Top University Amount', 'major_num_students':'Major Student Number', \
    'ethnicity_num_students':'Ethnicity Student Number', 'top_major':'Top Major', \
    'top_ethnicity':'Top Ethnicity', 'avg_percentage':'Average Percentage', \
    'total_count':'Total Ethnic Count'}
PLURAL_NAMES = {'University':'universities', 'City':'cities', 'Major':'majors', \
    'Ethnicity':'ethnicities'}
CURRENT_QUERY = ""
UNIVERSITY_AND_LIST = []
UNIVERSITY_OR_LIST = []
CITY_AND_LIST = []
CITY_OR_LIST = []
MAJOR_AND_LIST = []
MAJOR_OR_LIST = []
ETHNICITY_AND_LIST = []
ETHNICITY_OR_LIST = []

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
    """Serves up the searchbox HTML template."""
    return send_file('templates/angular-advanced-searchbox.html')

@APP.errorhandler(404)
@APP.errorhandler(500)
def error_page(error):
    """Error handler for Flask"""
    return "error"

@APP.route('/api/runUnitTests')
def run_tests():
    """Runs the unit tests for the About page."""
    return subprocess.getoutput("python3 tests.py")

@APP.route('/api/<string:model_name>')
def list_all_models(model_name):
    """List all models in the database given a model name"""
    model = get_model(model_name)
    models = model.query.all()
    list_models = [m.attributes() for m in models]
    return jsonify(results=list_models)

@APP.route('/api/<string:model_name>/<int:offset>/<int:limit>')
def list_models_range(model_name, offset, limit):
    """List models within a given range"""
    model = get_model(model_name)
    models = model.query.offset(offset).limit(limit).all()
    list_models = [m.attributes() for m in models]
    return jsonify(results=list_models)

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

@APP.route('/model/<string:model_name>/start/<int:start>/number/' + \
            '<int:num_items>/attr/<string:attr>/reverse/<string:is_reverse>')
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

@APP.route('/search/<string:model>/<string:query>/<string:bool_op>/<int:page>')
def get_search(model, query, bool_op, page):
    """Method that provides search functionality"""
    global CURRENT_QUERY
    university_columns = ['university_name', 'num_undergrads', 'cost_to_attend', \
        'grad_rate', 'public_or_private', 'city_name', 'major_name', 'major_num_students', \
        'ethnicity_name', 'ethnicity_num_students']
    city_columns = ['city_name', 'population', 'avg_tuition', 'top_university', \
        'top_major', 'top_ethnicity', 'major_name', 'major_num_students', 'ethnicity_name', \
        'ethnicity_num_students']
    major_columns = ['major_name', 'num_undergrads', 'top_city', 'top_city_amt', \
        'top_university', 'top_university_amt', 'avg_percentage']
    ethnicity_columns = ['ethnicity_name', 'total_count', 'top_city', 'top_city_amt', \
        'top_university', 'top_university_amt']
    columns_dict = {'University':university_columns, 'City':city_columns, \
        'Major':major_columns, 'Ethnicity':ethnicity_columns}
    list_results = []
    pag_list = eval(("{0}_{1}_LIST").format(model.upper(), bool_op.upper()))
    if query.lower() != CURRENT_QUERY.lower() or not len(pag_list):
        if query.lower() != CURRENT_QUERY.lower():
            del UNIVERSITY_AND_LIST[:]
            del UNIVERSITY_OR_LIST[:]
            del CITY_AND_LIST[:]
            del CITY_OR_LIST[:]
            del MAJOR_AND_LIST[:]
            del MAJOR_OR_LIST[:]
            del ETHNICITY_AND_LIST[:]
            del ETHNICITY_OR_LIST[:]
        fill_pag_list(model, query, bool_op, model.lower() + '_name', pag_list)
        CURRENT_QUERY = query
    model_search(list_results, model, bool_op, query, columns_dict[model], \
        model.lower() + '_name', page, pag_list)
    return jsonify(results=list_results, numpages=len(pag_list))

def fill_pag_list(model, query, bool_op, param, pag_list):
    """Fills in the pagination list to provide server side pagination."""
    q_array = query.split()
    sql = "SELECT t1.* FROM (SELECT *,ROW_NUMBER() OVER (ORDER BY id_num) AS row " + \
        "FROM (SELECT DISTINCT RANK() OVER (ORDER BY id_num) AS rowID," + param + \
        ",id_num FROM (" + create_sql_query(model, q_array, bool_op) + ") tab " + \
        "ORDER BY rowID) AS t) t1 WHERE (t1.row-1)%%10=0;"
    # print("### Distinct Row")
    # print(sql)
    pag_results = DB.engine.execute(sql)
    pag_iter = iter(pag_results)
    try:
        stop_loop = False
        curr_pag = next(pag_iter)
        while not stop_loop:
            offset = curr_pag.id_num - 1
            try:
                curr_pag = next(pag_iter)
            except StopIteration:
                stop_loop = True
            offset_str = "OFFSET " + str(offset)
            limit_str = " LIMIT " + ("ALL" if stop_loop else str(curr_pag.id_num - offset - 1))
            # print(offset_str + limit_str)
            pag_list.append(offset_str + limit_str)
    except StopIteration:
        pass

def create_sql_query(model, q_array, bool_op, str_limit=""):
    """Creates a SQL query given certain arguments."""
    if model == 'University':
        sql = "SELECT * FROM (SELECT U.id_num, MU.university_name, U.num_undergrads, " + \
        "U.cost_to_attend, U.grad_rate, U.public_or_private, U.city_name, MU.major_name, " + \
        "MU.num_students AS major_num_students, EU.ethnicity_name, EU.num_students AS " + \
        "ethnicity_num_students FROM (SELECT * FROM \"UNIVERSITY\" ORDER BY id_num " + \
        str_limit + ") U JOIN \"MAJORTOUNIVERSITY\" MU ON U.id_num=MU.university_id " + \
        "JOIN \"ETHNICITYTOUNIVERSITY\" EU ON U.id_num=EU.university_id) sq WHERE " + \
        "(sq::text ~* '\\y" + q_array[0] + "\\y'"
    elif model == 'City':
        sql = "SELECT * FROM (SELECT C.id_num, C.name AS city_name, C.population, " + \
        "C.avg_tuition, C.top_university, C.top_major, C.top_ethnicity, MC.major_name, " + \
        "MC.num_students AS major_num_students,EC.ethnicity_name,EC.num_students AS " + \
        "ethnicity_num_students FROM (SELECT * FROM \"CITY\" ORDER BY id_num " + \
        str_limit + ") C JOIN \"MAJORTOCITY\" MC ON C.id_num=MC.city_id JOIN " + \
        "\"ETHNICITYTOCITY\" EC ON C.id_num=EC.city_id) sq WHERE " + \
        "(sq::text ~* '\\y" + q_array[0] + "\\y'"
    elif model == 'Major':
        sql = "SELECT sq.id_num, sq.name AS major_name, sq.num_undergrads, sq.top_city, " + \
        "sq.avg_percentage, sq.top_university, sq.top_city_amt, sq.top_university_amt " + \
        "FROM (SELECT * FROM \"MAJOR\" ORDER BY id_num " + str_limit + ") sq WHERE " + \
        "sq.assoc_university = 1 AND (sq::text ~* '\\y" + q_array[0] + "\\y'"
    elif model == 'Ethnicity':
        sql = "SELECT sq.id_num, sq.name AS ethnicity_name, sq.total_count, sq.top_city, " + \
        "sq.top_city_amt, sq.top_university, sq.top_university_amt FROM (SELECT * " + \
        "FROM \"ETHNICITY\" ORDER BY id_num " + str_limit + ") sq WHERE sq.assoc_university " + \
        "= 1 AND (sq::text ~* '\\y" + q_array[0] + "\\y'"
    for q_word in q_array[1:]:
        sql += (" " + bool_op + " sq::text ~* '\\y" + q_word + "\\y'")
    sql += ") ORDER BY id_num"
    return sql


def model_search(results, model, bool_op, query, columns, param, page, pag_list):
    """Creates the contextualized field for every relevant model instance."""
    q_array = query.split()
    if page - 1 >= len(pag_list):
        return
    sql = create_sql_query(model, q_array, bool_op, pag_list[page-1])
    # print("Normal SQL")
    # print(sql)
    model_results = DB.engine.execute(sql + ';')
    model_results_iter = iter(model_results)
    stop_loop = False
    try:
        row = next(model_results_iter)
        while not stop_loop:
            result = {}
            result['Context'] = ""
            for col in columns:
                temp_str = CONVERT_NAMES[col] + ': ' + str(eval(('row.{0}').format(col))) + '\n'
                result['Context'] += temp_str
            old_row = row
            try:
                row = next(model_results_iter)
            except StopIteration:
                row = None
                stop_loop = True
            while row and eval(('row.{0}').format(param)) == eval(('old_row.{0}').format(param)):
                for col in columns:
                    temp_str = CONVERT_NAMES[col] + ': ' + str(eval(('row.{0}').format(col))) + '\n'
                    if temp_str not in result['Context']:
                        result['Context'] += temp_str
                try:
                    row = next(model_results_iter)
                except StopIteration:
                    row = None
                    stop_loop = True
            for q_word in q_array:
                pattern = re.compile(r'\b%s\b' % q_word, re.IGNORECASE)
                match_str = pattern.search(result['Context'])
                if match_str:
                    result['Context'] = pattern.sub("<b>"+match_str.group(0)+"</b>", \
                    result['Context'])
            temp_array = result['Context'].split('\n')
            result['Context'] = ""
            for temp in temp_array:
                if '<b>' in temp:
                    result['Context'] += temp + '<br>'
            result['model'] = model
            result['name'] = eval(('old_row.{0}').format(param))
            result['plural'] = PLURAL_NAMES[model]
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
