from flask import Flask
import os
from datetime import datetime
from .models import create_table, create_note_table

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
	
	create_table()
	create_note_table()
	@app.template_filter('datetime')
	def format_datetime(value):
		try:
			dt = datetime.fromisoformat(value)
			return dt.strftime('%b %d, %Y at %I:%M %p')
		except:
			return value

	from .routes import main
	from .auth import auth
	from .notes import notes

	app.register_blueprint(main)
	app.register_blueprint(auth)
	app.register_blueprint(notes)

	return app