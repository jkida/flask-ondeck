# -*- coding: utf-8 -*-
from app.extensions import db, ma
from app.helpers import SurrogatePK


class QueueBoard(db.Model, SurrogatePK):

    __tablename__ = 'queue_board'
    name = db.Column(db.String(80), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)  # opened/closed

    schedule_id = db.Column(db.Integer(), db.ForeignKey('schedule.id'))
    schedule = db.relationship('GroupSchedule', foreign_keys=schedule_id, back_populates='queue_boards')

    # settings
    max_on_deck = db.Column(db.Integer(), default=0)
    max_allowed_break = db.Column(db.Integer(), default=0)
    next_break_wait_time = db.Column(db.Integer(), default=0)
    max_duration = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<QueueBoard({name})>'.format(name=self.name)
