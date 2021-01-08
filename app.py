import settings
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template
import os
import wget
import time
from werkzeug.utils import secure_filename
from VideoDescription.Analyser import analyse as VideoAnalyse
from urllib.parse import urlparse
from ImageDescription.Analyser import *
from ImageDescription.utils import ImageEntity
from TextSummary.Summariser import *


UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp4', 'txt'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route("/image_analysis")
def show_image_analysis():
    return render_template("image_analysis.html")

@app.route("/ajax/image_analysis", methods=['POST'])
def do_image_analysis():
    file = request.files['image']
    imageData = "No Image Provided"
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("Received file: {}".format(filename))
            image = os.path.join(os.path.curdir,app.config['UPLOAD_FOLDER'], filename)
            print("Saving file: {}".format(filename))
            file.save(image)
            print("Processing file: {}".format(filename))
            data = detect_labels_local_file(image)
            imageData = ImageEntity(data)
            os.remove(image)
    return str(imageData)


@app.route("/text_summary")
def show_text_summary():
    return render_template("text_summary.html")

@app.route("/ajax/text_summary", methods=['POST'])
def do_text_summary():
    file = request.files['text']
    print(request.files)
    textData = "No Article Provided"
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("Received file: {}".format(filename))
            textFile = os.path.join(os.path.curdir,app.config['UPLOAD_FOLDER'], filename)
            print("Saving file: {}".format(filename))
            file.save(textFile)
            print("Processing file: {}".format(filename))
            textData = generate_summary(textFile, False, 2)
            os.remove(textFile)
    return str(textData)


if __name__ == '__main__':
    app.run(debug=True)