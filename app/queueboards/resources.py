from flask_apispec import marshal_with, use_kwargs as req_with, MethodResource as Resource
from app.auth.jwt import jwt_require_all
from .models import (
    QueueBoard,
    QueueBoardSchedule
)
from .schemas import (
    QueueBoardSchema,
    QueueBoardScheduleSchema
)
from .controllers import (
    add_queue_board,
    update_schedule
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
        board = add_queue_board(**data)
        db.session.commit()
        return board

@docs.register
@authdoc(description='QueueBoard Description', tags=['Queues'])
@api.route('/queueboard/<int:queue_board_id>')
@jwt_require_all
class QueueAPI(Resource):

    @marshal_with(QueueBoardSchema(many=True))
    def get(self, queue_board_id):
        return QueueBoard.query.get_or_404(queue_board_id)

    @marshal_with(QueueBoardSchema)
    @req_with(QueueBoardSchema)
    def put(self, queue_board_id, **data):
        board = QueueBoard.query.get_or_404(queue_board_id)
        board.update(**data)
        db.session.commit()
        return board


## Schedules for queueboards should be created with a queueboard
# @docs.register
# @authdoc(description='Queue Board Schedules', tags=['QueueBoardSchedules'])
# @api.route('/queue-board-schedule')
# @jwt_require_all
# class QueueBoardSchedulesAPI(Resource):
#
#     @marshal_with(QueueBoardScheduleSchema(many=True))
#     def get(self):
#         return QueueBoardSchedule.query.all()
#
#     @marshal_with(QueueBoardScheduleSchema)
#     @req_with(QueueBoardScheduleSchema)
#     def post(self, **data):
#         schedule = QueueBoardSchedule(**data)
#         db.session.add(schedule)
#         db.session.commit()
#         return schedule


@docs.register
@authdoc(description='Queue Board Schedules', tags=['QueueBoardSchedules'])
@api.route('/queue-board-schedule/<int:schedule_id>')
@jwt_require_all
class QueueBoardScheduleAPI(Resource):
    @marshal_with(QueueBoardScheduleSchema)
    def get(self, schedule_id):
        return QueueBoardSchedule.query.get_or_404(schedule_id)

    @marshal_with(QueueBoardScheduleSchema)
    @req_with(QueueBoardScheduleSchema)
    def put(self, schedule_id, **data):
        schedule = QueueBoardSchedule.query.get_or_404(schedule_id)
        update_schedule(schedule, **data)
        db.session.commit()
        return schedule