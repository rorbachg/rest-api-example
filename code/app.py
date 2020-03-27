from flask import Flask
from flask_restful import Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from models.user import UserModel
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = '1234'
api = Api(app)
jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
