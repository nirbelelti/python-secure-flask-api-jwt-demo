import hashlib
from flask import jsonify
from models.user import User


class AuthService:
    def __init__(self):
        pass

    def authenticate_user(self):
        request_data = self.get_json()
        user = User.query.filter_by(username=request_data['username']).first()
        password = request_data['password']

        if not user:
            return jsonify({'error': 'Invalid credentials'}), 404

        # Extract the salt and the hashed password
        salt = user.password[:32]  # First 32 bytes are the salt
        stored_hash = user.password[32:]  # The rest is the hashed password

        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        if hashed_password == stored_hash:
            return jsonify({'access_token': 'here wil be implement a token'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
