import datetime
import uuid

from flask import request

from services.auth_service import AuthService

auth_service = AuthService()


class AuthFacade:

    def __init__(self):
        self.auth_service = auth_service

    def login(self):
        return auth_service.authenticate_user(request)

    def validate_token(self):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            decoded_payload = auth_service.validate_jwt(token)
            if decoded_payload:
                new_payload = {
                    'user_id': decoded_payload['user_id'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                    'jti': str(uuid.uuid4())
                }
                new_token = auth_service.renew_token(new_payload)
                return new_token
            else:
                return {'error': 'Token is invalid or has expired'}, 401
        else:
            return {'error': 'Authorization header missing or invalid'}, 401

    def logout(self):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            decoded_payload = self.auth_service.validate_jwt(token)
            if decoded_payload:
                self.auth_service.revoke_token(decoded_payload['jti'])
                return {'message': 'Token has been revoked'}, 200
            else:
                return {'error': 'Token is invalid or has expired'}, 401
        else:
            return {'error': 'Authorization header missing or invalid'}, 401
