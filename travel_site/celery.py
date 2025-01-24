from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_site.settings')

app = Celery('travel_site')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

print(f"Celery tasks: {app.tasks.keys()}")


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
