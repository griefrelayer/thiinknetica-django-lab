import os

from celery import Celery
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletin_board.settings')

app = Celery('bulletin_board')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

interval_kwargs = {'days': 7}
interval = timedelta(**interval_kwargs)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    "do_every_three_minutes": {
        "task": 'main.tasks.mail_about_new_ads',
        'schedule': interval.total_seconds(),
        'args': (interval_kwargs,)
    }
}
