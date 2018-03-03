import json
from app.extensions import db
from app.celery.persistance.sqlalchemy_scheduler_models import (
    DatabaseSchedulerEntry,
    CrontabSchedule,
)
from .models import QueueBoard
import datetime as dt

def add_scheduler(schedule):
    # Open
    dse_open = DatabaseSchedulerEntry()
    dse_open.name = '{}-{}'.format(schedule.name, 'Open')
    dse_open.task = 'app.celery.tasks.set_active_queue_board'
    dse_open.arguments = '[]'  # json string
    dse_open.keyword_arguments = json.dumps({"queue_board_id": schedule.queue_board.id,
                                             "is_active": True})
    dse_open.crontab = CrontabSchedule(hour=schedule.trange.lower.hour,
                                       minute=schedule.trange.lower.minute)
    dse_open.board_schedule_id = schedule.id
    db.session.add(dse_open)

    # Close
    dse_close = DatabaseSchedulerEntry()
    dse_close.name = '{}-{}'.format(schedule.name, 'Close')
    dse_close.task = 'app.celery.tasks.set_active_queue_board'
    dse_close.arguments = '[]'  # json string
    dse_close.keyword_arguments = json.dumps({"queue_board_id": schedule.queue_board.id,
                                              "is_active": False})
    dse_close.crontab = CrontabSchedule(hour=schedule.trange.upper.hour,
                                         minute=schedule.trange.upper.minute)
    dse_close.board_schedule_id = schedule.id
    db.session.add(dse_close)

    return (dse_open, dse_close)


def add_queue_board(**data):
    board = QueueBoard(**data)
    db.session.flush()
    board.is_active = dt.datetime.now().time() in board.schedule.trange
    db.session.add(board)
    db.session.flush()

    add_scheduler(board.schedule)
    return board


def update_schedule(schedule, **data):
    schedule.update(**data)
    schedule.queue_board
    crons = db.session.query(DatabaseSchedulerEntry)\
        .filter(DatabaseSchedulerEntry.board_schedule_id == schedule.id)\
        .all()

    for cron in crons:
        if cron.name.endswith('Open'):
            cron.crontab.hour = schedule.trange.lower.hour
            cron.crontab.minute = schedule.trange.lower.minute
        elif cron.name.endswith('Close'):
            cron.crontab.hour = schedule.trange.upper.hour
            cron.crontab.minute = schedule.trange.upper.minute

    schedule.queue_board.is_active = dt.datetime.now().time() in schedule.trange

    return schedule




