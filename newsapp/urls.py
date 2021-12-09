from django.urls import path, include
from django.views.decorators.cache import cache_page
from .views import NewsList, Mysearch, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView, IndexView,  \
    CategoryList, CategoryDetail, subscribe_me  # импортируем наше представление


urlpatterns = [
    # path — означает путь. В данном случае путь ко всем новостям у нас останется пустым, позже станет ясно, почему
    path('', cache_page(60)(NewsList.as_view())),
path('search/', Mysearch.as_view()), # news/search/
path('<int:pk>/', cache_page(10)(NewsDetailView.as_view()), name='news_detail'),  # Ссылка на просмотр одной новости
path('create/', NewsCreateView.as_view(), name='news_create'),  # Ссылка на создание новости
path('delete/<int:pk>', NewsDeleteView.as_view(), name='news_delete'),  # Ссылка на создание новости
path('create/<int:pk>', NewsUpdateView.as_view(), name='news_create'),  # Ссылка на редактирование новости
path('accounts/', include('allauth.urls')),
path('index/', IndexView.as_view(), name='index'),
path('base/', IndexView.as_view(), name='base'),
path('category/', cache_page(60*5)(CategoryList.as_view()), name='categories'),
path('category/<int:pk>', CategoryDetail.as_view(), name='category_detail'),



    # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
]