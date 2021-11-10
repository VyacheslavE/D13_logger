from django_filters import FilterSet
from .models import News


# создаём фильтр
class NewsFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = News
        fields = {'news_create_time': ['lte'],
                  'news_text': ['icontains'],
                  'name': ['icontains'],
                  'category': ['exact'],
                  'news_author__author_user__username': ['icontains'],
                  }  # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)

