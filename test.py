import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

drop_table = "DROP TABLE IF EXISTS users"
create_table = "CREATE TABLE users (id int, username text, password text)"

user = (1, 'jose', 'adfs')
insert_query = 'INSERT INTO users VALUES (?, ?, ?)'

users = [(1, 'jose', 'adfs'),
         (2, 'rolf', 'xys'),
         (3, 'anne', 'ghj')]

select_query = "SELECT * FROM users"
cursor.execute(drop_table)
cursor.execute(create_table)
cursor.executemany(insert_query, users)

for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()