from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from werkzeug.security import generate_password_hash, check_password_hash

import logging
import uuid

from logging.handlers import RotatingFileHandler

app = Flask(__name__)
handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

from pymongo import MongoClient
print("started mongo client")
client = MongoClient("mongodb://db")

from datetime import datetime

db = client.test

app.secret_key = 'development key'

HOST_URL = "http://192.168.99.100/"

@app.route("/hello")
def hello():
	result = db.resturants.insert_one({"name":"test"})
	return str(result)

	return "Hello World!"

@app.route("/login", methods=['GET', 'POST'])
def login():
	if 'logged_in' in session and session['logged_in'] == True:
		return redirect("/")

	if request.method == "POST":
		cursor = db.users.find({"email":request.form['username']})
		if cursor == None: return render_template("login.html", error="Wrong username or password")
		entry = cursor[0]
		if entry == None: return render_template("login.html", error="Wrong username or password")

		if check_password_hash(entry['password'], request.form['password']):
			session['logged_in'] = True
			session['email'] = request.form['username']
			flash('You were logged in')
			return redirect("/")
		else:
			return render_template("login.html", error="Wrong username or password")
		#return "username: " + request.form['username'] + " <br> password:" + request.form['password'] + "<br>"

	else:
		return render_template("login.html")


@app.route("/create_account", methods=['GET', 'POST'])
def create_account():

	if request.method == "POST":
		if request.form['password'] != request.form['cpassword']:
			return render_template("create_account.html", error="Passwords don't match")
		cursor = db.users.find({"email":request.form['username']})
		if cursor.count() > 0:
			return render_template("create_account.html", error="Email already taken")

		db.users.insert_one({"email":request.form['username'], "password":generate_password_hash(request.form['password'])})
		session['logged_in'] = True
		session['email'] = request.form['username']

		return redirect("/")

	else:
		return render_template("create_account.html")

@app.route("/logout")
def logout():
	session.pop('logged_in', None)
	session.pop('email', None)
	return redirect("/")

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
	if not session['logged_in']:
		return redirect("/login")

	if request.method == "GET":

		cursor = db.users.find({"email":session['email']})
		userinfo = cursor[0]

		return render_template("dashboard.html", thisUser=userinfo, HOST_URL=HOST_URL)
	else:

		return str(db.users.update({"email":session['email']}, {
				"$set": {
					"enabled-rec":request.form["enabled-rec"] ,
					"online-rec":request.form["online-rec"],
					"sms-rec":request.form["sms-rec"]
				}
		}, upsert=False))

		return "done"

@app.route('/usr/<username>')
def user_form(username, methods=['GET', 'POST']):
		cursor = db.users.find({"email":username})
		userinfo = cursor[0]

		if True:
			db.users.update(
				{ "email":username },
				{ "$push": { "suggestion": request.form["suggestion"] } }
				)

		return render_template("user_form.html", user=userinfo)

"""
@app.route('/usr/<username>/add')
def user_form_submit(username, method='GET'):
	return "hello world"
	if not 'suggestor' in session:
		session['suggestor'] = uuid.uuid4()

	db.users.findsession['suggestor']
	db.students.update(
		{ "email":username },
		{ "$push": { "suggestion": request.form["suggestion"] } }
	)

	infoString = request.form["suggestion"] + " added to " + username + "\'s suggestions"
	return render_template("user_form.html", user=userinfo, info=infoString)
"""


if __name__ == "__main__":

    app.run()
