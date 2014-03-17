#!/usr/bin/env python
from flask import Flask, jsonify, request, abort, make_response

# ======
# This class is necessary to allow access to other websites on the same server
# ======

class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the 
    front-end server to add these headers, to let you quietly bind 
    this to a URL other than / and to an HTTP scheme that is 
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


# ======
# Set up the Flask app and read in the MySQL db
# ======

app = Flask(__name__)
#app = Flask(__name__, static_url_path="")
#app.wsgi_app = ReverseProxied(app.wsgi_app)

import MySQLdb as mdb

connection = mdb.connect('localhost', 'DLPtest', 'DLPtest', 'python_test')

tasks_base_url = 'http://ec2-54-227-62-182.compute-1.amazonaws.com/todo/tasks'

maxtasks = 10


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

    with connection:
        cursor = connection.cursor(mdb.cursors.DictCursor)

    # check how many tasks are currently in the table - abort if there are already 10
    cursor.execute("SELECT * FROM todo_list")
    tasks = [row for row in cursor]
    if len(tasks) == maxtasks:
        abort(400)

    # insert task into the SQL DB
    cursor.execute("INSERT INTO todo_list(title, description) VALUES('%s', '%s')" % (title, description))

    # return the row just added
    cursor.execute("SELECT * FROM todo_list ORDER BY Id DESC LIMIT 1")
    added_task = [row for row in cursor]
    added_id = added_task[0]['Id']
    new_uri = '%s/%d' % (tasks_base_url, added_id)
    cursor.execute("UPDATE todo_list SET uri='%s' WHERE Id='%d'" % (new_uri, added_id))
    cursor.execute("SELECT * FROM todo_list ORDER BY Id DESC LIMIT 1")
    added_task = [row for row in cursor][0]

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
# Edit a task
# ======

@app.route('/todo/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    with connection:
        cursor = connection.cursor(mdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM todo_list WHERE Id = %d" % task_id) # use LIMIT to limit range of rows returned
    task = [row for row in cursor]

    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != unicode:
        abort(400)
    if 'complete' in request.json and type(request.json['complete']) not in [int, bool]:
        abort(400)

    task = task[0]

    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['complete'] = request.json.get('complete', task['complete'])

    cursor.execute("UPDATE todo_list SET title='%s', description='%s', complete='%d' WHERE Id='%d'" % (task['title'], task['description'], task['complete'], task_id))

    # return the row just updated
    cursor.execute("SELECT * FROM todo_list WHERE Id = %d" % task_id)
    updated_task = [row for row in cursor][0]

    return jsonify( { 'task': updated_task } )


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', debug=True)

