from flask_security import RegisterFormV2
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, length


class RegisterUser(RegisterFormV2):
    name = StringField(
        "Name",
        validators=[DataRequired(), length(max=64)],
    )


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
