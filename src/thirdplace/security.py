from flask_security.core import Security
from flask_security.datastore import SQLAlchemyUserDatastore

from . import models

user_datastore = SQLAlchemyUserDatastore(models.db, models.User, models.Role)
security = Security(app, user_datastore)
