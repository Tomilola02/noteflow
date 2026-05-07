from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import create_user, verify_user
from werkzeug.security import generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		name = request.form.get("username")
		pword = request.form.get("password")
		if not name or not pword:
			flash("All fields are required!")
			return redirect(url_for("auth.login"))
		
		user = verify_user(name, pword)
		if user:
			user_id, username, password = user
			flash("Login Successful")
			session['id'] = user_id
			session['user'] = username
			return redirect(url_for("main.dashboard"))
		else:
			flash("Invalid Username or Password")
			return redirect(url_for("auth.login"))
	return render_template("login.html")
	
@auth.route("/register", methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		name = request.form.get("username")
		pword = request.form.get("password")
		
		if not name or not pword:
			flash("All fields are required!")
			return redirect(url_for("auth.register"))
		
		user = create_user(name, pword)
		
		if user:
			flash("Registered Successfully!")
			return redirect(url_for("auth.login"))
		else:
			flash("Username Already Exists")
			return redirect(url_for("auth.register"))
	return render_template("register.html")

@auth.route("/logout")
def logout():
	session.clear()
	flash("Logged out!")
	return redirect(url_for("auth.login"))