VERSION=0.1
FLASK_ENV=development
FLASK_APP={{cookiecutter.app_name}}.app:create_app
SECRET_KEY=changeme
DATABASE_URI=mysql+pymysql://backend:backend@localhost/backend
JWT_ACCESS_TOKEN_EXPIRES = 3600
JWT_REFRESH_TOKEN_EXPIRES = 86400
{%- if cookiecutter.use_celery == "yes" %}
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/
{%- endif %}