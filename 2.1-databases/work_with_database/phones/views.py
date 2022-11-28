from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_field = request.GET.get('sort')
    if sort_field == 'name':
        phone_objects = Phone.objects.all().order_by('name')
    elif sort_field == 'min_price':
        phone_objects = Phone.objects.all().order_by('price')
    elif sort_field == 'max_price':
        phone_objects = Phone.objects.all().order_by('price').reverse()
    else:
        phone_objects = Phone.objects.all()
    context = {'phones': phone_objects}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug)[0]  # [0] т.к. из БД по такому фильтру должна быть одна запись
    context = {'phone': phone}
    return render(request, template, context)