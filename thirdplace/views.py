import http.client

from flask import abort, redirect, render_template, request, url_for
from flask_security.core import current_user

from thirdplace import forms, models
from thirdplace.core import app


@app.route("/", methods=["GET", "POST"])
def show_forums():
    if request.method == "POST" and not current_user.is_authenticated:
        return app.login_manager.unauthorized()

    form = forms.CreateForum()
    if form.validate_on_submit():
        forum = models.Forum(form.forum.data)
        models.db.session.add(forum)
        models.db.session.commit()
        return redirect(url_for("show_topics", forum_id=forum.forum_id))

    return render_template("forums.html", forums=models.Forum.query_all(), form=form)


@app.route("/<int:forum_id>/", methods=["GET", "POST"])
def show_topics(forum_id: int):
    if request.method == "POST" and not current_user.is_authenticated:
        return app.login_manager.unauthorized()

    form = forms.CreateTopic()
    if form.validate_on_submit():
        topic = models.Topic(forum_id, form.topic.data, models.Topic.ACTIVE)
        post = models.Post(topic, form.post.data, poster=current_user)
        models.db.session.add(topic)
        models.db.session.add(post)
        models.db.session.flush()
        topic.latest_post = post
        topic.forum.latest_post = post
        models.db.session.add(topic)
        models.db.session.commit()

        return redirect(
            url_for("show_posts", forum_id=forum_id, topic_id=topic.topic_id)
        )

    return render_template(
        "topics.html",
        forum=models.Forum.query.get(forum_id),
        topics=models.Topic.query_for_forum(forum_id),
        form=form,
    )


@app.route("/<int:forum_id>/<int:topic_id>/", methods=["GET", "POST"])
def show_posts(forum_id: int, topic_id: int):
    if request.method == "POST" and not current_user.is_authenticated:
        return app.login_manager.unauthorized()

    topic = models.Topic.query.get(topic_id)
    if forum_id != topic.forum.forum_id:
        abort(http.client.NOT_FOUND)

    form = forms.Post()
    if form.validate_on_submit():
        post = models.Post(topic, form.post.data, poster=current_user)
        models.db.session.add(post)
        models.db.session.flush()
        topic.latest_post = post
        topic.forum.latest_post = post
        models.db.session.add(topic)
        models.db.session.commit()

        return redirect(
            (
                url_for("show_posts", forum_id=forum_id, topic_id=topic_id)
                + f"#p{post.post_id}"
            )
        )

    return render_template(
        "posts.html",
        topic=topic,
        posts=models.Post.query_for_topic(topic_id),
        form=form,
    )


@app.route("/users/<int:user_id>")
def show_user(user_id: int):
    pass
