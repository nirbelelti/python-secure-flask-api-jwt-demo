from services.user_service import UserService
class UserFacade:
    def __init__(self):
        pass

    def get_index(self):
        return "Hello, World!"

    def create_user(self):
        return UserService.create(self)

    def get_user_by_id(self, id):
        return "not implemented yet"

    def update_user(self):
        return "not implemented yet"

    def delete_user(self):
        return "not implemented yet"
