from django import template

register = template.Library()  # если мы не зарегистрируем наши фильтры, то Django никогда не узнает, где именно их искать и фильтры потеряются

@register.filter(name='cenzor')  # регистрируем наш фильтр под именем multiply, чтоб django понимал, что это именно фильтр, а не простая функция
def cenzor(value):  # первый аргумент здесь это то значение, к которому надо применить фильтр, второй аргумент — это аргумент фильтра, т. е. примерно следующее будет в шаблоне value|multiply:arg
    VOC = ['хуй', 'хуев', 'пизд', 'ебать', 'бляд']
    for i in VOC:
        value = value.replace(i, i[0] + '*' * (len(i) - 2) + i[len(i) - 1:])
    return value

