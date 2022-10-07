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
        message = request.data.decode()
        if message == "listen":
            listener = Recognizer()
            audio_engine = SoftwareInteligenzaArtificiale()
            engine = pyttsx3.init()
            
            engine.say('      I am listening')
            engine.runAndWait()
            audio_engine.start_listening(listener, engine)
        else:
            audio_engine.run_context(request.data.decode())

    return render_template('silent_sofia.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
