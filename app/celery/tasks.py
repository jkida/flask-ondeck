from app.celery.main import app

@app.task
def add(x, y):
    print(app.conf.beat_schedule)
    return x + y


# Add new schedule

