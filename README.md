# cookiecutter-flask-restful

Cookiecutter template for flask restful, including blueprints, application factory, and more

## Introduction

This cookie cutter is a very simple boilerplate for starting a REST api using Flask, flask-restful, marshmallow, SQLAlchemy and jwt.
It comes with basic project structure and configuration, including blueprints, application factory and basics unit tests.

Features

* Simple flask application using application factory, blueprints
* [Flask command line interface](http://flask.pocoo.org/docs/1.0/cli/) integration
* Simple cli implementation with basics commands (init, run, etc.)
* [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/) included in entry point
* Authentication using [Flask-JWT-Extended](http://flask-jwt-extended.readthedocs.io/en/latest/) including access token and refresh token management
* Simple pagination utils
* Unit tests using pytest and factoryboy
* Configuration using environment variables
* OpenAPI json file and swagger UI

Used packages :

* [Flask](http://flask.pocoo.org/)
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
* [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/)
* [Flask-JWT-Extended](http://flask-jwt-extended.readthedocs.io/en/latest/)
* [marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/)
* [passlib](https://passlib.readthedocs.io/en/stable/)
* [tox](https://tox.readthedocs.io/en/latest/)
* [pytest](https://docs.pytest.org/en/latest/)
* [factoryboy](http://factoryboy.readthedocs.io/en/latest/)
* [dotenv](https://github.com/theskumar/python-dotenv)
* [apispec](https://github.com/marshmallow-code/apispec)

## Usage

* [Installation](#installation)
* [Configuration](#configuration)
* [Authentication](#athentication)
* [Running tests](#running-tests)
* [WSGI Server](#installing-a-wsgi-server)
* [Flask CLI](#using-flask-cli)
* [Using Celery](#using-celery)
* [Using Docker](#using-docker)
* [Makefile](#makefile-usage)
* [APISpec and swagger](#using-apispec-and-swagger)
* [Test](#test)
* [Changelog](#changelog)


### Installation

For the example, let's say you named your app `myapi` and your project `myproject`

Once project started with cookiecutter, you can install it using pip :

```
cd myproject
pip install -r requirements.txt
pip install -e .
```

You have now access to cli commands and you can init your project

```
myapi db upgrade
myapi init
```

To list all commands

```
myapi --help
```

### Configuration

Configuration is handled by environment variables, for development purpose you just
need to update / add entries in `.flaskenv` file.

It's filled by default with following content:

```
FLASK_ENV=development
FLASK_APP="myapp.app:create_app"
SECRET_KEY=changeme
DATABASE_URI="sqlite:////tmp/myapp.db"
CELERY_BROKER_URL=amqp://guest:guest@localhost/  # only present when celery is enabled
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/  # only present when celery is enabled
```

Avaible configuration keys:

* `FLASK_ENV`: flask configuration key, enables `DEBUG` if set to `development`
* `SECREY_KEY`: your application secret key
* `DATABASE_URI`: SQLAlchemy connection string
* `CELERY_BROKER_URL`: URL to use for celery broker, only when you enabled celery
* `CELERY_RESULT_BACKEND_URL`: URL to use for celery result backend (e.g: `redis://localhost`)

### Authentication


To access protected resources, you will need an access token. You can generate 
an access and a refresh token using `/auth/login` endpoint, example using curl

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}' http://localhost:5000/auth/login
```

This will return something like this

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWRlbnRpdHkiOjEsImlhdCI6MTUxMDAwMDQ0MSwiZnJlc2giOmZhbHNlLCJqdGkiOiI2OTg0MjZiYi00ZjJjLTQ5MWItYjE5YS0zZTEzYjU3MzFhMTYiLCJuYmYiOjE1MTAwMDA0NDEsImV4cCI6MTUxMDAwMTM0MX0.P-USaEIs35CSVKyEow5UeXWzTQTrrPS_YjVsltqi7N4", 
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNTEwMDAwNDQxLCJ0eXBlIjoicmVmcmVzaCIsImp0aSI6IjRmMjgxOTQxLTlmMWYtNGNiNi05YmI1LWI1ZjZhMjRjMmU0ZSIsIm5iZiI6MTUxMDAwMDQ0MSwiZXhwIjoxNTEyNTkyNDQxfQ.SJPsFPgWpZqZpHTc4L5lG_4aEKXVVpLLSW1LO7g4iU0"
}
```
You can use access_token to access protected endpoints :

```bash
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWRlbnRpdHkiOjEsImlhdCI6MTUxMDAwMDQ0MSwiZnJlc2giOmZhbHNlLCJqdGkiOiI2OTg0MjZiYi00ZjJjLTQ5MWItYjE5YS0zZTEzYjU3MzFhMTYiLCJuYmYiOjE1MTAwMDA0NDEsImV4cCI6MTUxMDAwMTM0MX0.P-USaEIs35CSVKyEow5UeXWzTQTrrPS_YjVsltqi7N4" http://127.0.0.1:5000/api/v1/users
```

You can use refresh token to retreive a new access_token using the endpoint `/auth/refresh`


```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNTEwMDAwNDQxLCJ0eXBlIjoicmVmcmVzaCIsImp0aSI6IjRmMjgxOTQxLTlmMWYtNGNiNi05YmI1LWI1ZjZhMjRjMmU0ZSIsIm5iZiI6MTUxMDAwMDQ0MSwiZXhwIjoxNTEyNTkyNDQxfQ.SJPsFPgWpZqZpHTc4L5lG_4aEKXVVpLLSW1LO7g4iU0" http://127.0.0.1:5000/auth/refresh
```

this will only return a new access token

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWRlbnRpdHkiOjEsImlhdCI6MTUxMDAwMDYxOCwiZnJlc2giOmZhbHNlLCJqdGkiOiIzODcxMzg4Ni0zNGJjLTRhOWQtYmFlYS04MmZiNmQwZjEyNjAiLCJuYmYiOjE1MTAwMDA2MTgsImV4cCI6MTUxMDAwMTUxOH0.cHuNf-GxVFJnUZ_k9ycoMMb-zvZ10Y4qbrW8WkXdlpw"
}
```

### Running tests

Simplest way to run tests is to use tox, it will create a virtualenv for tests, install all dependencies and run pytest

```
tox
```

But you can also run pytest manually, you just need to install tests dependencies before

```
pip install pytest pytest-runner pytest-flask pytest-factoryboy factory_boy
pytest
```

With docker-compose and the Makefile
```bash
make tests
```

**WARNING**: you will need to set env variables

### Installing a wsgi server
#### Running with gunicorn

This project provide a simple wsgi entry point to run gunicorn or uwsgi for example.

For gunicorn you only need to run the following commands

```
pip install gunicorn
gunicorn myapi.wsgi:app
```

And that's it ! Gunicorn is running on port 8000

If you chose gunicorn as your wsgi server, the proper commands should be in your docker-compose file.

#### Running with uwsgi

Pretty much the same as gunicorn here

```
pip install uwsgi
uwsgi --http 127.0.0.1:5000 --module myapi.wsgi:app
```

And that's it ! Uwsgi is running on port 5000

If you chose uwsgi as your wsgi server, the proper commands should be in your docker-compose file.

### Using Flask CLI

This cookiecutter is fully compatible with default flask CLI and use a `.flaskenv` file to set correct env variables to bind the application factory.
Note that we also set `FLASK_ENV` to `development` to enable debugger.


### Using Celery

This cookiecutter has an optional [Celery](http://www.celeryproject.org/) integration that let you choose if you want to use it or not in your project.
If you choose to use Celery, additionnal code and files will be generated to get started with it.

This code will include a dummy task located in `yourproject/yourapp/tasks/example.py` that only return `"OK"` and a `celery_app` file used to your celery workers.


#### Running celery workers

In your project path, once dependencies are installed, you can just run

```
celery worker -A myapi.celery_app:app --loglevel=info
```

If you have updated your configuration for broker / result backend your workers should start and you should see the example task avaible

```
[tasks]
  . myapi.tasks.example.dummy_task
```


#### Running a task

To run a task you can either import it and call it

```python
>>> from myapi.tasks.example import dummy_task
>>> result = dummy_task.delay()
>>> result.get()
'OK'
```

Or use the celery extension

```python
>>> from myapi.extensions import celery
>>> celery.send_task('myapi.tasks.example.dummy_task').get()
'OK'
```

## Using docker

**WARNING** both Dockerfile and `docker-compose.yml` are **NOT** suited for production, use them for development only or as a starting point.

This template offer simple docker support to help you get started and it comes with both Dockerfile and a `docker-compose.yml`. Please note that docker-compose is mostly useful when using celery
since it takes care of running rabbitmq, redis, your web API and celery workers at the same time, but it also work if you don't use celery at all.

Dockerfile has intentionally no entrypoint to allow you to run any command from it (server, shell, init, celery, ...)

Note that you still need to init your app on first start, even when using compose.

```bash
docker build -t myapp .
...
docker run --env-file=.flaskenv myapp myapi init
docker run --env-file=.flaskenv -p 5000:5000 myapp myapi run -h 0.0.0.0
 * Serving Flask app "myapi.app:create_app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 214-619-010
```

With compose

```bash
docker-compose up
...
docker exec -it <container_id> myapi init
```

With docker-compose and the Makefile
```bash
make init
```

## Makefile usage

Initizalize the environment
```bash
make init
```

Build the containers
```bash
make build
```

Run the containers
```bash
make run
```

Create new database migration
```bash
make db-migrate
```

Apply database migrations
```bash
make db-upgrade
```

Run tests
```bash
make test
```

## Using APISpec and Swagger

This boilerplate comes with pre-configured APISpec and swagger endpoints. Using default configuration you have two endpoints avaible:

* `/swagger.json`: return OpenAPI specification file in json format
* `/swagger-ui`: swagger UI configured to hit OpenAPI json file

This come with a very simple extension that allow you to override basic settings of APISpec using your `config.py` file:

* `APISPEC_TITLE`: title for your spec, default to `{{cookiecutter.project_name}}`
* `APISPEC_VERSION`: version of your API, default to `1.0.0`
* `OPENAPI_VERSION`: OpenAPI version of your spec, default to `3.0.2`
* `SWAGGER_JSON_URL`: Url for your JSON specifications, default to `/swagger.json`
* `SWAGGER_UI_URL`: Url for swagger-ui, default to `/swagger-ui`
* `SWAGGER_URL_PREFIX`: URL prefix to use for swagger blueprint, default to `None`

## Test

Tox is used for automate test, test under different python versions is configured in tox.ini. One should pay attention usage with pyenv, a .python-version file should specify (with prioirty) python versions used in tox.

example of .python-version

```bash
restful_api
3.6.10
3.8.1
```

tox parallel

```bash
tox -p all
```

tox lint with black and flake8

```bash
tox -e lint
```

## Changelog

### 18/01/2020

* Added python 3.8 support
* Upgraded to marshmallow 3
* Added `lint` and `tests` envs to tox
* Added black support
* Improved travis tests
* Updated Makefile to handle tests with celery
* Updated tox to handle env variables for celery when runing tests
* Added initial db migration instead of relying on `db.create_all()`
* Added new step to create database in README
* Various cleanup

### 08/2019

* Added apispec dependencies
* Registered `users` endpoints into swagger
* New `apispec` extension
* Added two new routes `/swagger.json` and `/swagger-ui` (configurable urls)
* Added swagger html template
* Add travis file

### 26/04/2019

* Added docker and docker-compose support

### 24/04/2019

* Update configuration to only use env variables, `.flaskenv` has been updated too
* Add unit tests for celery
* Add flake8 to tox
* Configuration file cannot be overridden by `MYAPP CONFIG` env variable anymore
* various cleanups (unused imports, removed `configtest.py` file, flake8 errors)

