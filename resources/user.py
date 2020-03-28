from flask_restful import Resource, reqparse
from models.user import UserModel
from db import db

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)


    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'That username already exists'}, 400
       
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created succesfully'}, 201

    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}
