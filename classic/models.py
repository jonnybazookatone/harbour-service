"""
Models use to define the database
The database is not initiated here, but a pointer is created named db. This is
to be passed to the app creator within the Flask blueprint.
"""

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    """
    Users table
    Foreign-key absolute_uid is the primary key of the user in the user
    database microservice.
    """
    __bind_key__ = 'imports'
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    absolute_uid = db.Column(db.Integer, unique=True, nullable=False)
    classic_mirror = db.Column(db.String(32), nullable=False)
    classic_cookie = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<User: id {0}, absolute_uid {1}, classic_cookie "{2}">'\
            .format(self.id, self.absolute_uid, self.classic_cookie)
