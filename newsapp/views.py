from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, TemplateView  # импортируем необходимые дженерики
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, mail_managers
from django.http import HttpResponse
from django.views import View
from .tasks import hello


from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
 #DetailView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД

from .models import News, Category, BaseRegisterForm, BasicSignupForm
from .filters import NewsFilter
from .forms import NewsForm
from django.db.models.signals import post_save


class IndexView(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')


# создаём функцию обработчик с параметрами под регистрацию сигнала
def notify_news_create(sender, instance, created, **kwargs):
    subject = f'{instance.suscribers_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.news_text,
    )
    print('subject ============== ', subject)


# коннектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию
post_save.connect(notify_news_create, sender=News)


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/base/'
    message = f'Congrats with successfull registration, {User.username}!'

    def post(self, request, *args, **kwargs):
        reg = BaseRegisterForm(
            first_name=request.POST['first_name'],
            message=request.POST['message'],
        )
        reg.save()

        # отправляем письмо

        send_mail(
            subject=f'{reg.first_name}',
            # имя клиента будет в теме письма
            message=reg.message,  # сообщение с кратким описанием проблемы
            from_email='VyachTest2021@rambler.ru',  # здесь указываете почту, с которой будете отправлять
            recipient_list=[reg.email] #["test9999999@meta.ua"]  # здесь список получателей
        )

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

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новость
            form.save()

        return super().get(request, *args, **kwargs)


# дженерик для получения одной новости
class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = News.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class NewsCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm
    permission_required = ('newsapp.add_news',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def form_validation(self, form):
        self.object = form.save()
        news_cat = self.request.POST['category']
        url = f'{self.object.get_absolute_url()}'
        my_subscribers = Category.objects.get(id=news_cat).subscribers.all()
        mail = []
        new_news = f'{self.object.text}'
        my_cat = f'{Category.objects.get(id=news_cat).category}'
        for subscriber in my_subscribers:
            mail.append(subscriber.email)
        send_mail.delay(mail, new_news, my_cat, url)  # вызываем таск
        return super().form_valid(form)


# дженерик для редактирования объекта новость
class NewsUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'news_create.html'
    form_class = NewsForm
    permission_required = ('newsapp.change_news',)


    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return News.objects.get(pk=id)


# дженерик для удаления новости
class NewsDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    queryset = News.objects.all()
    success_url = '/news/'
    permission_required = ('newsapp.delete_news',)

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


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/index/')


@login_required
def subscribe_me(request, news_category_id):
    user = request.user
    my_category = Category.objects.get(id=news_category_id)
    my_category.subscribers.add(user)
    return redirect(f'/subscribed/{news_category_id}')


