from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3)

jwt = JWTManager(app)
db = SQLAlchemy(app)

import models, resources

@app.before_first_request
def create_tables():
    db.create_all()

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response

@app.route('/')
def index():
  return jsonify({'message':'Hello World!'})

# Auth
api.add_resource(resources.UserRegistration, '/auth/register')
api.add_resource(resources.UserLogin, '/auth/login')

# User Actions
api.add_resource(resources.GetClients, '/user/clients') # Get Clients
api.add_resource(resources.AddClient, '/user/clients/add') # Add a Client

# Miscellaneous Admin APIs
api.add_resource(resources.AllUsers, '/admin/users')
api.add_resource(resources.AllClients, '/admin/clients')
api.add_resource(resources.SecretResource, '/secret')
