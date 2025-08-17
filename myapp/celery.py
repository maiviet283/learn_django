import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

app = Celery('myapp')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Tự động load task từ tất cả các app có tasks.py
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
