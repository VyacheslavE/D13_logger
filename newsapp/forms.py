from django.forms import ModelForm
from .models import News


# Создаём модельную форму
class NewsForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = News
        fields = ['news_author', 'news_text', 'name', 'category' ]

