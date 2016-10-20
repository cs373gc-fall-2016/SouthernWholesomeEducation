"""Implmentation of flask app for serving HTML pages"""

import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route('/<string:page_name>/')
def render_static(page_name):
    """Return HTML page stored in templates directory"""
    return render_template('%s' % page_name)

@app.route('/')
def render_home():
    """Return index.html page when no path is given"""
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    """Return the favicon.ico"""
    return send_from_directory(os.path.join(app.root_path, 'static'), \
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run()
