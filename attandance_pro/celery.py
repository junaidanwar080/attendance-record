from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from celery.schedules import crontab

# Set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attandance_pro.settings')

app = Celery('attandance_pro')

# Load task modules from all registered Django app configs
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in installed Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'upload_attendance_every_day_at_8_pm': {  # Change to reflect the task's frequency
        'task': 'attandance.tasks.upload_task',
        'schedule': crontab(hour=20, minute=0),  
        'args': (r'D:/project/attandance_pro/attendance-record/attendance-record/ICT.xlsx', None, None),  # Update file path
    },
}

# Redis server address (ensure this is the same as CELERY_BROKER_URL)
app.conf.broker_url = 'redis://127.0.0.1:6379'
app.conf.result_backend = 'redis://127.0.0.1:6379'

# Additional Celery settings
app.conf.accept_content = ['application/json']
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.timezone = 'Asia/Karachi'

# celery -A attandance_pro  worker -l info
# celery -A attandance_pro  beat -l info 
