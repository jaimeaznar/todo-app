# TODO-APP
---

# API Usage

The API can be accessed at: https://todo-app-team-b.herokuapp.com

---

## Intro

This project is part of the Advanced Python course at MCSBT

---

## Install dependencies

### Python 3.X

Follow instructions to install the correct version of Python for your platform in the python [docs](https://www.python.org/downloads/)

### Virtual Environment (venv)

Instructions for setting up a virtual enviornment for your platform can be found in the python [docs](https://docs.python.org/3/tutorial/venv.html)

### PIP Dependencies
Once you have your venv setup and running, install dependencies by navigating to the root directory and running:

`pip install -r requirements.txt`
This will install all of the required packages included in the requirements.txt file.

### Local Database Setup

before running the project make sure to execute `createdb todoapp`

### Running the server

From within the root directory, first ensure you're working with your created venv. To run the server, execute the following:

`export FLASK_APP=app`
`export FLASK_ENV=development`
`flask run`
Setting the `FLASK_ENV` variable to development will detect file changes and restart the server automatically.

---

## Database Schema

Here is a representation of the db schema (models.py):


User
- id (primary key)
- name
- email
- password
- task

Task
- id (primary key)
- description
- state
- user_id (foreign key to task.id)

Every field must be populated. Constraints are enforced in the backend so that no fields are null. 

---

# Endpoint Overview

Postman can be used. Make sure the **session token**  is send along with requests for all CRUD endpoints.


## GET /
This endpoint doesn't require authentication
Returns `home.html`

## GET /signup

This endpoint doesn't require authentication.
renders signup form.
The endpoint will return a status code of 200 if successful.

## POST /signup

This endpoint doesn't require authentication.
Signs up a user and saves info in the database.
The endpoint will return a status code of 200 if successful.

## GET /login

This endpoint doesn't require authentication.
renders login form.
The endpoint will return a status code of 200 if successful.

## POST /login

This endpoint doesn't require authentication.
Logs in a user and will render the `tasks.html`page.
The endpoint will return a status code of 200 if successful.

## GET /logout

This endpoint requires authentication.
Logsout user and terminates session
The endpoint will return a status code of 200 if successful.

## GET /tasks

This endpoint requires authentication.
Shows `tasks` for logged in user.
The endpoint will return a status code of 200 if successful.

## GET /create-task

This endpoint requires authentication.
renders Task form.
The endpoint will return a status code of 200 if successful.

## POST /create-task

This endpoint requires authentication.
Commits task and saves it in the data base.
The endpoint will return a status code of 200 if successful.

## GET | POST /task-done/<int:task_id>
This endpoint requires authentication.
Changes task status and updates database.
The endpoint will return a status code of 200 and redirect (3xx) to `/tasks` endpoint.

## GET | POST /delete/<int:task_id>

This endpoint requires authentication.
Deletes task updates database.
The endpoint will return a status code of 200 and redirect (3xx) to `/tasks` endpoint.

