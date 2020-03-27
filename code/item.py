from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True, 
        help="This field cannot be left blank"
        )
    #@jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item, 200
        return {'message': 'Item not found'}, 404
        
        
    def post(self, name):
        # force=True - for json format
        # silent=True - returns None insetad of error

        data = Item.parser.parse_args()

        if Item.find_by_name(name):
            return {'message': F'An item with name {name} already exists'}, 400

        try:
            item = Item.insert(name, data['price'])
        except:
            return {'message': 'An error occurred'}, 500
        return item, 201

    @classmethod
    def insert(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(NULL, ?, ?)"
        cursor.execute(query, (name, price))
        connection.commit()
        connection.close()
        item = cls.find_by_name(name)
        return item

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
        item = Item.find_by_name(name)
        if item:
            try:
                item = Item.update(name, data['price'])
            except:
                return {'message': 'An error occurred'}, 500
        else:
            try:
                item = Item.insert(name, data['price'])
            except:
                return {'message': 'An error occurred'}, 500
        return item, 200

    @classmethod
    def update(cls, name, price):
        print('Updating..')
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("UPDATE items SET price = ? WHERE name = ?", (price, name))
        connection.commit()
        connection.close()
        item = cls.find_by_name(name)
        print(item)
        return item

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'id': row[0], 'name': row[1], 'price': row[2]}}
        return None

class ItemList(Resource):
    def get(self):
        items = []
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        for row in cursor.execute("SELECT * FROM items"):
            items.append({'id': row[0], 'name': row[1], 'price': row[2]})
        connection.close()
        return {'items': items}