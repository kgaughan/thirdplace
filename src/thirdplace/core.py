"""Initialises shared objects and datastructures."""

import bbcode
from flask import Flask

from . import gravatar

app = Flask("thirdplace")
app.config.update(SQLALCHEMY_TRACK_MODIFICATIONS=False)
app.config.from_envvar("THIRDPLACE_SETTINGS", silent=False)


app.jinja_env.filters.update(
    {"bbcode": bbcode.render_html, "gravatar": gravatar.gravatar},
)
