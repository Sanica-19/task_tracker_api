# Task Tracker REST API

A simple REST API built with Python, Flask and SQLite for managing tasks (create, read, update, delete).

## Features
- CRUD endpoints for tasks (GET, POST, PUT, DELETE /tasks)
- SQLite database with parameterized SQL queries
- Input validation and error handling (400 / 404 responses)
- Unit tests with pytest using a temporary test database

## Tech Stack
Python, Flask, SQLite, pytest, Git

## Run locally
    pip install -r requirements.txt
    python app.py

## Run tests
    pytest

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | List all tasks |
| POST | /tasks | Add a task (JSON: title) |
| PUT | /tasks/<id> | Mark a task done (JSON: done) |
| DELETE | /tasks/<id> | Delete a task |