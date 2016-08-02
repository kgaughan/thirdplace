"""Initialises shared objects and datastructures."""

import bbcode
from flask import Flask


app = Flask('thirdplace')
app.config.update(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
app.config.from_envvar('THIRDPLACE_SETTINGS', silent=False)


app.jinja_env.filters['bbcode'] = bbcode.render_html
