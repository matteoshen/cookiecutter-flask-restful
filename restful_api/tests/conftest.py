import json
import pytest

from myapi.models import User
from myapi.app import create_app
from myapi.extensions import db as _db


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        username='admin',
        username_cn='系统管理员',
        email='admin@admin.com',
        password='admin',
        role_id=1
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def normal_user(db):
    user = User(
        username='normal',
        username_cn='普通用户',
        email='normal@normal.com',
        password='normal',
        role_id=2
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def admin_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def normal_headers(normal_user, client):
    data = {
        'username': normal_user.username,
        'password': 'normal'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['access_token']
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {
        'username': admin_user.username,
        'password': 'admin'
    }
    rep = client.post(
        '/auth/login',
        data=json.dumps(data),
        headers={'content-type': 'application/json'}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer %s' % tokens['refresh_token']
    }


@pytest.fixture
def no_token_header():
    return {
        'content-type': 'application/json',
    }


@pytest.fixture
def fake_token_header():
    return {
        'content-type': 'application/json',
        'authorization': 'Bearer shenshenehss'
    }
