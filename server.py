from flask import Flask, request, redirect, render_template, session, flash
import re, md5
from mysqlconnection import MySQLConnector
NAME_REGEX = re.compile(r'^[a-zA-Z]*$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASS_REGEX = re.compile(r'^[a-zA-Z0-9]*$')
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]*$')
app = Flask(__name__)
app.secret_key = 'SecretStuff'
mysql = MySQLConnector(app, 'wall')

@app.route('/')
def index():
	things = mysql.query_db('SELECT email FROM users WHERE email = "maxrose93@hotmail.com";')
	if 'first_name' not in session and 'last_name' not in session and 'email' not in session and 'username' not in session:
		return render_template('index.html', stuff = len(things) )

	elif 'first_name' not in session and 'last_name' not in session and 'username' not in session:
		return render_template('index.html', mail=session['email'], stuff = len(things) )

	elif 'first_name' not in session and 'email' not in session and 'username' not in session:
		return render_template('index.html', last=session['last_name'], stuff = len(things))

	elif 'last_name' not in session and 'email' not in session and 'username' not in session:
		return render_template('index.html', first=session['first_name'], stuff = len(things))
	
	elif 'first_name' not in session and 'last_name' not in session and 'email' not in session:
		return render_template('index.html', user=session['username'], stuff = len(things))

	elif 'first_name' not in session and 'last_name' not in session:
		return render_template('index.html', mail=session['email'], user=session['username'], stuff = len(things))

	elif 'first_name' not in session and 'email' not in session:
		return render_template('index.html', last=session['last_name'], user=session['username'], stuff = len(things))

	elif 'last_name' not in session and 'email' not in session:
		return render_template('index.html', first=session['first_name'], user=session['username'], stuff = len(things))

	elif 'first_name' not in session and 'username' not in session:
		render_template('index.html', last=session['last_name'], mail=session['email'], stuff = len(things))

	elif 'last_name' not in session and 'username' not in session:
		return render_template('index.html', first=session['first_name'], mail=session['email'], stuff = len(things))

	elif 'email' not in session and 'username' not in session:
		return render_template('index.html', first=session['first_name'], last=session['last_name'], stuff = len(things))

	elif 'first_name' not in session:
		render_template('index.html', last=session['last_name'], mail=session['email'], user=session['username'], stuff = len(things))

	elif 'last_name' not in session:
		return render_template('index.html', first=session['first_name'], mail=session['email'], user=session['username'], stuff = len(things))

	elif 'email' not in session:
		return render_template('index.html', first=session['first_name'], last=session['last_name'], user=session['username'], stuff = len(things))

	elif 'username' not in session:
		return render_template('index.html', first=session['first_name'], last=session['last_name'], mail=session['email'], stuff = len(things))

	else:
		return render_template('index.html', first=session['first_name'], last=session['last_name'], mail=session['email'], user=session['username'], stuff = len(things))
	# return render_template('index.html')

@app.route('/reg', methods=['POST'])
def registration():
	count = 0
	session.clear()
	

	if len(request.form['first_name']) < 1:
		flash("first name cannot be empty!")
	elif not NAME_REGEX.match(request.form['first_name']):
		flash("Names only have letters")
	else:
		session['first_name'] = request.form['first_name']
		count += 1

	if len(request.form['last_name']) < 1:
		flash("last name cannot be empty!")
	elif not NAME_REGEX.match(request.form['last_name']):
		flash("Names only have letters")
	else:
		session['last_name'] = request.form['last_name']
		count += 1

	check = {"email": request.form['email']}
	emailcheck = mysql.query_db('SELECT email FROM users WHERE email = ":email";', check)
	print emailcheck
	print len(emailcheck)
	if len(request.form['email']) < 1:
		flash("Email cannot be blank!")
	elif not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address!")
	elif len(emailcheck) > 0:
		# if emailcheck[0]['email']==request.form['email']:
		flash("email is already registered")
	else:
		session['email'] = request.form['email']
		count += 1

	# usercheck = mysql.query_db('SELECT username FROM users WHERE username = ":username";', values)

	if len(request.form['username']) < 3 or len(request.form['username']) > 11 :
		flash("Username must be 3 - 10 characters long!")
	elif not USERNAME_REGEX.match(request.form['username']):
		flash("Invalid username")
	# elif len(usercheck) >= 1:
	# 	flash("username already exists :(")
	else:
		session['username'] = request.form['username']
		count += 1

	if len(request.form['password']) < 8:
		flash("Password needs at least 8 characters!")
	elif request.form['password']!=request.form['pass_conf']:
		flash("Passwords do not match")
	else:
		password = md5.new(request.form['password']).hexdigest();
		count += 1

	if count == 5:
		values = {
		"first_name":request.form['first_name'],
		"last_name":request.form['last_name'],
		"password":password,
		"email":request.form['email'],
		"username": request.form['username']
	}
		query='INSERT INTO users (first_name, last_name, password, email, username, created_at, updated_at) VALUES(:first_name,:last_name,:password,:email, :username, now(), now());'
		session.clear()
		mysql.query_db(query, values)
		flash("Thank you for successfully signing up!")
	return redirect('/')

@app.route('/login', methods=['POST'])
def login():

	values = {
	"password":request.form['password'],
	"username": request.form['username']
	}

	if len(request.form['password']) < 8:
		flash("Password cannot be empty")
	elif len(request.form['username']) < 3 or len(request.form['username']) > 11 :
		flash("Usernames are 3 - 10 characters long")
	elif mysql.query_db('SELECT DISTINCT * FROM users WHERE username = ":username" AND password = ":password";', values):
		session['username'] = request.form['username']
		session['password'] = request.form['password']
	else:
		
		session['username'] = request.form['username']


	if count == 5:
		query='INSERT INTO users (first_name, last_name, password, email, username, created_at, updated_at) VALUES(":first_name",":last_name",":password",":email", ":username", now(), now());'
		session.clear()
		mysql.query_db(query, values)
		flash("Thank you for Submitting your form!")

app.run(debug=True)