webdev
======

For testing web development tools

## Manifest

* flask/  - for testing Flask microframework

## todo-list application

* Flask backend
* MySQL database
* Frontend TODO

### Operation:

Leave this running:

    ./flask/todo.py

To get list of tasks from browser, enter:

    http://localhost:5000/todo/tasks

From curl, enter:

    curl -i http://localhost:5000/todo/tasks

To add a task, enter (for example):

    curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Learn Flask"}' http://localhost:5000/todo/tasks

To delete a task by task ID (defined in the URL) (for example):

    curl -i -X DELETE http://localhost:5000/todo/tasks/2
