from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')

# # Моя изначальная реализация.
# def show_catalog(request):
#     template = 'catalog.html'
#     sort_field = request.GET.get('sort')
#     if sort_field == 'name':
#         phone_objects = Phone.objects.all().order_by('name')
#     elif sort_field == 'min_price':
#         phone_objects = Phone.objects.all().order_by('price')
#     elif sort_field == 'max_price':
#         phone_objects = Phone.objects.all().order_by('price').reverse()
#     else:
#         phone_objects = Phone.objects.all()
#     context = {'phones': phone_objects}
#     return render(request, template, context)


# Игорь Мартюшев предложил следующий вариант с SORT_MAP
def show_catalog(request):
    SORT_MAP = {
    'name': 'name',
    'min_price': 'price',
    'max_price': '-price',  # Вот здесь интересно. "-" заменяет реверс, а "?" - случайным образом.  !!!!!!!!!!!!!!!
    }                       # https://docs.djangoproject.com/en/4.1/ref/models/querysets/           !!!!!!!!!!!!!!!
    template = 'catalog.html'
    sort_field = request.GET.get('sort')
    phones = Phone.objects.all()
    if sort_field:
        phone_objects = phones.order_by(SORT_MAP[sort_field])
    else:
        phone_objects = phones
    context = {'phones': phone_objects}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug)[0]  # [0] т.к. из БД по такому фильтру должна быть одна запись
    context = {'phone': phone}
    return render(request, template, context)