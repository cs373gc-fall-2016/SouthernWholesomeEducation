import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s' % page_name)

@app.route('/')
def render_home():
    return render_template('index.html')

@app.route('/<string:folder_name>/<string:page_name>')
def send_js(folder_name, page_name):
    return send_from_directory(os.path.join(app.root_path, 'templates/%s' % folder_name), '%s' % page_name)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run()
