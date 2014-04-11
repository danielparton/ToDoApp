ToDoApp
=======

A simple to-do list web application.

Currently hosted on an Amazon EC2 instance:

http://ec2-54-227-62-182.compute-1.amazonaws.com/ToDoClient/

Feel free to play around with the to-do list. Number of tasks is limited to 10.

This application is closely based on the tutorials by Miguel Grinberg:

https://github.com/miguelgrinberg/REST-tutorial

http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

http://blog.miguelgrinberg.com/post/writing-a-javascript-rest-client

I made a few changes, such as using MySQL for data storage, using Apache
virtual hosts to host the server and client, and I removed the user-login
feature. The latter change was to avoid communicating user login details
insecurely, since a) I am serving the application over HTTP, not HTTPS, and b)
this is my first network app and I didn't want to risk compromising people's
data if I do something wrong...

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

## Installation notes

The exact installation process will likely be highly dependent upon your server
set-up, so I only give here a few basic details here.

Please edit flask/backend-config.yaml-TEMPLATE with your own MySQL
authorization credentials, then rename to the file to 'backend-config.yaml'.

The various source files will need to be moved to the appropriate locations on
your server(s). The frontend consists of one file: html/index.html.  The
backend consists of flask/ToDoApp.py, flask/backend-config.yaml, and the
scripts in the MySQL directory. These backend files should be put together in
the same folder. The frontend and backend should be hosted as separate servers
(or virtual hosts).

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
