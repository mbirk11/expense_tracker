# Expense Tracker API

Expense Tracker API built with Django REST Framework.

## Live Demo

Swagger Documentation:

http://13.50.248.37:8000/api/docs/

## Features

* Custom User Model
* JWT Authentication
* Email Verification
* Password Recovery
* Redis Integration
* Category Management
* Expense Management
* Docker Support
* PostgreSQL Support
* Swagger Documentation

## Installation

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Docker

```bash
docker-compose up --build
```

## Run Tests

```bash
python manage.py test
```
