import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsapp.settings')

app = Celery('newsapp')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_news_mails_every_monday': {
        'task': 'newsapp.tasks.send_monday_mail',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

