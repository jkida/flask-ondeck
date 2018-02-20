from app.celery.main import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task(bind=True)
def add(self, x, y):
    logger.info(self.__dict__)
    return x + y


# Add new schedule

