from django.db import models
from django.core.validators import MinValueValidator
#from newsapp.models import *

#  создаём категорию, к которой будет привязываться новость
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # названия категорий тоже не должны повторяться

    def __str__(self):
        return f'{self.name.title()}'


# Создаём модель новость
class News(models.Model):
    news_create_time = models.DateTimeField(auto_now_add=True)
    news_text = models.TextField(default="None")
    name = models.CharField(
        max_length=100,
        unique=True,  # названия не должны повторяться
    )

    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='all_news',  # все новости в категории будут доступны через поле news
    )

    def __str__(self):
        return f'{self.name.title()}: {self.news_text[:50]}'




