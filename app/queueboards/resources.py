from flask_apispec import marshal_with, use_kwargs as req_with, MethodResource as Resource
from app.auth.jwt import jwt_require_all
from .models import (
    QueueBoard
)
from .schemas import (
    QueueBoardSchema
)
from app.extensions import api, db, docs
from app.helpers import authdoc


@docs.register
@authdoc(description='QueueBoard Description', tags=['Queues'])
@api.route('/queueboard')
@jwt_require_all
class QueuesAPI(Resource):

    @marshal_with(QueueBoardSchema(many=True))
    def get(self):
        return QueueBoard.query.all()

    @marshal_with(QueueBoardSchema)
    @req_with(QueueBoardSchema)
    def post(self, **data):
        board = QueueBoard(**data)
        db.session.add(board)
        db.session.commit()
        return board