#!/usr/bin/env python

# Create and populate a table

import MySQLdb as mdb

connection = mdb.connect('localhost', 'DLPtest', 'DLPtest', 'python_test')

with connection:
    cursor = connection.cursor(mdb.cursors.DictCursor)

    cursor.execute("DROP TABLE IF EXISTS todo_list")
    cursor.execute("CREATE TABLE todo_list(Id INT PRIMARY KEY AUTO_INCREMENT, \
                 title VARCHAR(100), \
                 description TEXT, \
                 uri VARCHAR(100), \
                 complete TINYINT NOT NULL DEFAULT 0)")
    cursor.execute("INSERT INTO todo_list(title, description, complete) VALUES('Complete ToDo app', 'Get this web-app working.', '1')")
    cursor.execute("SELECT * FROM todo_list ORDER BY Id DESC LIMIT 1")
    added_task = [row for row in cursor]
    added_id = added_task[0]['Id']
    new_uri = 'http://ec2-54-227-62-182.compute-1.amazonaws.com/todo/tasks/%d' % added_id
    cursor.execute("UPDATE todo_list SET uri='%s' WHERE Id='%d'" % (new_uri, added_id))

