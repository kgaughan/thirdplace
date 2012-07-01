import flask

from thirdplace.core import app
from thirdplace import models


@app.route('/')
def show_forums():
    forums = models.Forum.query_all()
    return flask.render_template('forums.html', forums=forums)


@app.route('/<int:forum_id>/')
def show_topics(forum_id):
    return ""


@app.route('/<int:forum_id>/<int:topic_id>/')
def show_posts(forum_id, topic_id):
    return ""


@app.route('/users/<int:user_id>/')
def show_user(user_id):
    return ""


@app.route('/users/<int:user_id>/posts/')
def show_user_posts(user_id):
    return ""
