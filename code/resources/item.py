from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True, 
        help="This field cannot be left blank"
        )
    #@jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404
        
        
    def post(self, name):
        # force=True - for json format
        # silent=True - returns None insetad of error

        data = Item.parser.parse_args()

        if ItemModel.find_by_name(name):
            return {'message': F'An item with name {name} already exists'}, 400

        item = ItemModel(name, data['price'])
        try:
            item.insert()
        except:
            return {'message': 'An error occurred'}, 500
        return item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item:
            try:
                updated_item.update()
            except:
                return {'message': 'An error occurred'}, 500
        else:
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occurred'}, 500
        return updated_item.json(), 200


class ItemList(Resource):
    def get(self):
        items = []
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        for row in cursor.execute("SELECT * FROM items"):
            items.append({'id': row[0], 'name': row[1], 'price': row[2]})
        connection.close()
        return {'items': items}