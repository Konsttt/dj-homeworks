import datetime
import os

from django.http import HttpResponse
from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}'
    msg = f'<h1>Текущее время: {current_time}</h1>'
    return HttpResponse(msg)


def workdir_view(request):
    files_list = os.listdir('.')
    msg = ''
    for file in files_list:
        msg += f'<h3>{file}</h3>'
    return HttpResponse(msg)
