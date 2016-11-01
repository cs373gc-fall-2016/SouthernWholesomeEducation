#!/usr/bin/env python
"""Implementation of flask app for serving HTML pages"""

import os
from flask import Flask, render_template, send_from_directory
from models import *

APP = Flask(__name__)
@APP.route('/')
def render_home():
    """Return index.html page when no path is given"""
    return render_template('index.html')

@APP.route('/about/')
def render_about():
    """Return HTML page stored in templates directory"""
    return render_template('about.html')

@APP.route('/index/')
def render_about():
    """Return HTML page stored in templates directory"""
    return render_template('index.html')

# We assume this will always list out database entries
@APP.route('/<string:table_name>/')
def render_detail():
    """Return HTML page stored in templates directory"""
    myUni_all = table_name.query.all()
    myUni = 1
    # myUni = University.query.filter_by(name='UT').first()
    print (myUni)
    print (myUni_all)
    return render_template('detail.html', myUni = myUni, myUni_all = myUni_all)


# @APP.route('/university/<string:uni_name>/')
# def render_uni_detail():
#     """Return index.html page when no path is given"""
#     myUni = University.query.all()
#     return render_template('detail.html', myUni=myUni)


@APP.route('/favicon.ico')
def favicon():
    """Return the favicon.ico"""
    return send_from_directory(os.path.join(APP.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    APP.run()
