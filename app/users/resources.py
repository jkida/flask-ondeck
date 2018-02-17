from flask_apispec import marshal_with, use_kwargs as req_with, MethodResource as Resource, doc
from app.auth.jwt import jwt_require_all
from .models import (
    User, UserSchema, UserLoginSchema,
    Role, RoleSchema,
    Schedule, ScheduleSchema
)
from app.extensions import api, db, docs
from app.helpers import authdoc, verify_password
from flask_login import login_user
from app.auth.redis_session import LoggedInUser
from flask import abort


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
@authdoc(description='Users Description', tags=['User'])
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
@authdoc(description='Roles Description', tags=['Role'])
@api.route('/role')
@jwt_require_all
class RolesAPI(Resource):

    @marshal_with(RoleSchema(many=True))
    def get(self):
        return Role.query.all()

    @marshal_with(RoleSchema)
    @req_with(RoleSchema)
    def post(self, **data):
        role = Role(**data)
        db.session.add(role)
        db.session.commit()
        return role

@docs.register
@authdoc(description='Role Description', tags=['Role'])
@api.route('/role/<int:role_id>')
@jwt_require_all
class RoleAPI(Resource):

    @marshal_with(RoleSchema)
    def get(self, role_id):
        return Role.query.get_or_404(role_id)

    @marshal_with(RoleSchema)
    @req_with(RoleSchema)
    def put(self, role_id, **data):
        role = Role.query.get_or_404(role_id)
        role.update(**data)
        db.session.commit()
        return role


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
        db.session.commit()
        return schedule