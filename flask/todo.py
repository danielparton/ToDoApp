#!/usr/bin/env python
from flask import Flask, jsonify

app = Flask(__name__)

import MySQLdb as mdb

connection = mdb.connect('localhost', 'DLPtest', 'DLPtest', 'python_test')

@app.route('/todo/tasks', methods = ['GET'])
def get_tasks():

    with connection:
        cursor = connection.cursor()

    cursor = connection.cursor(mdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM todo_list") # use LIMIT to limit range of rows returned
    tasks = [row for row in cursor]

    return jsonify( {'tasks': tasks} )

if __name__ == '__main__':
    app.run(debug = True)

