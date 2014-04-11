import sqlite3

# ======
# Retrieve data
# ======

db_path = 'todo_list.db'

with sqlite3.connect(db_path) as connection:
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM todo_list")

    # column headers
    column_headers = cursor.description
    print column_headers

    # fetch all rows
    rows = cursor.fetchall()
    for row in rows:
        print row
        pass

