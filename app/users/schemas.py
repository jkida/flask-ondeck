import marshmallow
from app.extensions import db, ma
from app.helpers import TimeRangeModelConverter
from .models import User, UserGroup, Schedule, GroupSchedule


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ('password',)
        sqla_sesssion = db.session
        strict = True

    # @marshmallow.post_load
    # def make_instance(self, data):
    #     return data


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

    # @marshmallow.post_load
    # def make_instance(self, data):
    #     return data


class ScheduleSchema(ma.ModelSchema):
    class Meta:
        model = Schedule
        strict = True
        sqla_session = db.session
        model_converter = TimeRangeModelConverter


    # @marshmallow.post_load
    # def make_instance(self, data):
    #     return data


class GroupScheduleSchema(ma.ModelSchema):
    class Meta:
        model = GroupSchedule
        strict = True
        sqla_session = db.session
        model_converter = TimeRangeModelConverter


    # @marshmallow.post_load
    # def make_instance(self, data):
    #     return data

