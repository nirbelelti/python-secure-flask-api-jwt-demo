from flask import Flask, request


app = Flask(__name__)

@app.route('/users', methods=['GET'])
def index():
    return
@app.route('/user', methods=['GET'])
def get_user():
    return

@app.route('/user', methods=['POST'])
def create():
    return

@app.route('/user', methods=['PUT'])
def update():
    return

@app.route('/user', methods=['DELETE'])
def delete():
    return

if __name__ == '__main__':

    app.run(debug=True)

