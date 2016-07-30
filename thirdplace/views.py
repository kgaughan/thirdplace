from flask import render_template

from thirdplace import models
from thirdplace.core import app


@app.route("/")
def list_forums():
    return render_template('forums.html',
                           forums=models.Forum.query_all())
