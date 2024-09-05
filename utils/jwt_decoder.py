from functools import wraps
from flask import Flask, request, jsonify

from services.auth_service import AuthService as AuthService
from services.user_service import UserService as UserService

auth_service = AuthService()
user_service = UserService()


def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            print("Token is present condition")
        if not token:
            print("Token is missing condition")
            return jsonify({"message": "Token is missing"}), 401
        print("decorated function wwxswkzzkksaxs :")
        valid_token = auth_service.validate_jwt(token)
        if not valid_token:
            return jsonify({"message": "Invalid or expired token"}), 401
        return valid_token
    return decorated_function

