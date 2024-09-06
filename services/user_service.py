from flask import Flask, request, jsonify, g
from models.user import User, db


def validate_request(request_data):
    if 'username' not in request_data or 'password' not in request_data:
        return jsonify({'error': 'Missing username or password'}), 400
    elif len(request_data['password']) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long'}), 400
    elif len(request_data['username']) < 4:
        return jsonify({'error': 'Username must be at least 4 characters long'}), 400
    elif User.query.filter_by(username=request_data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    else:
        return True


class UserService:

    def index(self):
        return "Hello, World!"

    def create(self):
        request_data = self.get_json()
        valid_request = validate_request(request_data)
        if not valid_request:
            return valid_request
        else:
            new_user = User(username=request_data['username'])
            password = request_data['password']
            new_user.hash_and_salt_password(password)

            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201

    @staticmethod
    def get_user(user_id):
        return User.query.get(user_id)

    def update(self):
        user = g.current_user
        if not user:
            return jsonify({'error': 'User not found'}), 404
        else:
            request_data = self.get_json()
            if 'username' in request_data:
                user.username = request_data['username']
            if 'password' in request_data:
                user.hash_and_salt_password(str(request_data['password']))
            db.session.commit()
            return jsonify({'message': 'User updated successfully'}), 200

    def delete(self):
        return "not implemented yet"
