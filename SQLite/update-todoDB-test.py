import sqlite3

# ======
# Update database
# ======

db_path = 'todo_list.db'

with sqlite3.connect(db_path) as connection:
    cursor = connection.cursor()
    cursor.execute("UPDATE todo_list SET complete='0' WHERE rowid='1'")

