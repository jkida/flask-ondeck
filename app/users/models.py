# -*- coding: utf-8 -*-
import datetime as dt
import marshmallow
from marshmallow_sqlalchemy import ModelConverter
from app.extensions import db, ma
from app.helpers import SurrogatePK, reference_col, TIMERANGE
from flask_login import UserMixin


class UserGroup(db.Model, SurrogatePK):
    """A group for a user."""

    __tablename__ = 'user_group'
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', back_populates='user_group')
    schedules = db.relationship('GroupSchedule', back_populates='user_group')
    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(db.Model, SurrogatePK, UserMixin):
    """A user of the app."""

    __tablename__ = 'user'
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    active = db.Column(db.Boolean(), default=True)
    is_admin = db.Column(db.Boolean(), default=False)
    user_group_id = reference_col('user_group')
    user_group = db.relationship('UserGroup', back_populates='users')

    # def set_password(self, password):
    #     """Set password."""
    #     self.password = bcrypt.generate_password_hash(password)
    #
    # def check_password(self, value):
    #     """Check password."""
    #     return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


class Schedule(db.Model):

    __tablename__ = 'schedule'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    timezone = db.Column(db.String(), default='utc')
    trange = db.Column(TIMERANGE())
    _type = db.Column('type', db.String())



    __mapper_args__ = {
        'polymorphic_identity': 'schedule',
        'polymorphic_on': _type
    }


class GroupSchedule(Schedule):
    user_group_id = reference_col('user_group')
    queue_boards = db.relationship('QueueBoard', back_populates='schedule')

    user_group = db.relationship("UserGroup", back_populates='schedules')


    __mapper_args__ = {
        'polymorphic_identity': 'role_schedule'
    }

#### Schemas

