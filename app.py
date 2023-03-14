from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

# set database and collection names
database_name = 'usersdb'
collection_name = 'Info'

# set up database connection
app.config['MONGO_URI'] = f'mongodb://localhost/{database_name}'
mongo = PyMongo(app)





# GET /users Endpoint - Returns a list of all users.
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = mongo.db[collection_name].find()
        output = []
        for user in users:
            output.append({'id': user['id'], 'name': user['name'], 'email': user['email'], 'password': user['password']})
    except Exception as e:
        output = f"Some error has occurred: {e}"
    return jsonify({'result': output})






# GET /users/<id> Endpoint - Returns the user with the specified ID.
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        user = mongo.db[collection_name].find_one({'id':int(id)})
        if user:
            output = {'id': user['id'], 'name': user['name'], 'email': user['email'], 'password': user['password']}
        else:
            output = "User not found!"
    except Exception as e:
        output = f"Some error has occurred: {e}"
    return jsonify({'result': output})




# POST /users Endpoint - Creates a new user with the specified data.
@app.route('/users', methods=['POST'])
def add_user():
    try:
        id = request.json['id']
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        user = mongo.db[collection_name].find_one({'id': int(id)})
        if user:
            output = "User already exists"
        else:
            mongo.db[collection_name].insert_one({'id': id, 'name': name, 'email': email, 'password': password})
            output = "User added successfully"
    except Exception as e:
        output = f"Some error has occurred: {e}"
    return jsonify({'result': output})





# PUT /users/<id> Endpoint - Updates the user with the specified ID with the new data.
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        user = mongo.db[collection_name].find_one({'id': int(id)})
        if user:
            name = request.json.get('name', user.get('name'))
            email = request.json.get('email', user.get('email'))
            password = request.json.get('password', user.get('password'))
            mongo.db[collection_name].update_one(
                {'id': id},
                {'$set': {'name': name, 'email': email, 'password': password}}
            )
            output = "User updated successfully"
        else:
            output = "User not found!"
    except Exception as e:
        output = f"Some error has occurred: {e}"
    return jsonify({'result': output})






# DELETE /users/<id> Endpoint - Deletes the user with the specified ID.
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = mongo.db[collection_name].find_one({'id': int(id)})
        if user:
            mongo.db[collection_name].delete_one({'id': int(id)})
            output = "User deleted successfully"
        else:
            output = "User not found!"
    except Exception as e:
        output = f"Some error has occurred: {e}"
    return jsonify({'result': output})




# Start the Flask Application
if __name__ == '__main__':
    app.run(debug=True)