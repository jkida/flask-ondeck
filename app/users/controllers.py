from app.extensions import db
from app.models import QueueBoard, User, UserGroup, QueueBoardSchedule

def query_active_queues(user):
    q = (db.session.query(QueueBoard)
         .outerjoin(QueueBoardSchedule, QueueBoardSchedule.id == QueueBoard.schedule_id)
         .outerjoin(UserGroup, UserGroup.id == QueueBoardSchedule.user_group_id)
         .outerjoin(User, User.user_group_id == UserGroup.id)
         .filter(User.id == user.id)
         .filter(QueueBoard.is_active == True)
         .filter(db.not_(QueueBoard.members.contains([{'user_id': user.id}]))))

    return q



