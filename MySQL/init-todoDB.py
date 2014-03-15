#!/usr/bin/env python

# Create and populate a table

import MySQLdb as mdb

connection = mdb.connect('localhost', 'DLPtest', 'DLPtest', 'python_test')

with connection:
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS todo_list")
    cursor.execute("CREATE TABLE todo_list(Id INT PRIMARY KEY AUTO_INCREMENT, \
                 title VARCHAR(50), \
                 description VARCHAR(50), \
                 complete TINYINT NOT NULL DEFAULT 0)")
    cursor.execute("INSERT INTO todo_list(title, description) VALUES('Learn MySQL', 'Learn how to operate a MySQL database using Python')")

