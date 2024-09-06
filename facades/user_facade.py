from services.user_service import UserService
class UserFacade:
    def __init__(self):
        pass

    def get_index(self):
        return "Hello, World!"

    def create_user(self):
        return UserService.create(self)

    @staticmethod
    def get_user_by_id():
        user_id = g.decoded_token.get('user_id')
        user = UserService.get_user(user_id)
        if user:
            user_data = {
                'id': user.id,
                'username': user.username,
            }
            new_token = AuthService().renew_token(
                {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                 'jti': str(uuid.uuid4())})
            response = {
                'user': user_data,
                'token': new_token
            }
            return response
        else:
            return jsonify({'message': 'User not found'}), 404

    def update_user(self):
        UserService.update(self)
        new_token = AuthService().renew_token(
            {'user_id': g.current_user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
             'jti': str(uuid.uuid4())})
        response = {
            'message': "User updated successfully",
            'token': new_token
        }
        return jsonify(response), 200

    def delete_user(self):
        return "not implemented yet"
