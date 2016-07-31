"""Initialises shared objects and datastructures."""

from flask import Flask


app = Flask('thirdplace')
app.config.update(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
app.config.from_envvar('THIRDPLACE_SETTINGS', silent=False)
