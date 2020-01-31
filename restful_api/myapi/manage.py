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
    """Create a new admin user and a new admins role
    """
    from myapi.extensions import db
    from myapi.models import User, Role

    click.echo("create user")
    user = User(
        username="admin",
        username_cn="系统管理员",
        email="admin@mail.com",
        password="admin",
        role_id=1,
        active=True,
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")

    click.echo("create role")
    role = Role(role_name="admins", role_name_cn="系统管理员角色",)
    db.session.add(role)
    db.session.commit()
    click.echo("created role admins")


if __name__ == "__main__":
    cli()
