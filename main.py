from flask import Flask, request
from facades.user_facade import UserFacade as User


app = Flask(__name__)

@app.route('/users', methods=['GET'])
def index():
    return User.get_index(request)

@app.route('/user', methods=['GET'])
def get_user():
    return User.get_user_by_id(request.args.get('id'))

@app.route('/user', methods=['POST'])
def create():
    return User.create_user()

@app.route('/user', methods=['PUT'])
def update():
    return User.update_user()

@app.route('/user', methods=['DELETE'])
def delete():
    return User.delete_user()

if __name__ == '__main__':

    app.run(debug=True)

