import http.client

from flask import abort, render_template

from thirdplace import models
from thirdplace.core import app


@app.route("/")
def show_forums():
    return render_template('forums.html',
                           forums=models.Forum.query_all())


@app.route("/<int:forum_id>/")
def show_topics(forum_id):
    return render_template('topics.html',
                           forum=models.Forum.query.get(forum_id),
                           topics=models.Topic.query_for_forum(forum_id))


@app.route("/<int:forum_id>/<int:topic_id>/")
def show_posts(forum_id, topic_id):
    topic = models.Topic.query.get(topic_id)
    if forum_id != topic.forum.forum_id:
        abort(http.client.NOT_FOUND)
    return render_template('posts.html',
                           topic=topic,
                           posts=models.Post.query_for_topic(topic_id))


@app.route("/users/<int:user_id>")
def show_user(user_id):
    pass
