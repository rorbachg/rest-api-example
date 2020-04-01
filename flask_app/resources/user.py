from flask_restful import Resource, reqparse
from models.user import UserModel
from db import db
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required,
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required, 
    get_jwt_identity,
    get_raw_jwt)
from datetime import timedelta
from blacklist import BLACKLIST



_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True)
_user_parser.add_argument('password', type=str, required=True)

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'That username already exists'}, 400
       
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created succesfully'}, 201

    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}

class UserLogin(Resource):
    def post(self):
        """ get data from parser
            find user in database
            check password
            create access token
            create refresh token
            return them
        """
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True) #, expires_delta=timedelta(minutes=1))
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return {'message': 'Invalid credentials'}, 401

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)# , expires_delta=timedelta(minutes=1))
        return {'access_token': new_token}

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'User logged out'}
