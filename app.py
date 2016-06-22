from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, Response

from werkzeug.security import generate_password_hash, check_password_hash

from pymongo import MongoClient

from bson.objectid import ObjectId

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


@app.route('/ajax/keys.json')
def get_all_keys():
	return Response("{\"keys\":" + model.getKeys() + "}", mimetype="application/json")


@app.route("/add", methods=["GET", "POST"])
def add_unknown_item():
	if request.method == "POST":
		#model.insertItem(model.handlePOST(request.form))
		data = model.handlePOST(request.form)
		data["picture"] = "/image/" + str(model.fs.put(request.files['picture'], content_type=request.files["picture"].content_type))


		model.insertItem(data)
		#return str(data)

		#f = request.files['picture']
		#return str(request.files["picture"].read())

		return redirect(url_for("show_object_for_key", identifer=request.form["key"]))
	else:
		return render_template("create.html", identifer="")


@app.route('/add/<identifer>')
def insert_item(identifer):
	#return "adding " + str(identifer)
	return render_template("create.html", identifer=identifer)

@app.route("/")
def home():
	return render_template("home.html")


@app.route("/print/<identifer>")
def generate_label(identifer):
	return render_template("label.txt", info=model.infoForItem(identifer))

# print label command to implement - curl 192.168.99.100/print/test > /dev/tcp/10.0.0.51/2501


@app.route('/image/<identifer>')
def get_upload(identifer):
	return Response(model.fs.get(ObjectId(identifer)).read(), content_type=model.fs.get(ObjectId(identifer)).content_type)
	#return str(model.fs.get(ObjectId(identifer)).content_type)
	#return "get " + identifer


@app.route('/uploads', methods=['POST'])
def save_upload():
	return str(model.fs.put(request.files['picture'], content_type=request.files["picture"].content_type))


if __name__ == "__main__":
    app.run(debug=True)
