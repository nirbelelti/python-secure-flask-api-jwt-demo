from functools import wraps
from flask import g, request, jsonify

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
        valid_token = auth_service.validate_jwt(token)
        if not valid_token:
            return jsonify({"message": "Invalid or expired token"}), 401
        g.decoded_token = valid_token
        return f(*args, **kwargs)
    return decorated_function


def get_current_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = g.decoded_token.get('user_id')
        if user_id:
            user = user_service.get_user(user_id)
            if user:
                g.current_user = user
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': 'Invalid token payload'}), 401
    return decorated
