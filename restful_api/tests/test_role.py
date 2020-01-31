import factory
from pytest_factoryboy import register

from myapi.models import User, Role
from myapi.config import VERSION


@register
class RoleFactory(factory.Factory):

    rolename = factory.Sequence(lambda n: "role%d" % n)
    rolename_cn = factory.Sequence(lambda n: "角色%d" % n)

    class Meta:
        model = Role


@register
class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "user%d" % n)
    username_cn = factory.Sequence(lambda n: "用户%d" % n)
    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    role_id = factory.Sequence(lambda n: n)
    password = "mypwd"

    class Meta:
        model = User


def test_get_role(client, db, role, admin_headers):
    # test 404
    rep = client.get(f"/api/v{VERSION[0]}/roles/100000", headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(role)
    db.session.commit()

    # test get_role
    rep = client.get(f"/api/v{VERSION[0]}/roles/{role.id}", headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["role"]
    assert data["rolename"] == role.rolename
    assert data["rolename_cn"] == role.rolename_cn


def test_get_role_no_token(client, no_token_header):
    # test no token
    rep = client.get(f"/api/v{VERSION[0]}/roles", headers=no_token_header)
    assert rep.status_code == 401


def test_get_role_fake_token(client, fake_token_header):
    # test fake token
    rep = client.get(f"/api/v{VERSION[0]}/roles", headers=fake_token_header)
    assert rep.status_code == 422


def test_put_role(client, db, role, admin_headers):
    # test 404
    rep = client.put(f"/api/v{VERSION[0]}/roles/100000", headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(role)
    db.session.commit()

    data = {"rolename": "updated"}

    # test update role
    rep = client.put(f"/api/v{VERSION[0]}/roles/%d" % role.id, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["role"]
    assert data["rolename"] == "updated"
    assert data["rolename_cn"] == role.rolename_cn


def test_delete_role_in_use(client, db, role, role_factory, admin_headers):
    # test 404
    rep = client.delete(f"/api/v{VERSION[0]}/roles/100000", headers=admin_headers)
    assert rep.status_code == 404

    db.session.add(role)
    db.session.commit()
    role_id = role.id

    # test delete role in use
    rep = client.delete(f"/api/v{VERSION[0]}/roles/{role_id}", headers=admin_headers)
    assert rep.status_code == 600


def test_delete_role(client, db, role, role_factory, admin_headers):
    # test delete role
    roles = role_factory.create_batch(10)

    db.session.add_all(roles)
    db.session.commit()

    role_id = roles[-1].id
    rep = client.delete(f"/api/v{VERSION[0]}/roles/{role_id}", headers=admin_headers)
    assert rep.status_code == 200
    assert db.session.query(Role).filter_by(id=role_id).first() is None


def test_create_role(client, db, admin_headers):
    # test bad data
    data = {"rolename": "created"}
    rep = client.post(f"/api/v{VERSION[0]}/roles", json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["rolename_cn"] = "创建"

    rep = client.post(f"/api/v{VERSION[0]}/roles", json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    role = db.session.query(Role).filter_by(id=data["role"]["id"]).first()

    assert role.rolename == "created"
    assert role.rolename_cn == "创建"


def test_get_all_role(client, db, role_factory, admin_headers):
    roles = role_factory.create_batch(30)

    db.session.add_all(roles)
    db.session.commit()

    rep = client.get(f"/api/v{VERSION[0]}/roles", headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for role in roles:
        assert any(u["id"] == role.id for u in results["results"])
