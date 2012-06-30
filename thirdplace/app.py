import flask

from thirdplace.core import app


@app.route('/')
def show_forums():
    return flask.render_template('forums.html')


@app.route('/<int:forum_id>/')
def show_forum(forum_id):
    return ""


@app.route('/<int:forum_id>/<int:topic_id>/')
def show_topic(forum_id, topic_id):
    return ""


@app.route('/users/<int:user_id>/')
def show_user(user_id):
    return ""


@app.route('/users/<int:user_id>/posts/')
def show_user_posts(user_id):
    return ""
