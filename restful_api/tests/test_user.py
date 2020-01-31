import factory
from pytest_factoryboy import register

from myapi.models import User
from myapi.config import VERSION


@register
class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    username_cn = factory.Sequence(lambda n: "用户%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"
    role_id = 1

    class Meta:
        model = User


def test_get_user(client, db, user, admin_headers):
    # test 404
    rep = client.get(f"/api/v{VERSION[0]}/users/100000", headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user
    rep = client.get(f"/api/v{VERSION[0]}/users/%d" % user.id, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == user.username
    assert data["username_cn"] == user.username_cn
    assert data["email"] == user.email
    assert data["active"] == user.active
    assert data["role_id"] == user.role_id


def test_get_user_no_token(client, no_token_header):
    # test no token
    rep = client.get(f"/api/v{VERSION[0]}/users", headers=no_token_header)
    assert rep.status_code == 401


def test_get_user_fake_token(client, fake_token_header):
    # test fake token
    rep = client.get(f"/api/v{VERSION[0]}/users", headers=fake_token_header)
    assert rep.status_code == 422


def test_put_user(client, db, user, admin_headers):
    # test 404
    rep = client.put(f"/api/v{VERSION[0]}/users/100000", headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    data = {"username": "updated"}

    # test update user
    rep = client.put(f"/api/v{VERSION[0]}/users/%d" % user.id, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == "updated"
    assert data["username_cn"] == user.username_cn
    assert data["email"] == user.email
    assert data["role_id"] == user.role_id
    assert data["active"] == user.active


def test_delete_user(client, db, user, admin_headers):
    # test 404
    rep = client.delete(f"/api/v{VERSION[0]}/users/100000", headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    # test get_user
    user_id = user.id
    rep = client.delete(f"/api/v{VERSION[0]}/users/%d" % user_id, headers=admin_headers)
    assert rep.status_code == 200
    assert db.session.query(User).filter_by(id=user_id).first() is None


def test_create_user(client, db, admin_headers):
    # test bad data
    data = {"username": "created"}
    rep = client.post(f"/api/v{VERSION[0]}/users", json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["username_cn"] = "创建"
    data["password"] = "admin"
    data["email"] = "create@mail.com"
    data["role_id"] = 1

    rep = client.post(f"/api/v{VERSION[0]}/users", json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    user = db.session.query(User).filter_by(id=data["user"]["id"]).first()

    assert user.username == "created"
    assert user.username_cn == "创建"
    assert user.email == "create@mail.com"
    assert user.role_id == 1


def test_get_all_user(client, db, user_factory, admin_headers):
    users = user_factory.create_batch(30)

    db.session.add_all(users)
    db.session.commit()

    rep = client.get(f"/api/v{VERSION[0]}/users", headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for user in users:
        assert any(u["id"] == user.id for u in results["results"])
