from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, length


class CreateForum(FlaskForm):
    forum = StringField(
        "Create a new forum",
        validators=[DataRequired(), length(max=128)],
    )


class CreateTopic(FlaskForm):
    topic = StringField(
        "Topic title",
        validators=[DataRequired(), length(max=128)],
    )

    post = TextAreaField("")


class Post(FlaskForm):
    post = TextAreaField("Respond")
