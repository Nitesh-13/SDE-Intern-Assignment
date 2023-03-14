from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

database_name = 'user'
mongo_port = "3049"

app = Flask(__name__)
app.config['MONGO_URI'] = f'mongodb://localhost:{mongo_port}/{database_name}'
mongo = PyMongo(app)





# GET /users Endpoint - Returns a list of all users.
@app.route('/users', methods=['GET'])
def get_all_users():
    print("Returns a list of all users.")






# GET /users/<id> Endpoint - Returns the user with the specified ID.
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print("Returns the user with the specified ID.")






# POST /users Endpoint - Creates a new user with the specified data.
@app.route('/users', methods=['POST'])
def add_user():
    print("Creates a new user with the specified data.")





# PUT /users/<id> Endpoint - Updates the user with the specified ID with the new data.
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    print("Updates the user with the specified ID with the new data.")





# DELETE /users/<id> Endpoint - Deletes the user with the specified ID.
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    print("Deletes the user with the specified ID.")



# Start the Flask Application
if __name__ == '__main__':
    app.run()