import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, "Manoj", "asdf")

insert_query = "INSERT into users values (?,?,?)"
cursor.execute(insert_query,user)

connection.commit()
connection.close()