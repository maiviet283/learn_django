from celery import shared_task
import time

@shared_task
def slow_add(x, y):
    time.sleep(3)
    return x + y