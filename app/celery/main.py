from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('app.celery',
             broker='amqp://guest@localhost//',
             # backend='amqp://',
             include=['app.celery.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)