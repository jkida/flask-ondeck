import marshmallow
from app.extensions import db, ma
from .models import QueueBoard

class QueueBoardSchema(ma.ModelSchema):
    class Meta:
        model = QueueBoard
        sqla_sesssion = db.session
        strict = True

    @marshmallow.post_load
    def make_instance(self, data):
        return data