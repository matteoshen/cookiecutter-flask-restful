VERSION=0.1
FLASK_ENV=development
FLASK_APP=myapi.app:create_app
DATABASE_URI=mysql+pymysql://backend:backend@localhost/backend&charset=utf8mb4
SECRET_KEY=changeme
JWT_ACCESS_TOKEN_EXPIRES = 3600
JWT_REFRESH_TOKEN_EXPIRES = 86400
