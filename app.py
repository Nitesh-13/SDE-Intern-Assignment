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
    users = mongo.db[collection_name].find()
    output = []
    for user in users:
        output.append({'id': user['id'], 'name': user['name'], 'email': user['email'], 'password': user['password']})
    return jsonify({'result': output})






# GET /users/<id> Endpoint - Returns the user with the specified ID.
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db[collection_name].find({'id': int(id)}).limit(1)
    if user:
        output = {'id': user[0]['id'], 'name': user[0]['name'], 'email': user[0]['email'], 'password': user[0]['password']}
    else:
        output = "No such user"
    return jsonify({'result': output})






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
    app.run(debug=True)