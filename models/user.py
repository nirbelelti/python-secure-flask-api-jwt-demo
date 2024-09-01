from flask_sqlalchemy import SQLAlchemy
import hashlib
import os

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(64), nullable=False)

    def hash_and_salt_password(self, password):
        salt = os.urandom(32)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        self.password = salt + hashed_password
