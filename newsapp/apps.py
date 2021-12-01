import redis
from django.apps import AppConfig


class NewsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsapp'

    def ready(self):
        import newsapp.signals
        from .views import BaseRegisterView
        from .tasks import send_mails
        from .scheduler import news_scheduler
        print('started!')

        news_scheduler.add_job(
            id='send_mails',
            func=send_mails,
            trigger='interval',
            seconds=300,
        )

        news_scheduler.start()


red = redis.Redis(
    host='redis-13542.c290.ap-northeast-1-2.ec2.cloud.redislabs.com',
    port='13542',
    password='jslNYCHhkmNgIXG9dseEBAdT3v4TviKH'
    )
