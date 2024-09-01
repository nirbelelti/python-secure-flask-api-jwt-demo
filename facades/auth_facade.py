from services.auth_service import AuthService


class AuthFacade:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def login(self):
        return AuthService.authenticate_user(self)
