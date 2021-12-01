from celery import shared_task
import time
from .models import News, Category
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_mail(mail, new_news, my_cat, url):
    print(f'{mail} - mail, {new_news} - news, {url} ')
    html_content = render_to_string('subcribers_letter_new_created.html',
                                    {
                                        'new_news': new_news,
                                        'ur': url

                                    },
                                    )
    # получаем наш html
    msg = EmailMultiAlternatives(
        subject=f'Новая статья в твоём разделе {my_cat}',
        body='',
        from_email='VyachTest2021@rambler.ru',
        to=mail,
    )
    msg.attach_alternative(html_content, 'text/html')  # добавляем html
    msg.send()


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


def send_mails():
    print('Hello from background task!')


@shared_task
def send_monday_mail():
    week_date = datetime.now() - timedelta(days=7)
    my_cats = Category.objects.all()

    for cat in my_cats:
        week_news = News.objects.filter(category = cat.id).filter(news_create_time__date__gte=week_date)
        all_subscribers = cat.subscribers.all()
        mails = []

        for one_sub in all_subscribers:
            mails.append(one_sub.email)

        # получаем наш html
        html_content = render_to_string('Week_news_to_subscribers.html',
                                    {'all_week_news': week_news,
                                     'cat': cat,
                                     }
                                    )

        # в конструкторе параметры писем
        msg = EmailMultiAlternatives(
            subject=f'Новости за неделю. Раздел: {cat} - {datetime.now().strftime("%Y-%M-%d")}',
            body='',
            from_email='VyachTest2021@rambler.ru',
            to=mails,  # перечень адресатов
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()




