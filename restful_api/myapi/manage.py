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
    """Create a new admin user
    """
    from myapi.extensions import db
    from myapi.models import User

    click.echo("create user")
    user = User(
        username="admin",
        username_cn="系统管理员",
        email="admin@mail.com",
        password="admin",
        active=True,
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
