import marshmallow
from marshmallow_sqlalchemy import ModelConverter
from app.extensions import db, ma
from .models import User, UserGroup, Schedule
from app.helpers import TIMERANGE


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


class UserGroupSchema(ma.ModelSchema):
    class Meta:
        model = UserGroup
        strict = True
        sqla_session = db.session

    @marshmallow.post_load
    def make_instance(self, data):
        return data


class ScheduleSchema(ma.ModelSchema):
    tranges = marshmallow.fields.List(marshmallow.fields.List(marshmallow.fields.Time))
    class Meta:
        model = Schedule
        strict = True
        sqla_session = db.session
        model_converter = AppModelConverter


    @marshmallow.post_load
    def make_instance(self, data):
        return data