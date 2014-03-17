# Retrieve data

import MySQLdb as mdb

connection = mdb.connect('localhost', 'DLPtest', 'DLPtest', 'python_test')

with connection:
    cursor = connection.cursor(mdb.cursors.DictCursor)

    cursor.execute("UPDATE todo_list SET complete='0' WHERE Id='1'")

