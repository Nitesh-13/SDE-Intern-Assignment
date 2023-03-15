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



api.add_resource(User, '/users', endpoint='users')


# Start the Flask Application
if __name__ == '__main__':
    app.run(debug=True,port=5000)