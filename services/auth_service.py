import hashlib
import os
import uuid
import jwt
import redis

from flask import jsonify
from models.user import User
import datetime

jwt_key = os.environ.get('ENV_JWT_KEY', 'default_jwt_secret_key')  # Secret key for token generation
jwt_algorithm = 'HS256'
redis_host = os.environ.get('REDIS_HOST', 'localhost')  # Redis host address
redis_port = os.environ.get('REDIS_PORT', 6379)  # Redis port

redis = redis.Redis(host=redis_host, port=redis_port, db=0)


def encode_jwt_token(payload):
    secret_key = jwt_key
    algorithm = 'HS256'
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


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
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                'jti': str(uuid.uuid4())
            }
            token = encode_jwt_token(payload)
            redis.setex(payload['jti'], int(payload['exp'].timestamp()), 'active')
            return jsonify({'access_token': token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    def validate_jwt(self):
        try:
            decoded_payload = jwt.decode(self, jwt_key, algorithms=[jwt_algorithm])
            jti = decoded_payload['jti']
            if redis.get(jti) is None:
                print("Token has been revoked. Please log in again.")
                return None
            redis.delete(jti)
            print("Token is valid")
            return decoded_payload
        except jwt.ExpiredSignatureError:
            print("Token has expired. Please log in again.")
        except jwt.InvalidTokenError:
            print("Invalid token. Access denied.")
        return None