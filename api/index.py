import os
import yaml
from flask import Flask, render_template, send_from_directory, request, make_response

app = Flask(__name__, template_folder='../templates')

TRANSLATIONS = {
    'ja': {
        'work_title': 'Work',
        'work_desc': 'インターフェース・映像・教育の「新しい」表現や体験の方法をプログラミングなどの理数的な視点から実装しています。',
        'about_title': 'About Suke(木崎 公亮)',
        'contact': 'Contact (Mail)',
        'research_title': '研究活動/Research',
    },
    'en': {
        'work_title': 'Work',
        'work_desc': 'I implement “new” methods of expression and experience in interface, video, and education from a mathematical and scientific perspective, such as programming.',
        'about_title': 'About Suke',
        'contact': 'Contact (Mail)',
        'research_title': 'Research',
    }
}

def load_data():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.yaml')
    with open(data_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_lang():
    lang = request.args.get('lang')
    if lang in ['ja', 'en']:
        return lang
    
    lang = request.cookies.get('lang')
    if lang in ['ja', 'en']:
        return lang
    
    accept_lang = request.headers.get('Accept-Language', '')
    if accept_lang.startswith('en'):
        return 'en'
    return 'ja'

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'css'), filename)

@app.route('/data/<path:filename>')
def serve_data(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'data'), filename)

@app.route('/')
@app.route('/index.html')
def index():
    lang = get_lang()
    projects = load_data()
    
    response = make_response(render_template('index.html', 
                                         projects=projects, 
                                         lang=lang, 
                                         t=TRANSLATIONS[lang]))
    
    if request.args.get('lang'):
        response.set_cookie('lang', lang, max_age=30*24*60*60) # 30 days
    return response

@app.route('/about')
@app.route('/about.html')
def about():
    lang = get_lang()
    response = make_response(render_template('about.html', 
                                         lang=lang, 
                                         t=TRANSLATIONS[lang]))
    
    if request.args.get('lang'):
        response.set_cookie('lang', lang, max_age=30*24*60*60)
    return response

@app.route('/en')
@app.route('/en/')
@app.route('/en/index.html')
def index_en_legacy():
    # Redirect legacy /en to root with lang=en
    response = make_response(app.redirect('/?lang=en'))
    return response

@app.errorhandler(404)
def page_not_found(e):
    # Try to serve as a static file if it exists in root (for things like CNAME, etc)
    filename = request.path.lstrip('/')
    root_dir = os.path.join(os.path.dirname(__file__), '..')
    if os.path.isfile(os.path.join(root_dir, filename)):
        return send_from_directory(root_dir, filename)
    return send_from_directory(root_dir, '404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
    