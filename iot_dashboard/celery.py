import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iot_dashboard.settings')
app = Celery('iot_dashboard')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()




