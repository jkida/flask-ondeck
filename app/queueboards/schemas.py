import marshmallow
from app.extensions import db, ma
from app.helpers import TimeRangeModelConverter
from .models import QueueBoard, QueueBoardSchedule


class QueueBoardScheduleSchema(ma.ModelSchema):
    class Meta:
        model = QueueBoardSchedule
        sqla_session = db.session
        strict = True
        model_converter = TimeRangeModelConverter


    # @marshmallow.post_load
    # def make_instance(self, data):
    #     return data


class QueueBoardSchema(ma.ModelSchema):
    schedule = marshmallow.fields.Nested(QueueBoardScheduleSchema)
    class Meta:
        model = QueueBoard
        sqla_sesssion = db.session
        strict = True

    # @marshmallow.post_load
    # def make_instance(self, data):
    #     return data