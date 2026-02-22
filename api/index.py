import os
import yaml
from flask import Flask, render_template, send_from_directory

app = Flask(__name__, template_folder='../templates')

def load_data():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.yaml')
    with open(data_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'css'), filename)

@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'data'), filename)

@app.route('/<path:filename>')
def serve_root(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..'), filename)

@app.route('/')
def index():
    projects = load_data()
    return render_template('index.html', projects=projects)

@app.route('/en')
@app.route('/en/')
@app.route('/en/index.html')
def index_en():
    projects = load_data()
    return render_template('en.html', projects=projects)

if __name__ == '__main__':
    app.run(debug=True)
    