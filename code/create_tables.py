import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text UNIQUE, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)
cursor.execute("INSERT INTO items VALUES(NULL, 'chair', 16.99)")

for row in cursor.execute("SELECT * FROM items"):
    print(row)

connection.commit()
connection.close()