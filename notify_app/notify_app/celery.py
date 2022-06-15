import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notify_app.settings')


app = Celery('notify_app')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()