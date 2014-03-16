#!/usr/bin/env python
from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)

import MySQLdb as mdb

connection = mdb.connect('localhost', 'DLPtest', 'DLPtest', 'python_test')


# ======
# 404 error handler
# ======

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

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
# Get a single task
# ======

@app.route('/todo/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    '''Return a single task in JSON format'''

    with connection:
        cursor = connection.cursor()

    cursor = connection.cursor(mdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM todo_list WHERE Id = %d" % task_id)
    task = [row for row in cursor]
    if len(task) == 0:
        abort(404)

    return jsonify( {'task': task} )


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

@app.route('/todo/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    with connection:
        cursor = connection.cursor()

    cursor = connection.cursor(mdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM todo_list WHERE Id = %d" % task_id) # use LIMIT to limit range of rows returned
    task = [row for row in cursor]

    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'complete' in request.json and type(request.json['complete']) is not int:
        abort(400)

    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['complete'] = request.json.get('complete', task[0]['complete'])

    cursor.execute("UPDATE todo_list SET title='%s', description='%s', complete='%d' WHERE Id='%d'" % (task[0]['title'], task[0]['description'], task[0]['complete'], task_id))

    # return the row just updated
    cursor.execute("SELECT * FROM todo_list WHERE Id = %d" % task_id)
    updated_task = [row for row in cursor]

    return jsonify( { 'task': updated_task } )
    #return jsonify( { 'task': task } )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

