"""Initialises shared objects and datastructures."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask('thirdplace')
app.config.update(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
app.config.from_envvar('THIRDPLACE_SETTINGS', silent=False)
db = SQLAlchemy(app)
