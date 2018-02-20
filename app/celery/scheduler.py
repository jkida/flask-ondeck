from app.celery.main import app
from app.celery.persistance.sqlalchemy_scheduler_models import (
    DatabaseSchedulerEntry,
    IntervalSchedule
)
from app.celery.persistance.sqlalchemy_scheduler import dbsession


# dse = DatabaseSchedulerEntry()
# dse.name = 'Simple add task 3 2'
# dse.task = 'app.celery.tasks.add'
# dse.arguments = '[3, 2]'  # json string
# dse.keyword_arguments = '{}'  # json string
# dse.interval = IntervalSchedule(period='seconds', every=3)
# dbsession.add(dse)
# dbsession.commit()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    pass
