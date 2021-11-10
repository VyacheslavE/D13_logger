from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView  # импортируем необходимые дженерики
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
 #DetailView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД

from .models import News, Category
from .filters import NewsFilter
from .forms import NewsForm

class NewsList(ListView):
    model = News  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'all_news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-news_create_time']
    paginate_by = 5  # поставим постраничный вывод в один элемент
    form_class = NewsForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST
  #  queryset = News.objects.order_by('-news_create_time')

# class NewsDetail(DetailView):
#     model = News  # указываем модель, объекты которой мы будем выводить
#     template_name = 'news_.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будет лежать одна новость
#     context_object_name = 'one_news'  # это имя списка, в котором будут лежать один объект, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст

        context['categories'] = Category.objects.all()
        context['form'] = NewsForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


# дженерик для получения одной новости
class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = News.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class NewsCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm


# дженерик для редактирования объекта новость
class NewsUpdateView(UpdateView):
    template_name = 'news_create.html'
    form_class = NewsForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return News.objects.get(pk=id)


# дженерик для удаления новости
class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = News.objects.all()
    success_url = '/news/'

class Mysearch(ListView):
    model = News  # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'all_news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-news_create_time']
    paginate_by = 5  # поставим постраничный вывод в один элемент


    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context