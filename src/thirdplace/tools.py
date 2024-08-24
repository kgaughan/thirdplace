import base64
import os
import re

import click

from thirdplace import core, models, views


def generate_secret_key(length: int) -> bytes:
    """
    Generate a string suitable for use as a secret key.
    """
    return base64.b64encode(os.urandom(length))


def replace_field(settings_path: str, field: str, length: int):
    """
    Update the given settings file with a new secret key.
    """
    with open(settings_path, "r+") as fh:
        lines = [line for line in fh if not re.match(f"^ *{field}", line)]
        lines.append(f"{field} = {generate_secret_key(length)!r}\n")
        fh.seek(0)
        fh.truncate()
        fh.writelines(lines)


@click.group()
def cli():
    pass


@cli.command()
def initdb():
    """
    Initialise the database.
    """
    with core.app.app_context():
        models.db.create_all()


@cli.command()
def salt():
    """
    Update the salt in a settings file.
    """
    replace_field(os.environ["THIRDPLACE_SETTINGS"], "SECURITY_PASSWORD_SALT", 12)


@cli.command()
def secretkey():
    """
    Update the secret key in a settings file.
    """
    # 48 is a multiple of both 6 and 8, thus won't leave rubbish at the end of
    # the key.
    replace_field(os.environ["THIRDPLACE_SETTINGS"], "SECRET_KEY", 48)


@cli.command()
def run():
    """
    Run the development server.
    """
    views.app.run()


if __name__ == "__main__":
    cli()
