import datetime

from flask_security import RoleMixin, Security, SQLAlchemyUserDatastore, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from thirdplace.core import app

db = SQLAlchemy(app)


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("roles.id")),
)


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    # flask-security
    fs_uniquifier = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
    )

    roles = db.relationship(
        "Role",
        secondary=roles_users,
        backref=db.backref("users", lazy="dynamic"),
    )


class Post(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(
        db.Integer,
        db.ForeignKey("topics.topic_id"),
        index=True,
        nullable=False,
    )
    modified = db.Column(db.DateTime, nullable=False)
    posted = db.Column(db.DateTime, nullable=False)
    poster_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post = db.Column(db.Text, nullable=False)

    poster = db.relationship(
        "User",
        primaryjoin="Post.poster_user_id==User.id",
        backref=db.backref("posts", order_by=posted),
    )

    topic = db.relationship(
        "Topic",
        primaryjoin="Post.topic_id==Topic.topic_id",
        backref=db.backref("posts", order_by=posted),
    )

    def __init__(self, topic, post, poster):
        super().__init__()
        now = datetime.datetime.now(datetime.timezone.utc)
        self.topic = topic
        self.post = post
        self.poster = poster
        self.posted = now
        self.modified = now

    @classmethod
    def query_for_topic(cls, topic_id: int):
        return (
            cls.query.options(db.joinedload(cls.poster))
            .filter_by(topic_id=topic_id)
            .all()
        )


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class Topic(db.Model):
    __tablename__ = "topics"

    CLOSED = 0
    ACTIVE = 1
    STICKY = 2

    topic_id = db.Column(db.Integer, primary_key=True)
    forum_id = db.Column(db.Integer, db.ForeignKey("forums.forum_id"), nullable=False)
    latest_post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.post_id", use_alter=True, name="fk_latest"),
        nullable=True,
    )
    topic = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    latest_post = db.relationship(
        "Post",
        primaryjoin="Topic.latest_post_id==Post.post_id",
    )

    forum = db.relationship("Forum", backref=db.backref("topics", order_by=topic))

    post_count = db.column_property(
        db.select(func.count()).where(Post.topic_id == topic_id).scalar_subquery(),
        deferred=True,
    )

    def __init__(self, forum_id: int, topic: str, status):
        assert status in (self.CLOSED, self.ACTIVE, self.STICKY)
        super().__init__()
        self.forum_id = forum_id
        self.topic = topic
        self.status = status

    @classmethod
    def query_for_forum(cls, forum_id: int):
        return (
            cls.query.options(
                db.joinedload(cls.latest_post, Post.poster),
                db.undefer(cls.post_count),
            )
            .filter_by(forum_id=forum_id)
            .all()
        )


class Forum(db.Model):
    __tablename__ = "forums"

    forum_id = db.Column(db.Integer, primary_key=True)
    latest_post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.post_id", use_alter=True, name="fk_latest"),
        nullable=True,
    )
    forum = db.Column(db.String(128), nullable=False)

    latest_post = db.relationship(
        "Post",
        primaryjoin="Forum.latest_post_id==Post.post_id",
    )

    topic_count = db.column_property(
        db.select(func.count()).where(Topic.forum_id == forum_id).scalar_subquery(),
        deferred=True,
    )

    def __init__(self, forum: str):
        super().__init__()
        self.forum = forum

    @classmethod
    def query_all(cls):
        return cls.query.options(
            db.joinedload(cls.latest_post, Post.topic),
            db.joinedload(cls.latest_post, Post.poster),
            db.undefer(cls.topic_count),
        ).all()
