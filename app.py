############################################################################################
# importing needed libraries
import os, datetime, time
from flask import *
from flask_cors import CORS, cross_origin
from pytube import YouTube
from pytube.cli import on_progress
from flask import send_from_directory
from flask_compress import Compress
from flask_minify import Minify
from flask_wtf.csrf import CSRFProtect
from flask_cdn import CDN
from flask_sslify import SSLify
############################################################################################



############################################################################################
# configuring flask application
app = Flask(
    __name__,
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
)

SSLify(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['CDN_DOMAIN'] = 'd12vn54927k41s.cloudfront.net'
CDN(app)

CORS(app)
CSRFProtect(app)
Compress(app)
Minify(app, html=True, js=True, cssless=True)
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
# Loading page
@app.route('/')
@cross_origin()
def loading():
    return render_template("loading.html")
############################################################################################



############################################################################################
# Contact page
@app.route("/contact-us", methods=["GET"])
@cross_origin()
def contact():
    return render_template('contact_page.html')
############################################################################################



############################################################################################
# Terms page
@app.route("/terms-of-use", methods=["GET"])
@cross_origin()
def terms():
    return render_template('terms_page.html')
############################################################################################



############################################################################################
# Privacy page
@app.route("/privacy-policy", methods=["GET"])
@cross_origin()
def privacy():
    return render_template('privacy_page.html')
############################################################################################



############################################################################################
# Home page route
@app.route("/", methods=["GET", "POST"])
@cross_origin()
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
@cross_origin()
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
@cross_origin()
def yt_res_720p_download():
    path = yt.streams.get_by_itag('22').download(os.path.expanduser("~/Downloads")).strip(" ")
    return send_file(path, as_attachment=True)
    
     
@app.route('/background_process_download360p', methods=["GET"])
@cross_origin()
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
# running flask server
if __name__ == "__main__":
    app.run(debug=False)
############################################################################################