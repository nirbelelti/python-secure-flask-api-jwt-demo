from flask import Flask, request, g
from facades.user_facade import UserFacade as User
from facades.auth_facade import AuthFacade as Auth
from models.user import db
from utils.jwt_decoder import jwt_required, get_current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

user_facade = User()
auth_facade = Auth()
@app.route('/user', methods=['POST'])
def create():
    return user_facade.create_user(request)


@app.route('/user', methods=['GET'])
@jwt_required
def get_user():
    return user_facade.get_user_by_id()


@app.route('/user', methods=['PUT'])
@jwt_required
@get_current_user
def update():
    return user_facade.update_user(request)


@app.route('/user', methods=['DELETE'])
@jwt_required
@get_current_user
def delete():
    return user_facade.delete_user()


@app.route('/authenticate_user', methods=['POST'])
def authenticate_user():
    return auth_facade.login(request)


@app.route('/validate_token', methods=['POST'])
def validate_token():
    return auth_facade.validate_token(request)


@app.route('/logout', methods=['POST'])
def logout():
    return auth_facade.logout(request)


if __name__ == '__main__':
    app.run(debug=True)
