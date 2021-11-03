from django.views.generic import \
    ListView, DetailView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД

from .models import News


class NewsList(ListView):
    model = News  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'all_news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = News.objects.order_by('-news_create_time')

class NewsDetail(DetailView):
    model = News  # указываем модель, объекты которой мы будем выводить
    template_name = 'news_.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будет лежать одна новость
    context_object_name = 'one_news'  # это имя списка, в котором будут лежать один объект, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон


