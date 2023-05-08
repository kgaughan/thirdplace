import base64
import os
import re

import click

from thirdplace import models, views


def generate_secret_key() -> bytes:
    """
    Generate a string suitable for use as a secret key.
    """
    # 48 is a multiple of both 6 and 8, thus won't leave rubbish at the
    # end of the key.
    return base64.b64encode(os.urandom(48))


def replace_secret_key(settings_path: str):
    """
    Update the given settings file with a new secret key.
    """
    with open(settings_path, "r+") as fh:
        lines = [line for line in fh if not re.match("^ *SECRET_KEY", line)]
        lines.append("SECRET_KEY = %r\n" % generate_secret_key())
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
    models.db.create_all()


@cli.command()
def secretkey():
    """
    Update the secret key in a settings file.
    """
    replace_secret_key(os.environ["THIRDPLACE_SETTINGS"])


@cli.command()
def run():
    """
    Run the development server.
    """
    views.app.run()


if __name__ == "__main__":
    cli()
