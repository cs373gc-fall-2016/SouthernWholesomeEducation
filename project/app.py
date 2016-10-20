from flask import Flask, render_template
 
app = Flask(__name__, static_url_path='/templates')
 
@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s' % page_name)

@app.route('/')
def render_home():
    return render_template('index.html')
 
if __name__ == "__main__":
    app.run()
