from thirdplace.core import db


class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(32), nullable=False, unique=True)
    pwd = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)


class Forum(db.Model):

    __tablename__ = 'forums'

    forum_id = db.Column(db.Integer, primary_key=True)
    latest_post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.post_id', use_alter=True, name='fk_latest'))
    forum = db.Column(db.String(128), nullable=False)


class Topic(db.Model):

    __tablename__ = 'topics'

    CLOSED = 0
    ACTIVE = 1
    STICKY = 2

    topic_id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(db.Integer, db.ForeignKey('forums.forum_id'))
    latest_post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.post_id', use_alter=True, name='fk_latest'))
    topic = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    forum = db.relationship(
        "Forum", backref=db.backref('topics', order_by=topic))


class Post(db.Model):

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))
    modified = db.Column(db.DateTime, nullable=False)
    posted = db.Column(db.DateTime, nullable=False)
    poster_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post = db.Column(db.Text, nullable=False)

    poster = db.relationship(
        "User", backref=db.backref('posts', order_by=posted))

    topic = db.relationship(
        "Topic", backref=db.backref('posts', order_by=posted))
