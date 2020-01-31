import click
from flask.cli import FlaskGroup

from myapi.app import create_app


def create_myapi(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_myapi)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Create a new admin user and new roles
    """
    from myapi.extensions import db
    from myapi.models import User, Role

    click.echo("create user")
    user_admin = User(
        username="admin",
        username_cn="系统管理员",
        email="admin@mail.com",
        password="admin",
        role_id=1,
        active=True,
    )
    db.session.add(user_admin)
    user_test = User(
        username="normal",
        username_cn="普通用户",
        email="normal@normal.com",
        password="normal",
        role_id=2,
        active=True,
    )
    db.session.add(user_admin)
    db.session.add(user_test)
    db.sesson.commit()
    click.echo("created user admin, normal")

    click.echo("create role")
    role_admins = Role(role_name="admins", role_name_cn="系统管理员角色",)
    role_normals = Role(role_name="normals", role_name_cn="普通用户角色",)
    db.session.add(role_admins)
    db.session.add(role_normals)
    db.session.commit()
    click.echo("created role admins, normals")


if __name__ == "__main__":
    cli()
