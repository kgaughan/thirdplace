from sqlalchemy.sql import func

from thirdplace.core import db


class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(32), nullable=False, unique=True)
    pwd = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False)


class Post(db.Model):

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(
        db.Integer,
        db.ForeignKey('topics.topic_id'),
        nullable=False)
    modified = db.Column(db.DateTime, nullable=False)
    posted = db.Column(db.DateTime, nullable=False)
    poster_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.user_id'),
        nullable=False)
    post = db.Column(db.Text, nullable=False)

    poster = db.relationship(
        'User',
        primaryjoin='Post.poster_user_id==User.user_id',
        backref=db.backref('posts', order_by=posted))

    topic = db.relationship(
        'Topic',
        primaryjoin='Post.topic_id==Topic.topic_id',
        backref=db.backref('posts', order_by=posted))

    @classmethod
    def query_for_topic(cls, topic_id):
        return cls.query.options(db.joinedload_all(cls.poster)).all()


class Topic(db.Model):

    __tablename__ = 'topics'

    CLOSED = 0
    ACTIVE = 1
    STICKY = 2

    topic_id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(
        db.Integer,
        db.ForeignKey('forums.forum_id'),
        nullable=False)
    latest_post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.post_id', use_alter=True, name='fk_latest'),
        nullable=True)
    topic = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    latest_post = db.relationship(
        'Post',
        primaryjoin='Topic.latest_post_id==Post.post_id')

    forum = db.relationship(
        'Forum', backref=db.backref(
            'topics', order_by=topic))

    post_count = db.column_property(
        db.select([func.count()]).where(Post.topic_id == topic_id),
        deferred=True)

    @classmethod
    def query_for_forum(cls, forum_id):
        return cls.query.options(db.joinedload_all(
            cls.latest_post, Post.poster
        ), db.undefer(
            'post_count'
        )).all()


class Forum(db.Model):

    __tablename__ = 'forums'

    forum_id = db.Column(db.Integer, primary_key=True)
    latest_post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.post_id', use_alter=True, name='fk_latest'),
        nullable=True)
    forum = db.Column(db.String(128), nullable=False)

    latest_post = db.relationship(
        'Post',
        primaryjoin='Forum.latest_post_id==Post.post_id')

    topic_count = db.column_property(
        db.select([func.count()]).where(Topic.forum_id == forum_id),
        deferred=True)

    @classmethod
    def query_all(cls):
        return cls.query.options(db.joinedload_all(
            cls.latest_post, Post.topic
        ), db.joinedload_all(
            cls.latest_post, Post.poster
        ), db.undefer(
            'topic_count'
        )).all()
