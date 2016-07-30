from flask import render_template

from thirdplace import models
from thirdplace.core import app


@app.route("/")
def list_forums():
    return render_template('forums.html',
                           forums=models.Forum.query_all())


@app.route("/<int:forum_id>/")
def show_topics(forum_id):
    pass


@app.route("/<int:forum_id>/<int:topic_id>/")
def show_posts(forum_id, topic_id):
    pass


@app.route("/users/<int:user_id>")
def show_user(user_id):
    pass
