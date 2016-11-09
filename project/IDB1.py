# pylint: disable=W0401,W0123,W0614,W0612,W0613,W0611
#!/usr/bin/env python
"""Implementation of flask app for serving HTML pages"""

import os
import subprocess
from flask import Flask, send_from_directory, jsonify, \
    make_response, request, send_file, render_template
from models import *
import requests
import json as jsonlib
from statistics import get_github_stats

DEFAULT_PAGE = 10

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

# @APP.route('/api/<string:model_name>/')
# @APP.route('/api/<string:model_name>/<int:page>')
# def api_models(model_name, page=0):
#     """Return list of models for the Models table page"""
#     model_name = model_name.title()
#     json = {'page': page}
#     page_size = DEFAULT_PAGE
#     if 'page_size' in request.args:
#         page_size = int(request.args['page_size'])
#     json['page_size'] = page_size
#
#     offset = (page - 1) * page_size if page > 0 else 0
#     json['total_entries'] = get_count(model_name)
#
#     if 'sort' in request.args:
#         sort_by = request.args['sort']
#
#         order = ".desc()" if request.args['order'] == 'desc' else ""
#         if model_name == "University" and sort_by == "city_id":
#             models = eval('University.query.join(City, University.city_id==City.id_num)\
#                 .order_by(City.name{0}).offset(offset).limit(page_size).all()'.format(order))
#
#         elif model_name == "City" and (sort_by == "university_list"
# or sort_by == "major_list" or sort_by == "ethnicity_list"):
#             models = eval('City.query.order_by(func.count(sort_by)).group_by(City.id_num).offset
#(offset).limit(page_size).all()'.format(sort_by))
#
#         else:
#             models = eval('{0}.query.order_by({0}.{1}{2}). \
#             offset(offset).limit(page_size).all()'.format(model_name, sort_by, order))
#     else:
#         models = eval('{0}.query.offset(offset).limit(page_size).all()'.format(model_name))
#     # if models is None:
#         # return error_page()
#
#     list_models = models
#     json_list = []
#     for i in list_models:
#         json_list.append(i.attributes())
#     return jsonify(results=json_list)

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
    model_list = [Ethnicity, Major]
    model_names = {University:'University', City:'City', Major:'Major',
        Ethnicity:'Ethnicity'}
    plural_names = {University:'universities', City:'cities', Major:'majors',
        Ethnicity:'ethnicities'}
    convert_names = {'name':'Name', 'num_undergrads':'Number of Undergraduates',
        'cost_to_attend':'Cost to Attend', 'grad_rate':'Graduation Rate',
        'public_or_private':'Public/Private', 'city_name':'City', 'majors':'Major',
        'ethnicities':'Ethnicity', 'population':'Population', 'uni_count':'University Count',
        'maj_count':'Major Count', 'avg_tuition':'Average Tuition', 'universities':'University',
        'top_city':'Top City', 'top_city_amt':'Top City Amount', 'top_university':'Top University',
        'top_university_amt':'Top University Amount'}
    q_array = query.lower().split()
    results = []
    for model in model_list:
        if model == Ethnicity or model == Major:
            models = model.query.filter_by(assoc_university=1)
        else:
            models = model.query.all()
        for row in models:
            attr = row.attributes()
            result = {}
            result['Context'] = ""
            for q in q_array:
                for key, value in attr.items():
                    if isinstance(value, list):
                        for e in value:
                            for k,v in e.items():
                                if q in str(v).lower():
                                    result['Context'] += convert_names[key] + ': ' + v.lower().replace(q, '<b>'+q+'</b>') + '<br>'
                    else:
                        if q in str(value).lower():
                            result['Context'] += convert_names[key] + ': ' + value.lower().replace(q,'<b>'+q+'</b>') + '<br>'
            if len(result['Context']):
                temp_list = [temp.capitalize() for temp in result['Context'].split(' ')]
                result['Context'] = ' '.join(temp_list)
                result['model'] = model_names[model]
                result['name'] = attr['name']
                result['plural'] = plural_names[model]
                result['id_num'] = attr['id_num']
                results.append(result)
    and_results = []
    for i in results:
        and_found = True
        for q in q_array:
            if q not in i['Context'].lower():
                and_found = False
                break
        if and_found:
            and_results.append(i)
    return jsonify(orResults=results, andResults=and_results)

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
