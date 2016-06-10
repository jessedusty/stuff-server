from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from werkzeug.security import generate_password_hash, check_password_hash

import logging
import uuid

from logging.handlers import RotatingFileHandler

app = Flask(__name__)
handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)



from datetime import datetime

app.secret_key = 'development key'

HOST_URL = "http://192.168.99.100/"

@app.route('/key/<identifer>')
def show_user_profile(identifer):
    # show the user profile for that user
	return render_template("id.html", identifer=identifer)

    #return 'User %s' % identifer

@app.route("/hello")
def hello():
	return render_template("id.html")

@app.route("/")
def home():
	return str("home")

if __name__ == "__main__":
    app.run()
