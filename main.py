import os
from flask import Flask, redirect, render_template,request
# from moviepy.editor import *
import moviepy.editor as mp
import time
import azure.cognitiveservices.speech as speechsdk
# from pydub import AudioSegment
from flask_cors import CORS
from urllib3 import Retry



app = Flask(__name__)

app.config["VIDEO_FOLDER"] = "static/Videos"

CORS(app)

# @app.route('/')
# def index():
#     return render_template("main.html")

@app.route('/',methods = ['GET','POST'])
def authenticate():
    return render_template("login.html")

@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'midhunchakkaravarthybaz@gmail.com' and password == 'Midhun@22':
            return render_template("main.html")
        else:
            return render_template("login.html")


@app.route('/signup',methods = ['GET','POST'])
def signup():
    return render_template("main.html")

@app.route('/home', methods = ['POST','GET'])
def getvideo():
    if request.method == 'GET':
        # args = request.args
        # filepath = args.get('path')

        
        
        # videoclip = VideoFileClip("demo.mp4")
        # audioclip = videoclip.audio
        return render_template('main.html')
        # return str.join(getTranscript())
    if request.method == 'POST':
        if request.files:
            file_data = request.files['file']

            filename = "video.mp4"
            basedir = os.path.abspath(os.path.dirname(__file__))
            file_data.save(os.path.join(basedir, filename))

            print(file_data)


            my_clip = mp.VideoFileClip(os.path.join(basedir, filename))
            my_clip.audio.write_audiofile(os.path.join(basedir, "demo.wav"))
            str = ''
            # return render_template('main.html',transcript = str.join(getTranscript()))
            # return str.join(getTranscript())
            # return redirect('/home',transcript=str.join(getTranscript()))
            return printtrans(str.join(getTranscript()))


def printtrans(transcript):
    return render_template('main.html',transcript=transcript)


def getTranscript():
    speech_config = speechsdk.SpeechConfig(subscription="e1318f76770c4872a1dead52a5223fdb", region="centralindia")
    speech_config.speech_recognition_language="en-US"

    # audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    audio_config = speechsdk.audio.AudioConfig(filename="demo.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
  
    all_results = []
    def handle_final_result(evt):
        all_results.append(evt.result.text)


    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    speech_recognizer.recognized.connect(handle_final_result) 
    
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)
    
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    print("Printing all results:")
    return all_results


@app.route('/history')
def history():
    return render_template('History.html')


@app.route('/logout')
def logout():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)


