#!/usr/bin/env python
from flask import Flask, jsonify, request

app = Flask(__name__)

import MySQLdb as mdb

connection = mdb.connect('localhost', 'DLPtest', 'DLPtest', 'python_test')


# ======
# Get list of tasks
# ======

@app.route('/todo/tasks', methods = ['GET'])
def get_tasks():
    '''Return all tasks in JSON format'''

    with connection:
        cursor = connection.cursor()

    cursor = connection.cursor(mdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM todo_list") # use LIMIT to limit range of rows returned
    tasks = [row for row in cursor]

    return jsonify( {'tasks': tasks} )


# ======
# Add a task
# ======

@app.route('/todo/tasks', methods = ['POST'])
def create_task():
    '''Accepts a task in JSON format and adds it to the SQL DB.
    Returns the added task.'''

    # request must be json format
    if not request.json or not 'title' in request.json:
        abort(400)

    # get title and description from the json request
    title = request.json['title']
    description = request.json.get('description', "")

    with connection:
        cursor = connection.cursor()

    # insert task into the SQL DB
    cursor.execute("INSERT INTO todo_list(title, description) VALUES('%s', '%s')" % (title, description))

    # return the row just added
    cursor.execute("SELECT * FROM todo_list ORDER BY Id DESC LIMIT 1")
    added_task = [row for row in cursor]

    return jsonify( { 'task': added_task } ), 201


# ======
# Delete a task
# ======

@app.route('/todo/tasks/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    '''Delete a task.'''

    with connection:
        cursor = connection.cursor()

    cursor.execute("DELETE FROM todo_list WHERE Id = '%d'" % task_id)

    return jsonify( { 'result': True } )


# ======
# Toggle task complete field
# ======

# TODO


if __name__ == '__main__':
    app.run(debug = True)

