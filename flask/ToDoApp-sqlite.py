#!/usr/bin/env python
from flask import Flask, jsonify, request, abort, make_response, g
import os, sys, sqlite3

app = Flask(__name__)

# ======
# Parameters
# ======

db_path = '../SQLite/todo_list.db'
tasks_base_url = 'http://ec2-54-227-62-182.compute-1.amazonaws.com/todo/tasks'
maxtasks = 10


# ======
# database connection and teardown, and other general-use defs
# ======

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = getattr(g, '_database', None)
    if db == None:
        db = g._database = sqlite3.connect(db_path)
    db.row_factory = dict_factory
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db != None:
        db.close()


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

    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM todo_list") # use LIMIT to limit range of rows returned
    tasks = [row for row in cursor]

    return jsonify( {'tasks': tasks} )


# ======
# Get a single task
# ======

@app.route('/todo/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    '''Return a single task in JSON format'''

    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM todo_list WHERE rowid = ?", str(task_id))
    task = [row for row in cursor]
    if len(task) == 0:
        abort(404)
    task = task[0]

    return jsonify( {'task': task} )


# ======
# Add a task
# ======

@app.route('/todo/tasks', methods = ['POST'])
def create_task():
    '''Accepts a task in JSON format and adds it to the SQL DB.
    Returns the added task.
    Max 10 tasks.'''

    # request must be json format
    if not request.json or not 'title' in request.json:
        abort(400)

    # get title and description from the json request
    title = request.json['title']
    description = request.json.get('description', "")

    db = get_db()
    cursor = db.cursor()

    # check how many tasks are currently in the table - abort if there are already 10
    cursor.execute("SELECT * FROM todo_list")
    tasks = cursor.fetchall()
    if len(tasks) == maxtasks:
        abort(400)

    # insert task into the SQL DB
    cursor.execute("INSERT INTO todo_list(title, description) VALUES(?,?)", (title, description))
    added_id = str(cursor.lastrowid)

    # return the row just added
    cursor.execute("SELECT rowid FROM todo_list ORDER BY rowid DESC LIMIT 1")
    #added_id = str(cursor.fetchone()[0])
    new_uri = tasks_base_url + '/' + added_id
    cursor.execute("UPDATE todo_list SET uri=? WHERE rowid=?", (new_uri, added_id))
    #cursor.execute("SELECT * FROM todo_list ORDER BY rowid DESC LIMIT 1")
    cursor.execute("SELECT * FROM todo_list WHERE rowid=?", added_id)
    added_task = cursor.fetchone()

    db.commit()

    return jsonify( { 'task': added_task } ), 201


# ======
# Delete a task
# ======

@app.route('/todo/tasks/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    '''Delete a task.'''

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM todo_list WHERE rowid=?", str(task_id))

    db.commit()

    return jsonify( { 'result': True } )


# ======
# Edit a task
# ======

@app.route('/todo/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM todo_list WHERE rowid = ?", str(task_id))
    task = cursor.fetchone()

    print request.json

    #if len(task) == 0:
    #    abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != unicode:
        abort(400)
    if 'complete' in request.json and type(request.json['complete']) not in [int, bool]:
        abort(400)

    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['complete'] = request.json.get('complete', task['complete'])

    cursor.execute("UPDATE todo_list SET title=?, description=?, complete=? WHERE rowid=?", (task['title'], task['description'], task['complete'], str(task_id)))

    # return the row just updated
    cursor.execute("SELECT * FROM todo_list WHERE rowid=?", str(task_id))
    updated_task = cursor.fetchone()

    return jsonify( { 'task': updated_task } )


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', debug=True)

