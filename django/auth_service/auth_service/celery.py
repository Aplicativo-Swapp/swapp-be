from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Setting the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')

app = Celery('auth_service')

# Reading config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks from all installed apps 
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')