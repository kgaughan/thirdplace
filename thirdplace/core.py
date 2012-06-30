"""Initialises shared objects and datastructures."""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask('thirdplace')
app.config.from_envvar('THIRDPLACE_SETTINGS', silent=False)
db = SQLAlchemy(app)
