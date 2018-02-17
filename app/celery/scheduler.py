from app.celery.main import app
from app.celery.tasks import add

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(5.0, add.s(1, 2), name='1 plus 2')