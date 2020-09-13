from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field can not be left blank!"
    )

    @classmethod
    def find_item_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item':
                    {
                        'name': row[0],
                        'price': row[1]
                    }
                    }

    @classmethod
    def insert_item(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items values(?,?)"
        cursor.execute(query, (name, price))
        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, name, price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items set price=? where name=?"
        cursor.execute(query, (price, name))
        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        try:
            item = Item.find_item_by_name(name)
            if item:
                return item
            return {'message': 'item not found'}
        except:
            return {'message': 'Error occured while connecting to database'}, 500

    def post(self, name):
        try:
            item = Item.find_item_by_name(name)
            if item:
                return {'message': 'An item with name {} already exists in database'.format(name)}, 400

            requested_data = Item.parser.parse_args()
            item = {'name': name, 'price': requested_data['price']}
            Item.insert_item(name, requested_data['price'])
            return item, 201
        except:
            return {'message': 'Error occured while connecting to database'}, 500

    def delete(self, name):
        if Item.find_item_by_name(name) is None:
            return {"message": "Item was not found in database"}
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items where name=?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {"message": "item has been deleted"}
        except:
            return {"message": "An error occured while updating database"}, 500

    def put(self, name):
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            if Item.find_item_by_name(name):
                Item.update_item(name, data['price'])
            else:
                Item.insert_item(name, data['price'])
            return item, 200
        except:
            return {'message': 'Error occured while connecting to database'}, 500


class ItemList(Resource):
    def get(self):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "SELECT * FROM items"
            result = cursor.execute(query)
            
            if result:
                items = []
                for row in result:
                    items.append({'name': row[0], 'price': row[1]})
                return ({"items": items}), 200
            else:
                return ({"message": "No items found in database"}), 200

            connection.close()
        except:
            return ({"message": "Error occured while connecting to database"}), 500
