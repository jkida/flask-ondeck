from flask_apispec import marshal_with, use_kwargs as req_with, MethodResource as Resource
from app.auth.jwt import AuthResource, jwt_require_all, jwt_required
from .models import (
    User, UserSchema,
    Role, RoleSchema,
    Schedule, ScheduleSchema
)
from app.extensions import api, db, docs
from app.helpers import authdoc


@docs.register
@authdoc(description='Users Description', tags=['Queues'])
@api.route('/user')
@jwt_require_all
class QueuesAPI(AuthResource):

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