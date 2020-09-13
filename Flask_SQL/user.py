import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE username=?"
            result = cursor.execute(query, (username,))
            row = result.fetchone()
            if row:
                user = cls(*row)
            else:
                user = None
            connection.close()
            return user
        except:
            return {'message': 'Error occured while connecting to database'}, 500

    @classmethod
    def find_by_id(cls, _id):
        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE id=?"
            result = cursor.execute(query, (_id,))
            row = result.fetchone()

            if row:
                user = cls(*row)
            else:
                user = None
            connection.close()
            return user
        except:
            return {'message': 'Error occured while connecting to database'}, 500


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Enter Password!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A user with username {} already exists".format(data['username'])}, 400

        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "INSERT INTO users values(NULL,?,?)"
            cursor.execute(query, (data['username'], data['password']))
            connection.commit()
            connection.close()
            return {"message": "User Created successfully."}, 201
        except:
            return {'message': 'Error occured while connecting to database'}, 500
