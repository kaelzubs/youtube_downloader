############################################################################################
# importing needed libraries
import os, datetime, time
from flask import *
from pytube import YouTube
from pytube.cli import on_progress
from flask import send_from_directory
from flask_compress import Compress
from flask_minify import Minify
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5
from flask_cdn import CDN
from flask_caching import Cache
from flask_assets import Environment
from flask_cors import CORS
from flask_sslify import SSLify
############################################################################################



############################################################################################
# configuring flask application
config = {
    "DEBUG": True,                # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(
    __name__,
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
)

CORS(app)

Compress(app)

BOOTSTRAP_SERVE_LOCAL = True
SECRET_KEY = os.urandom(32)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['FLASK_ASSETS_USE_CDN'] = True
app.config['CDN_DOMAIN'] = 'd12vn54927k41s.cloudfront.net'

CDN(app)

Bootstrap5(app)

csrf = CSRFProtect(app)
# csrf.init_app(app)

assets = Environment()
assets.init_app(app)

Minify(app=app, html=True, js=True, cssless=True)

app.config.from_mapping(config)
Cache(app)

SSLify(app, subdomains=True, permanent=True)
############################################################################################



############################################################################################
# bytes pretty-printing
UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]

def pretty_size(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix
############################################################################################



############################################################################################
@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy']="default-src 'self' http://mp4us.live; connect-src 'none';"
    resp.headers['Content-Security-Policy']="connect-src http://mp4us.live; script-src 'nonce-[random-value]' 'strict-dynamic'; object-src https://mp4us.live"
    return resp
############################################################################################



############################################################################################
# Loading page
@app.route('/')
def loading():
    return render_template("loading.html")
############################################################################################



############################################################################################
# Contact page
@app.route("/contact-us", methods=["GET"])
def contact():
    return render_template('contact_page.html')
############################################################################################



############################################################################################
# Terms page
@app.route("/terms-of-use", methods=["GET"])
def terms():
    return render_template('terms_page.html')
############################################################################################



############################################################################################
# Privacy page
@app.route("/privacy-policy", methods=["GET"])
def privacy():
    return render_template('privacy_page.html')
############################################################################################



############################################################################################
# Home page route
@app.route("/", methods=["GET", "POST"])
def index():
    data_list = []
    if request.method == "POST":
        yt_url = request.form.get("q")
        yt = YouTube(yt_url, on_progress_callback=on_progress)
        yt_emb = yt_url.replace('/watch?v=', '/embed/')
        yt_res_720p = yt.streams.get_by_itag('22').resolution
        yt_res_360p = yt.streams.get_by_itag('18').resolution

        yt_size_720p = yt.streams.get_by_itag('22').filesize
        yt_file_size_pretty_720p = pretty_size(yt_size_720p)
        yt_size_360p = yt.streams.get_by_itag('18').filesize
        yt_file_size_pretty_360p = pretty_size(yt_size_360p)

        yt_title = yt.streams[0].title
        yt_desc = yt.description
        yt_length = yt.length
        yt_duration = str(datetime.timedelta(seconds=yt_length))
        yt_file_format = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first().mime_type

        data_obj = {
            'url': yt_url,
            'url_emb': yt_emb,
            'title': yt_title,
            'description': yt_desc,
            'duration': yt_duration,
            'file_format': yt_file_format,

            'seven': yt_res_720p,
            'three': yt_res_360p,

            'file_size_720p': yt_file_size_pretty_720p,
            'file_size_360p': yt_file_size_pretty_360p,
        }
        data_list.append(data_obj)
        
    return render_template("base.html", data=data_list)
############################################################################################



############################################################################################
# Download page
@app.route("/download", methods=["GET", "POST"])
def download():
    data_list = []
    if request.method == "POST":
        global yt
        global yt_url
        yt_url = request.form.get("q")
        yt = YouTube(yt_url, on_progress_callback=on_progress)
        yt_emb = yt_url.replace('/watch?v=', '/embed/')
        yt_res_720p = yt.streams.get_by_itag('22').resolution
        yt_res_360p = yt.streams.get_by_itag('18').resolution

        yt_size_720p = yt.streams.get_by_itag('22').filesize
        yt_file_size_pretty_720p = pretty_size(yt_size_720p)
        yt_size_360p = yt.streams.get_by_itag('18').filesize
        yt_file_size_pretty_360p = pretty_size(yt_size_360p)        

        yt_title = yt.streams[0].title
        yt_desc = yt.description
        yt_length = yt.length
        yt_duration = str(datetime.timedelta(seconds=yt_length))
        yt_file_format = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first().mime_type

        data_obj = {
            'url': yt_url,
            'url_emb': yt_emb,
            'title': yt_title,
            'description': yt_desc,
            'duration': yt_duration,
            'file_format': yt_file_format,

            'seven': yt_res_720p,
            'three': yt_res_360p,

            'file_size_720p': yt_file_size_pretty_720p,
            'file_size_360p': yt_file_size_pretty_360p,
        }
        data_list.append(data_obj)
        time.sleep(0.5)

    elif request.method == 'GET':
        return redirect('/')
    else:
        return 'Not a valid request method for this route'

    return render_template("download.html", data=data_list)
############################################################################################



############################################################################################
# Download Route
@app.route('/background_process_download720p', methods=["GET"])
def yt_res_720p_download():
    path = yt.streams.get_by_itag('22').download(os.path.expanduser("~/Downloads")).strip(" ")
    return send_file(path, as_attachment=True)
    
     
@app.route('/background_process_download360p', methods=["GET"])
def yt_res_360p_download():
    path = yt.streams.get_by_itag('18').download(os.path.expanduser("~/Downloads")).strip(" ")
    return send_file(path, as_attachment=True)
############################################################################################



############################################################################################
# Error 404 page
@app.errorhandler(404)
def not_found(e):
    return render_template('custom_page404.html'), 404
############################################################################################



############################################################################################
# Error 400 page
@app.errorhandler(400)
def not_found(e):
    return render_template('custom_page400.html'), 400
############################################################################################



############################################################################################
# Error 405 page
@app.errorhandler(405)
def not_found(e):
    return render_template('custom_page405.html'), 405

############################################################################################



############################################################################################
# Error 500 page
@app.errorhandler(500)
def not_found(e):
  return render_template('custom_page500.html'), 500
############################################################################################



############################################################################################
# Implement Cookie Law
def cookies_check():
    value = request.cookies.get('cookie_consent')
    return value == 'true'


@app.context_processor
def inject_template_scope():
    injections = dict()
    injections.update(cookies_check=cookies_check)
    return injections
############################################################################################



############################################################################################
@app.before_request
def before_request():
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
############################################################################################



############################################################################################
# running flask server
if __name__ == "__main__":
    app.run(debug=False)
############################################################################################