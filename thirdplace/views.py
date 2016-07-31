import http.client

from flask import abort, render_template, request
from flask_security.core import current_user

from thirdplace import forms, models
from thirdplace.core import app


@app.route("/", methods=['GET', 'POST'])
def show_forums():
    if request.method == 'POST' and not current_user.is_authenticated:
        return app.login_manager.unauthorized()

    form = forms.CreateForum()
    if form.validate_on_submit():
        return "Hurray!"

    return render_template('forums.html',
                           forums=models.Forum.query_all(),
                           form=form)


@app.route("/<int:forum_id>/", methods=['GET', 'POST'])
def show_topics(forum_id):
    if request.method == 'POST' and not current_user.is_authenticated:
        return app.login_manager.unauthorized()

    return render_template('topics.html',
                           forum=models.Forum.query.get(forum_id),
                           topics=models.Topic.query_for_forum(forum_id))


@app.route("/<int:forum_id>/<int:topic_id>/", methods=['GET', 'POST'])
def show_posts(forum_id, topic_id):
    if request.method == 'POST' and not current_user.is_authenticated:
        return app.login_manager.unauthorized()

    topic = models.Topic.query.get(topic_id)
    if forum_id != topic.forum.forum_id:
        abort(http.client.NOT_FOUND)
    return render_template('posts.html',
                           topic=topic,
                           posts=models.Post.query_for_topic(topic_id))


@app.route("/users/<int:user_id>")
def show_user(user_id):
    pass
