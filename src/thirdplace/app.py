"""Initialises shared objects and datastructures."""

from flask import Flask

from . import forum, models

_app = None


def __getattr__(name):
    global _app  # noqa: PLW0603
    if name == "app":
        if _app is None:
            _app = create_app()
        return _app
    raise AttributeError(name)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(SQLALCHEMY_TRACK_MODIFICATIONS=False)
    app.config.from_envvar("THIRDPLACE_SETTINGS", silent=False)
    app.register_blueprint(forum.forum)
    models.db.init_app(app)
    models.security.init_app(app, models.user_datastore)
    return app
