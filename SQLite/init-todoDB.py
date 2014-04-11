#!/usr/bin/env python
import sqlite3

# ======
# Create and populate database and table "todo_list"
# ======

db_path = 'todo_list.db'

with sqlite3.connect(db_path) as connection:
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS todo_list")
    cursor.execute("CREATE TABLE todo_list( \
                 title VARCHAR(100), \
                 description TEXT, \
                 uri VARCHAR(100), \
                 complete INTEGER NOT NULL DEFAULT 0)")
    cursor.execute("INSERT INTO todo_list(title, description, complete) VALUES('Complete ToDo app', 'Get this web-app working.', '1')")
    cursor.execute("SELECT rowid FROM todo_list ORDER BY rowid DESC LIMIT 1")
    first_task_id = cursor.fetchone()[0]
    first_task_uri = 'http://ec2-54-227-62-182.compute-1.amazonaws.com/todo/tasks/' + str(first_task_id)
    cursor.execute("UPDATE todo_list SET uri=? WHERE rowid=?", (first_task_uri, first_task_id))

