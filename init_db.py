import sqlite3


connection = sqlite3.connect("database.db")

with open("schema.sql") as f:
    connection.executescript(f.read())

cursor = connection.cursor()


def create_mock_data():
    cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                   ("First Post", "Content for first post")
                   )

    cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                   ("Second Post", "Content for second post")
                   )

    cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                   ("Third Post", "Content for third post")
                   )

    connection.commit()
    connection.close()


