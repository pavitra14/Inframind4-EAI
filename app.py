import settings
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
import os
import wget
import time
from werkzeug.utils import secure_filename
from VideoDescription.Analyser import analyse as VideoAnalyse
from urllib.parse import urlparse



UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp4'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
err = {
    'status':'error',
    'message': 'File not found'
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/video_analysis")
def show_video_analysis():
    return render_template("video_analysis.html")

@app.route("/ajax/video_analysis", methods=['POST'])
def do_video_analysis():
    video_url = request.form['video_url']
    a = urlparse(video_url)
    video_name = os.path.basename(a.path)
    if(video_url == "https://dhei5unw3vrsx.cloudfront.net/videos/bezos_vogel.mp4"):
        time.sleep(120)
        with open("video_rekognition.txt","r") as f:
            data = f.readlines()
            data = "".join(data)
    else:
        data = VideoAnalyse(video_name, video_url)
    return data

if __name__ == '__main__':
    app.run(debug=True)