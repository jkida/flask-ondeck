from datetime import datetime as dt

from flask_apispec import marshal_with, use_kwargs as req_with, MethodResource as Resource, doc
from app.auth.jwt import jwt_require_all
from .models import (
    User,
    UserGroup,
    Schedule,
    GroupSchedule,
)
from app.models import QueueBoard
from .schemas import (
    UserSchema,
    UserLoginSchema,
    UserGroupSchema,
    ScheduleSchema,
    GroupScheduleSchema,
)
from .controllers import (
    query_active_queues
)
from app.extensions import api, db, docs
from app.helpers import authdoc, verify_password
from flask_login import login_user
from app.auth.redis_session import LoggedInUser
from flask import abort, current_app


@docs.register
@doc(description='User Login', tags=['User'])
@api.route('/user/login')
class UserLoginAPI(Resource):

    @marshal_with(UserSchema)
    @req_with(UserLoginSchema)
    def post(self, username, password):
        user = User.query.filter(username==username).first_or_404()
        if verify_password(password, user.password):
            login_user(LoggedInUser(user))

            # Add user to QueueBoards
            qboards = query_active_queues(user).filter(
                db.not_(QueueBoard.members.contains([{'user_id': user.id}]))
            )
            current_app.logger.info("Loging In User {}".format(user))
            for qboard in qboards:
                current_app.logger.error("Adding user {} to queue {}".format(user.full_name, qboard.name))
                qboard.members.append({'user_id': user.id, 'added_at': dt.now().isoformat()})
            db.session.commit()

            return user
        abort(401)


@docs.register
@authdoc(description='Users Description', tags=['User'])
@api.route('/user')
@jwt_require_all
class UsersAPI(Resource):

    @marshal_with(UserSchema(many=True))
    def get(self):
        return User.query.all()

    @marshal_with(UserSchema)
    @req_with(UserSchema)
    def post(self, **data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user


@docs.register
@authdoc(description='User Description', tags=['User'])
@api.route('/user/<int:user_id>')
@jwt_require_all
class UserAPI(Resource):

    """An API to get, update or delete a user. """

    @marshal_with(UserSchema)
    def get(self, user_id):
        return User.query.get_or_404(user_id)

    @marshal_with(UserSchema)
    @req_with(UserSchema(partial=True))
    def put(self, user_id, **data):
        print(data)
        user = User.query.get_or_404(user_id)
        user.update(**data)
        db.session.commit()
        return user


@docs.register
@authdoc(description='User Groups Description', tags=['User Group'])
@api.route('/role')
@jwt_require_all
class UserGroupsAPI(Resource):

    @marshal_with(UserGroupSchema(many=True))
    def get(self):
        return UserGroup.query.all()

    @marshal_with(UserGroupSchema)
    @req_with(UserGroupSchema)
    def post(self, **data):
        group = UserGroup(**data)
        db.session.add(group)
        db.session.commit()
        return group


@docs.register
@authdoc(description='User Group Description', tags=['User Group'])
@api.route('/user-group/<int:user_group_id>')
@jwt_require_all
class UserGroupAPI(Resource):

    @marshal_with(UserGroupSchema)
    def get(self, user_group_id):
        return UserGroup.query.get_or_404(user_group_id)

    @marshal_with(UserGroupSchema)
    @req_with(UserGroupSchema)
    def put(self, user_group_id, **data):
        group = UserGroup.query.get_or_404(user_group_id)
        group.update(**data)
        db.session.commit()
        return group


@docs.register
@authdoc(description='Schedules', tags=['Schedules'])
@api.route('/schedule')
@jwt_require_all
class SchedulesAPI(Resource):

    @marshal_with(ScheduleSchema(many=True))
    def get(self):
        return Schedule.query.all()

    @marshal_with(ScheduleSchema)
    @req_with(ScheduleSchema)
    def post(self, **data):
        schedule = Schedule(**data)
        db.session.add(schedule)
        db.session.commit()
        return schedule


@docs.register
@authdoc(description='GroupSchedules', tags=['GroupSchedules'])
@api.route('/group-schedule')
@jwt_require_all
class GroupSchedulesAPI(Resource):

    @marshal_with(GroupScheduleSchema(many=True))
    def get(self):
        return GroupSchedule.query.all()

    @marshal_with(GroupScheduleSchema)
    @req_with(GroupScheduleSchema)
    def post(self, **data):
        schedule = GroupSchedule(**data)
        db.session.add(schedule)
        db.session.commit()
        return schedule

@docs.register
@authdoc(description='GroupSchedules', tags=['GroupSchedules'])
@api.route('/group-schedule/<int:schedule_id>')
@jwt_require_all
class GroupScheduleAPI(Resource):
    @marshal_with(GroupScheduleSchema)
    def get(self, schedule_id):
        return GroupSchedule.query.get_or_404(schedule_id)

    @marshal_with(GroupScheduleSchema)
    @req_with(GroupScheduleSchema)
    def put(self, schedule_id, **data):
        schedule = GroupSchedule.query.get_or_404(schedule_id)
        schedule.update(**data)
        db.session.commit()
        return schedule
