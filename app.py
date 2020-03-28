from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from models.user import UserModel
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

@app.before_first_request
def create_all_tables():
    db.create_all()
db.init_app(app)


app.secret_key = '1234'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    app.run(port=5000, debug=True)

