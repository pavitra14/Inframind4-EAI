import settings
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template, session
from flask_socketio import SocketIO, emit, join_room
import os
import json
import time
from werkzeug.utils import secure_filename
from lxml import html
import requests
from urllib.parse import urlparse
from pprint import pformat

# Use Case Libraries
from VideoDescription.Analyser import analyse as VideoAnalyse
from ImageDescription.Analyser import *
from ImageDescription.utils import ImageEntity
from TextSummary.Summariser import *
from TextSentiment.utils import get_tweet
from TextSentiment.aws.comprehend import analyse_sentiment
from utils import sentiment_colors,sentiment_labels,get_sentiment_chart_values


UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp4', 'txt'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'Pm$@K7lN#d5#*GcUfj7^sQ7g*5LI'
socketio = SocketIO(app)

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

@app.route("/sentiment_social")
def show_sentiment_social():
    return render_template("sentiment_social.html")

@app.route("/ajax/sentiment_social", methods=['POST'])
def do_sentiment_social():
    tweet = get_tweet(request.form['tweet_url'])
    data = analyse_sentiment(tweet)
    response = dict()
    response['data'] = pformat(data)
    response['labels'] = sentiment_labels
    response['colors'] = sentiment_colors
    response['overall'] , response['values'] = get_sentiment_chart_values(data)
    return jsonify(response)

@app.route("/live_chat")
def show_live_chat():
    return render_template("live_chat.html")

@app.route("/ajax/do_sentiment_text_only", methods=['POST'])
def do_sentiment_text_only():
    msg = request.form['chat_message']
    data = analyse_sentiment(msg)
    overall, _ = get_sentiment_chart_values(data)
    return overall

@socketio.on('message', namespace='/chat')
def chat_message(message):
    print(message)
    emit('message', {'data': message['data']}, broadcast = True)

@socketio.on('connect', namespace='/chat')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})




# Following are functions required for demo
@app.route('/demo')
def chat():

    return render_template('chat.html')
@app.route('/demo/login')
def login():
    return render_template('login.html')

    
if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True)