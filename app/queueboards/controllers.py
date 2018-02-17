from app.models import User, Role, RoleQueueSchedule
from datetime import datetime as dt
from sqlalchemy.orm import contains_eager

def queueBoardState(session=None):
    if session is None:
        from app.extensions import db
        session = db.session

    q = (session.query(RoleQueueSchedule)
         .outerjoin(Role, Role.id == RoleQueueSchedule.role_id)
         .outerjoin(User, User.role_id == Role.id)
         .filter(RoleQueueSchedule.trange.contains(dt.now().time()))
         .options(contains_eager('role'), contains_eager('role.users')))
    return q