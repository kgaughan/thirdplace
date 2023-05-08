import http

import flask

from thirdplace import models
from thirdplace.core import app


@app.route("/")
def show_forums():
    forums = models.Forum.query_all()
    return flask.render_template("forums.html", forums=forums)


@app.route("/<int:forum_id>/")
def show_topics(forum_id: int):
    forum = models.Forum.query.get_or_404(forum_id).forum
    topics = models.Topic.query_for_forum(forum_id)
    return flask.render_template("topics.html", topics=topics, forum=forum)


@app.route("/<int:forum_id>/<int:topic_id>/")
def show_posts(forum_id: int, topic_id: int):
    topic = models.Topic.query.get_or_404(topic_id)
    if topic.forum_id != forum_id:
        flask.abort(http.NOT_FOUND)
    posts = models.Post.query_for_topic(topic_id)
    return flask.render_template(
        "posts.html",
        forum_id=forum_id,
        forum=topic.forum.forum,
        topic=topic.topic,
        posts=posts,
    )


@app.route("/users/<int:user_id>/")
def show_user(user_id: int):
    return ""


@app.route("/users/<int:user_id>/posts/")
def show_user_posts(user_id: int):
    return ""
