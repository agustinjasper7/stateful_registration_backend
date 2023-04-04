# backend

Backend for Registration Site with State Management

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Creating Database File

-   To create a **database file**, use this command:

        $ touch db.sqlite3

### Creating Super User for Admin access

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser


### Type checks

Running type checks with mypy:

    $ mypy backend

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

#### Building the server image

    $ docker-compose -f local.yml build

#### Running the server

    $ docker-compose -f local.yml up -d

#### Terminating the server

    $ docker-compose -f local.yml up down

#### Connecting to Logs

    $ docker-compose -f local.yml logs -f django

#### Other Commands

Used to commands in docker like management commands, tests, coverage, shell, etc.

    $ docker-compose -f local.yml run --rm django <command>
