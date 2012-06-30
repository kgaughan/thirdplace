"""Initialises shared objects and datastructures."""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_envvar('THIRDPLACE_SETTINGS', silent=False)
db = SQLAlchemy(app)
