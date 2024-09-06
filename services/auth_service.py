import hashlib
import os
import uuid
import jwt
import redis

from flask import jsonify
from models.user import User
import datetime

jwt_key = os.environ.get('ENV_JWT_KEY', 'default_jwt_secret_key')


def encode_jwt_token(payload):
    token = jwt.encode(payload, jwt_key, algorithm='HS256')
    return token


def decode_jwt(token):
    try:
        decoded_payload = jwt.decode(token, jwt_key, algorithms=['HS256'])
        print("Decoded payload:", decoded_payload)
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
    except jwt.InvalidTokenError:
        print("Invalid token.")

    return None


class AuthService:
    def __init__(self):
        self.jwt_key = jwt_key
        self.jwt_algorithm = 'HS256'
        self.redis_host = os.environ.get('REDIS_HOST', 'localhost')
        self.redis_port = os.environ.get('REDIS_PORT', 6379)
        self.redis = redis.Redis(host=self.redis_host, port=self.redis_port, db=0)

    def authenticate_user(self, request):
        request_data = request.get_json()
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
            self.redis.setex(payload['jti'], int(payload['exp'].timestamp()), 'active')
            return jsonify({'access_token': token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    def validate_jwt(self, token):

        try:
            decoded_payload = decode_jwt(token)
            if not decoded_payload or 'jti' not in decoded_payload:
                return None
            jti = decoded_payload['jti']
            if self.redis.get(jti) is None:
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

    def renew_token(self):
        token = encode_jwt_token(self)
        self.redis.setex(self['jti'], int(self['exp'].timestamp()), 'active')
        return jsonify({'access_token': token}), 200

    def revoke_token(self):
        self.redis.delete(self)
        return jsonify({'message': 'Token has been revoked'}), 200
