from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, length


class CreateForum(Form):

    forum = StringField('Create a new forum',
                        validators=[DataRequired(),
                                    length(max=128)])
