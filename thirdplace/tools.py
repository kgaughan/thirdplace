import argh
import base64
import os
import re
import sys


import thirdplace.models


def generate_secret_key():
    """Generate a string suitable for use as a secret key."""
    # 48 is a multiple of both 6 and 8, thus won't leave rubbish at the
    # end of the key.
    return base64.b64encode(os.urandom(48))


def replace_secret_key(settings_path):
    """Update the given settings file with a new secret key."""
    with open(settings_path, 'r+') as fh:
        lines = []
        for line in fh:
            if not re.match('^ *SECRET_KEY', line):
                lines.append(line)
        lines.append("SECRET_KEY = '%s'\n" % generate_secret_key())
        fh.seek(0)
        fh.truncate()
        fh.writelines(lines)


@argh.command
def initdb():
    """Initialise the database."""
    thirdplace.models.db.create_all()


@argh.arg('path', help='settings file to update')
def secretkey(args):
    """Update the secret key in a settings file."""
    replace_secret_key(args.path)


def main():
    """Dispatcher for the tools."""
    parser = argh.ArghParser()
    parser.add_commands([initdb, secretkey])
    return parser.dispatch(add_help_command=True)


if __name__ == '__main__':
    sys.exit(main())
