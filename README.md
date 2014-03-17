ToDoApp
=======

A simple to-do list web application.

Currently hosted on an Amazon EC2 instance:

http://ec2-54-227-62-182.compute-1.amazonaws.com/ToDoClient/

Feel free to play around with the to-do list. Number of tasks is limited to 10.

## Architecture

* Backend
    * MySQL database
    * Python Flask RESTful HTTP server
* Frontend
    * Components and styling via Bootstrap
    * API requests via jQuery
    * MVVM framework (including templating, event handling) via Knockout

Both backend and frontend are hosted by Apache as virtual hosts.

## Manifest

* MySQL/  - scripts for initializing and testing the MySQL database
* flask/  - Python Flask HTTP backend server
* html/   - HTML/JavaScript frontend

## Notes on using the database API (using the Flask built-in server on a local machine):

Leave this running:

    python flask/todo.py

To get list of tasks from browser, enter:

    http://localhost:5000/todo/tasks

From curl, enter:

    curl -i http://localhost:5000/todo/tasks

To add a task, enter (for example):

    curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Learn Flask"}' http://localhost:5000/todo/tasks

To delete a task by task ID (defined in the URL) (for example):

    curl -i -X DELETE http://localhost:5000/todo/tasks/2
