from app.celery.main import app
from celery.utils.log import get_task_logger
from .persistance.sqlalchemy_scheduler import dbsession as db
from app.models import QueueBoard
logger = get_task_logger(__name__)

@app.task(bind=True)
def add(self, x, y):
    logger.info(self.__dict__)
    return x + y

@app.task
def set_active_queue_board(*, queue_board_id, is_active):
    db.query(QueueBoard).filter(QueueBoard.id == queue_board_id)\
        .update({"is_active": is_active})
