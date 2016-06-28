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
	if not model.itemExists(identifer):
		return redirect(url_for("insert_item", identifer=identifer))

	return render_template("id.html", info=model.infoForItem(identifer))


@app.route('/ajax/keys.json')
def get_all_keys():
	return Response("{\"keys\":" + model.getKeys() + "}", mimetype="application/json")


@app.route("/add", methods=["GET", "POST"])
def add_unknown_item():
	if request.method == "POST":
		data = model.handlePOST(request.form)
		data["picture"] = "/image/" + str(model.fs.put(request.files['picture'], content_type=request.files["picture"].content_type))

		model.insertItem(data)

		return redirect(url_for("show_object_for_key", identifer=request.form["key"]))
	else:
		return render_template("create.html", identifer="")


@app.route('/add/<identifer>')
def insert_item(identifer):
	if model.itemExists(identifer):
		return redirect(url_for("show_object_for_key", identifer=identifer))
	else:
		return render_template("create.html", identifer=identifer)


@app.route("/")
def home():
	return render_template("home.html")


@app.route("/print")
def print_page():
	return render_template("print.html")


@app.route("/print/<identifer>")
def generate_label(identifer):
	return render_template("label.txt", info=model.infoForItem(identifer))

# print label command to implement - curl 192.168.99.100/print/test > /dev/tcp/10.0.0.51/2501


@app.route('/image/<identifer>')
def get_upload(identifer):
	return Response(model.fs.get(ObjectId(identifer)).read(), content_type=model.fs.get(ObjectId(identifer)).content_type)


@app.route('/uploads', methods=['POST'])
def save_upload():
	return str(model.fs.put(request.files['picture'], content_type=request.files["picture"].content_type))


@app.route("/search")
def search_items():
	return render_template("search.html")


@app.route("/list")
def list_items():
	return render_template("list.html", items=model.getAllItems())


@app.route("/edit/<identifier>", methods=["GET", "POST"])
def edit_item(identifier): 
	if request.method == "POST":
		data = model.handlePOST(request.form)
		model.updateItem(identifier, data)
		return redirect(url_for("show_object_for_key", identifer=identifier))
	else:
		return render_template("edit.html", info=model.infoForItem(identifier))



if __name__ == "__main__":
    app.run(debug=True)












