from flask import Flask, request


app = Flask(__name__)

@app.route('/users', methods=['GET'])
def index():
    return User.get_index(request)

@app.route('/user', methods=['GET'])
def get_user():
    return

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

