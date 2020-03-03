import click
from flask.cli import FlaskGroup
from flask_migrate.cli import db

from itembox.app import create_app


def create_itembox(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_itembox)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Create a new db
    """
    import os
    from itembox.config import db
    from itembox.models.items import Item

    click.echo("initializ db")
    # Data to initialize database with
    ITEMS = [
        {"uid": "1", "name": "server01"},
        {"uid": "2", "name": "server02"},
        {"uid": "3", "name": "server03"},
    ]

    # Delete database file if it exists currently
    if os.path.exists("itemBox.db"):
        os.remove("itemBox.db")

    # Create the database
    db.create_all()

    # iterate over the ITEMS structure and populate the database
    for item in ITEMS:
        i = Item(uid=item.get("uid"), name=item.get("name"), itemof='')
        db.session.add(i)

    db.session.commit()
    click.echo("initialized db")


if __name__ == "__main__":
    cli()