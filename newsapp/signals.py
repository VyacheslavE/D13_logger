from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import News


@receiver(post_save, sender=News)
def news_notify(sender, instance, created, **kwargs):
    send_mail(
        subject=instance.name,
        message=instance.news_text,
        from_email='vyachTest2021@yandex.ru',
        recipient_list=['vyacheslav.evlakhov@gmail.com']
    )


