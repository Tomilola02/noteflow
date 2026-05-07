from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import create_note, get_notes, get_note, update_note, delete_note_db

notes = Blueprint('notes', __name__)

# _ _ _ _ CREATE NOTE _ _ _ _ 
@notes.route("/create-note", methods=['POST', 'GET'])
def create_note_route():
	if 'id' not in session:
		return redirect(url_for("auth.login"))
	if request.method == 'POST':
		content = request.form.get("content")
		
		if not content:
			flash("Note can not be empty")
			return redirect(url_for("notes.create_note_route"))
		
		user_id = session["id"]
		create_note(user_id, content)
		flash("Note Added!")
		return redirect(url_for("notes.notes_r"))
	return render_template("notes/create_note.html")

# _ _ _ _ VIEW NOTES _ _ _ _
@notes.route("/notes")
def notes_r():
    if 'id' not in session:
        return redirect(url_for("auth.login"))

    user_notes = get_notes(session['id']) 
    return render_template("notes/notes.html", notes=user_notes)

# _ _ _ _ DELETE NOTE _ _ _ _
@notes.route("/delete-note/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    if 'id' not in session:
        return redirect(url_for("auth.login"))

    user_id = session['id']
    if delete_note_db(note_id, user_id): 
        flash("Note deleted")
    else:
        flash("Note not found")
    return redirect(url_for("notes.notes_r"))

# _ _ _ _ EDIT NOTE _ _ _ _
@notes.route("/edit-note/<int:note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    if 'id' not in session:
        return redirect(url_for("auth.login"))

    user_id = session['id']
    note = get_note(note_id, user_id) # MUST check user_id here

    if not note:
        flash("Note not found or you don't have access")
        return redirect(url_for("notes.notes_r"))

    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if not content:
            flash("Note cannot be empty")
            return render_template("notes/edit_note.html", note=note)

        update_note(note_id, user_id, content) # update_note should also use user_id
        flash("Note updated")
        return redirect(url_for("notes.notes_r"))

    return render_template("notes/edit_note.html", note=note)

