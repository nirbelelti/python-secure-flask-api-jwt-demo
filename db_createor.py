from main import app  # Import the app object from main.py
from models.user import db  # Import the db object from models.user

with app.app_context():  # Ensure the app context is set
    db.create_all()  # Create all tables
    print("Database created successfully!")