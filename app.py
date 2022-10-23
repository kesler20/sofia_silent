import os
from Context.speaker import SoftwareInteligenzaArtificiale
from flask import redirect, url_for, render_template, request, session, send_from_directory, flash
import os
from datetime import timedelta
from flask import Flask, redirect, url_for, render_template, request, session, send_from_directory, flash
import os
from os import path as ps
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

ROOT_DIR = os.path.dirname(os.getcwd())
app = Flask(
    __name__, 
    template_folder=ps.join(ROOT_DIR, 'sofia_silent', 'templates'),
    static_folder=ps.join(ROOT_DIR, 'sofia_silent', 'static')
)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'top secret!'
app.secret_key = 'password'
app.permanent_session_lifetime = timedelta(minutes=50)
db = SQLAlchemy(app)

@app.route("/", methods=["POST", "GET"])
def render_home_page():
  if request.method == "POST":
    msg = request.data.decode()
    audio_engine = SoftwareInteligenzaArtificiale()
    audio_engine.run_context(msg)

    return { "response" :"okay"}

#----------------------------------- COMMAND TO START-----------------------------------------------
if __name__ == '__main__':
    os.system(
        'start http://sofiasilentui-20221007004808-hostingbucket-dev.s3-website.eu-west-2.amazonaws.com/')
    app.run(debug=True, port=5500)
     
    
    