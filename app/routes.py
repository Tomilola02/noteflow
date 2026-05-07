from flask import Blueprint, request, flash, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash
from .models import update_user, update_password, remove_user

main = Blueprint('main', __name__)

# _ _ _ _ HOME _ _ _ _
@main.route("/")
def home():
	return render_template("index.html")

# _ _ _ _ DASHBOARD _ _ _ _
@main.route("/dashboard")
def dashboard():
	if 'id' not in session:
		return redirect(url_for("auth.login"))

	return render_template("dashboard.html", name=session['user'])
	
# _ _ _ _ PROFILE _ _ _ _
@main.route("/profile")
def profile():
	if 'id' not in session:
		return redirect(url_for("auth.login"))

	return render_template("profile.html", user=session['user'], id=session['id'])
	
# _ _ _ _ UPDATE _ _ _ _ 
@main.route("/edit-profile", methods=['POST', 'GET'])
def edit_profile():
	if 'id' not in session:
		return redirect(url_for("auth.login"))
	
	return render_template("edit_profile.html", user=session['user'])

# _ _ _ _ UPDATE USERNAME _ _ _ _ 
@main.route("/edit-username", methods=['POST', 'GET'])
def edit_username():
	if 'id' not in session:
		return redirect(url_for("auth.login"))

	if request.method == 'POST':
		new_username = request.form.get('username')
		
		if not new_username:
			flash("New Username Required")
			return redirect(url_for("main.edit_username"))
			
		id = session['id']
		
		updated_username = update_user(id, new_username)
		
		if not updated_username:
			flash("Username Already Exists")
			return redirect(url_for("main.edit_username"))
		flash("Edited Successfully!")
		session['user'] = new_username
		return redirect(url_for("main.edit_profile"))
	return render_template("edit_username.html")

# _ _ _ _ UPDATE PASSWORD _ _ _ _ 
@main.route("/edit-password", methods=['POST', 'GET'])
def edit_password():
	if 'id' not in session:
		return redirect(url_for("auth.login"))

	if request.method == 'POST':
		new_password = request.form.get('password')
		
		if not new_password:
			flash("New Password Required")
			return redirect(url_for("main.edit_password"))
		
		id = session['id']
		
		update_password(id, new_password)
		flash("Edited Successfully!")
		return redirect(url_for("main.edit_profile"))

	return render_template("edit_password.html")
	
# _ _ _ _ DELETE PROFILE _ _ _ _
@main.route("/delete-profile", methods=["POST"])
def delete_profile():
    if 'id' not in session:
        return redirect(url_for("auth.login"))

    user_id = session['id']

    remove_user(user_id)

    session.clear()
    flash("Account deleted successfully")
    return redirect(url_for("main.home"))
	