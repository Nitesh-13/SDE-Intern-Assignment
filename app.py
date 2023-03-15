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
            if id:
                user = mongo.db[collection_name].find_one({'id':int(id)})
                if user:
                    output = {'id': user['id'], 'name': user['name'], 'email': user['email'], 'password': user['password']}
                else:
                    output = "User not found!"
            else:
                users = mongo.db[collection_name].find()
                output = []
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


api.add_resource(User, '/users', endpoint='users')


# Start the Flask Application
if __name__ == '__main__':
    app.run(debug=True,port=5000)