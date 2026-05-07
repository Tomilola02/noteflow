import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

#_ _ _ DATABASE _ _ _
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "storage.db")

def get_db():
	return sqlite3.connect(DB_PATH)
	
#_ _ _ CREATE TABLE _ _ _
def create_table():
	conn = get_db()
	cur = conn.cursor()
		
	cur.execute('''CREATE TABLE IF NOT EXISTS users(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT UNIQUE,
		password TEXT	
	)''')
	conn.commit()

#_ _ _ _ CREATE USER _ _ _ _ 
def create_user (username, password):
	conn = get_db()
	cur = conn.cursor()
	hashed = generate_password_hash(password)
	
	try:
		cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
		conn.commit()
		return True
	except sqlite3.IntegrityError:
		return False
	finally:
		conn.close()
		
#_ _ _ _ GET USER _ _ _ _ 
def get_user(username):
	conn = get_db()
	cur = conn.cursor()
	
	cur.execute('SELECT id, username, password FROM users WHERE username = ?', (username,))
	
	user = cur.fetchone()
	conn.close()
	
	return user
	
#_ _ _ _ VERIFY USER _ _ _ _
def verify_user (username, password):
	user = get_user(username)
	
	if not user:
		return None
		
	user_id, user_name, stored_password = user
	if check_password_hash(stored_password, password):
		return user
	return None
	
# _ _ _ _ UPDATE USER _ _:,_ _ 
def update_user(user_id, new_username):
	conn = get_db()
	cur = conn.cursor()
	
	try:
		cur.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
		conn.commit()
		return True
	except sqlite3.IntegrityError:
		return False
	finally:
		conn.close()
    
# _ _ _ _ UPDATE PASSWORD _ _ _ _
def update_password(user_id, new_password):
    conn = get_db()
    cur = conn.cursor()
    hashed = generate_password_hash(new_password)
    
    cur.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, user_id))
    conn.commit()
    conn.close()
    
# _ _ _ _ REMOVE USER _ _ _ _
def remove_user(user_id):
	conn = get_db()
	cur = conn.cursor()
    
	cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
	conn.commit()
	conn.close()

# _ _ _ _ CREATE NOTE TABLE _ _ _ _
def create_note_table():
	conn = get_db()
	cur = conn.cursor()
	
	cur.execute(""" CREATE TABLE IF NOT EXISTS notes(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		user_id INTEGER,
		content TEXT,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		FOREIGN KEY(user_id) REFERENCES users(id)
	)""")
	
	conn.commit()
	conn.close()
create_note_table()

# _ _ _ _ CREATE NOTE _ _ _ _
def create_note(user_id, content):
	conn = get_db()
	cur = conn.cursor()
	
	cur.execute("INSERT INTO notes (user_id, content) VALUES(?, ?)", (user_id, content))
	
	conn.commit()
	conn.close()
	
# _ _ _ _ GET NOTES _ _ _ _
def get_notes(user_id):
	conn = get_db()
	cur = conn.cursor()

	cur.execute(
		"SELECT id, content, created_at, updated_at FROM notes WHERE user_id = ?",
		(user_id,)
	)

	notes = cur.fetchall()
	conn.close()
	return notes
	
def get_note(note_id, user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, content, created_at, updated_at FROM notes WHERE id = ? AND user_id = ?",
        (note_id, user_id)
    )

    note = cur.fetchone()
    conn.close()
    return note
    
def update_note(note_id, user_id, content):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE notes SET content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?",
        (content, note_id, user_id)
    )

    conn.commit()
    conn.close()

def delete_note_db(note_id, user_id):
	conn = get_db()
	cur = conn.cursor()
    
	cur.execute(
		"DELETE FROM notes WHERE id =? AND user_id =?",
		(note_id, user_id)
	)
    
	conn.commit()
	conn.close()