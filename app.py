import os
from Database.flask_database import app
from flask import render_template, request, redirect
from Context.speaker import SoftwareInteligenzaArtificiale
from speech_recognition import Recognizer
import pyttsx3


@app.route('/', methods=["GET", "POST"])
def home():
    audio_engine = SoftwareInteligenzaArtificiale()
    if request.method == 'POST':
        audio_engine.run_context(request.form["command"])
    return render_template('silent_sofia.html')


@app.route('/listening')
def listen():
    listener = Recognizer()
    audio_engine = SoftwareInteligenzaArtificiale()
    engine = pyttsx3.init()
    
    engine.say('      I am listening')
    engine.runAndWait()
    audio_engine.start_listening(listener, engine)
    return redirect('/')


if __name__ == '__main__':
    os.system("start http://localhost:5000")
    app.run(port=5000, debug=True)


# TODO:  put all the configuration files in the config_file.py
# TODO: create a virtual environment where you can get all the files
# TODO: add tasks from the complete system list https://www.taskade.com/d/FUZpsyou3tdrE98R
# TODO: in order to make your software run on other computers it should be more directory independent
# TODO: set a config file where you specify all there major directories
# TODO: create react app
# TODO: start development -> launches a development environment
