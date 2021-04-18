from flask_restful import Resource, reqparse
from models import UserModel, ClientModel
from passlib.hash import pbkdf2_sha256 as sha256

from flask_jwt_extended import (create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt)

# Auth APIs
class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        parser.add_argument('name', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {'message': 'User {} already exists'.format(data['email'])}, 409

        new_user = UserModel(
            name = data['name'],
            email = data['email'],
            password = UserModel.generate_hash(data['password'])
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['email'])
            return {
                'message': 'User {} was created'.format(data['email']),
                'access_token': access_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()
        current_user = UserModel.find_by_email(data['email'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['email'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['email'])
            return {
                'message': 'Succesfully logged in as {}'.format(current_user.email),
                'access_token': access_token
                }
        else:
            return {'message': 'Wrong credentials'}, 401

# User Actions
class GetClients(Resource):
    @jwt_required()
    def get(self):
        worker_email = get_jwt_identity()
        return ClientModel.return_my(worker_email)

class AddClient(Resource):

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_email', help = 'This field cannot be blank', required = True)
        parser.add_argument('client_phone_no', help = 'This field cannot be blank', required = True)
        parser.add_argument('client_name', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()
        worker_email = get_jwt_identity()
        print(worker_email)


        if ClientModel.find_by_email(data['client_email'], worker_email):
           return {'message': 'Client {} already exists'.format(data['client_email'])}

        new_client = ClientModel(
            client_name = data['client_name'],
            client_email = data['client_email'],
            client_phone_no = data['client_phone_no'],
            worker_email = worker_email
        )
        new_client.save_to_db()
        return {
          'message': 'Success'
        }

# Profile
class GetProfile(Resource):
    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        return UserModel.find_by_email(email)

class UpdateProfile(Resource):

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        parser.add_argument('name', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()
        email = get_jwt_identity()
        print(email)
        try:
            UserModel.update_details(data['name'], email, sha256.hash(data['password']))
            return {
              'message' : 'Success'
            }
        except:
            return {'message': 'Error'}, 400

# Miscellaneous
class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

class AllClients(Resource):
    def get(self):
        return ClientModel.return_all()

class SecretResource(Resource):
    @jwt_required()
    def get(self):
        return {
            'answer': 42
        }
