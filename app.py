from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# set database and collection names
database_name = 'usersdb'
collection_name = 'Info'

# set up database connection
app.config['MONGO_URI'] = f'mongodb://localhost/{database_name}'
mongo = PyMongo(app)

class User(Resource):

    # GET /users Endpoint
    def get(self, id=None):
        try:
            output = []
            if id:
                user = mongo.db[collection_name].find_one({'id':int(id)})
                if user:
                    output.append({'id': user['id'], 'name': user['name'], 'email': user['email'], 'password': user['password']})
                else:
                    output = "User not found!"
            else:
                users = mongo.db[collection_name].find()
                for user in users:
                    output.append({'id': user['id'], 'name': user['name'], 'email': user['email'], 'password': user['password']})
        except Exception as e:
            output = f"Some error has occurred: {e}"
        return jsonify({'result': output})


    # POST /users Endpoint - Creates a new user with the specified data.
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int, required=True)
            parser.add_argument('name', type=str, required=True)
            parser.add_argument('email', type=str, required=True)
            parser.add_argument('password', type=str, required=True)
            args = parser.parse_args()
            id = args['id']
            name = args['name']
            email = args['email']
            password = args['password']
            user = mongo.db[collection_name].find_one({'id': int(id)})
            if user:
                output = "User already exists"
            else:
                mongo.db[collection_name].insert_one({'id': id, 'name': name, 'email': email, 'password': password})
                output = "User added successfully"
        except Exception as e:
            output = f"Some error has occurred: {e}"
        return jsonify({'result': output})


    # PUT /users/<id> - Updates the user with the specified ID with the new data
    def put(self, id):
        try:
            user = mongo.db[collection_name].find_one({'id': int(id)})
            if user:
                parser = reqparse.RequestParser()
                parser.add_argument('name', type=str, location='json')
                parser.add_argument('email', type=str, location='json')
                parser.add_argument('password', type=str, location='json')
                args = parser.parse_args()
                update_dict = {}
                if args['name'] is not None:
                    update_dict['name'] = args['name']
                if args['email'] is not None:
                    update_dict['email'] = args['email']
                if args['password'] is not None:
                    update_dict['password'] = args['password']
                if update_dict:
                    mongo.db[collection_name].update_one(
                        {'id': id},
                        {'$set': update_dict}
                    )
                    output = "User updated successfully"
                else:
                    output = "No fields provided for update"
            else:
                output = "User not found!"
        except Exception as e:
            output = f"Some error has occurred: {e}"
        return jsonify({'result': output})


    # DELETE /users/<id> - Deletes the user with the specified ID
    def delete(self, id):
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

api.add_resource(User, '/users', endpoint='users')
api.add_resource(User, '/users/<int:id>', endpoint='user')

if __name__ == '__main__':
    app.run(debug=True)
