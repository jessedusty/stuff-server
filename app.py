from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from werkzeug.security import generate_password_hash, check_password_hash



import logging
import uuid

from logging.handlers import RotatingFileHandler

import model

app = Flask(__name__)
handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)



from datetime import datetime

app.secret_key = 'development key'

HOST_URL = "http://192.168.99.100/"

@app.route('/key/<identifer>')
def show_object_for_key(identifer):
    # show the user profile for that user
	if not model.itemExists(identifer):
		return redirect(url_for("insert_item", identifer=identifer))

	return render_template("id.html", info=model.infoForItem(identifer))
    #return 'User %s' % identifer

@app.route("/add", methods=["GET", "POST"])
def add_unknown_item():
	if request.method == "POST":
		return "inserted data into database, would you like to print label?"
	else:
		return "new label dialog"

@app.route('/add/<identifer>')
def insert_item(identifer):
	#return "adding " + str(identifer)
	return render_template("create.html", identifer=identifer)

@app.route("/hello")
def hello():
	return render_template("id.html")

@app.route("/")
def home():
	return str("home")

@app.route("/print/<identifer>")
def generate_label(identifer):
	return render_template("label.txt", info=model.infoForItem(identifer))

# print label command to implement - curl 192.168.99.100/print/test > /dev/tcp/10.0.0.51/2501


if __name__ == "__main__":
    app.run()
