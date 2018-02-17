# -*- coding: utf-8 -*-
import datetime as dt
import marshmallow
from marshmallow_sqlalchemy import ModelConverter
from app.extensions import db, ma
from sqlalchemy.orm import relationship
from app.helpers import SurrogatePK, reference_col, TIMERANGE
from sqlalchemy.dialects import postgresql
from flask_login import UserMixin

class Role(db.Model, SurrogatePK):
    """A role for a user."""

    __tablename__ = 'role'
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = relationship('User', back_populates='role')
    queue_schedules = relationship('RoleQueueSchedule', back_populates='role')

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
    role_id = reference_col('role')
    role = relationship('Role', back_populates='users')

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


class RoleQueueSchedule(Schedule):
    role_id = reference_col('role')
    queue_settings_id = reference_col('queue_setting')
    role = relationship(Role, back_populates='queue_schedules')
    __mapper_args__ = {
        'polymorphic_identity': 'role_schedule'
    }


class QueueSettings(db.Model, SurrogatePK):
    __tablename__ = 'queue_setting'

    max_on_deck = db.Column(db.Integer(), default=0)
    max_allowed_break = db.Column(db.Integer(), default=0)
    min_wait_time = db.Column(db.Integer(), default=0)
    max_duration = db.Column(db.Integer(), nullable=False)


#### Schemas

class AppModelConverter(ModelConverter):
    SQLA_TYPE_MAPPING = dict(
        list(ModelConverter.SQLA_TYPE_MAPPING.items()) +
        [(TIMERANGE, marshmallow.fields.Str)]
    )


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ('password',)
        sqla_sesssion = db.session
        strict = True

    @marshmallow.post_load
    def make_instance(self, data):
        return data


class UserLoginSchema(ma.Schema):
    username = ma.String(required=True)
    password = ma.String(required=True)

    class Meta:
        strict = True


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role
        strict = True
        sqla_session = db.session

    @marshmallow.post_load
    def make_instance(self, data):
        return data

class ScheduleSchema(ma.ModelSchema):

    # tranges = marshmallow.fields.List(marshmallow.fields.List(marshmallow.fields.Time))
    class Meta:
        model = Schedule
        strict = True
        sqla_session = db.session
        model_converter = AppModelConverter


    @marshmallow.post_load
    def make_instance(self, data):
        return data