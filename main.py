from flask import Flask, send_from_directory, request, flash, redirect
from flask import render_template
from pymongo import MongoClient
app = Flask(__name__)
myclient = MongoClient('localhost',27017)
mydb = myclient["mydb"]
mydb = myclient["lab4"]
mycol = mydb["accounts"]
app.secret_key = 'this is secret key'
# logins = {'admin': 'admin'}
session = False

@app.route('/', methods = ['GET','POST'])
def login():
	error = None
	global session
	if request.method == "POST":
		doc = mycol.find_one({"username": request.form['username']})
		try:
			if request.form['password'] == doc["password"]: #dung tk mk
				session = True
				return redirect ('cabinet')
			error = "Invalid credentials"
		except:
			error = "Invalid credentials"
	return render_template('lab3.html', error = error)

@app.route('/cabinet')
def cabinet():
	global session
	if session == True:
		return render_template('lab1.html')
	else: 
		return redirect ('/')

@app.route('/register', methods = ['GET','POST'])
def register():
	global session
	if request.method == "GET":
		return render_template('register.html')
	else:
		try:
			doc = mycol.find_one({"username": request.form['username']})
			if request.form['username'] in doc["username"]:
				flash("This username is already in use. Please try another one")
				return render_template('register.html')
		except:
			mycol.insert_one({"username": request.form['username'], "password": request.form['password']})
			session = True
			return redirect ('cabinet')
			
@app.route('/logout')
def logout():
	global session
	session = False
	return redirect ('/')

@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory('img', filename)

if __name__ == "__main__":
	app.run(host='localhost', port=5000, debug=True)