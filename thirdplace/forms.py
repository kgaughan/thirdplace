from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, length


class CreateForum(Form):

    forum = StringField('Create a new forum',
                        validators=[DataRequired(),
                                    length(max=128)])


class CreateTopic(Form):

    topic = StringField('Topic title',
                        validators=[DataRequired(),
                                    length(max=128)])

    post = TextAreaField('')


class Post(Form):

    post = TextAreaField('Respond')
