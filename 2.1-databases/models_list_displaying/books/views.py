import datetime

from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books_objects = Book.objects.all()
    books = [{'name': b.name, 'author': b.author, 'pub_date': b.pub_date.strftime('%Y-%m-%d')} for b in books_objects]
    context = {'books': books}
    return render(request, template, context)


def books_pagi(request, pub_date):
    template = 'books/book_pagi.html'
    all_books_obj = Book.objects.all()
    pub_date_list = sorted(list(set([d.pub_date for d in all_books_obj])))  # С помощью set удалили одинаковые даты
    max_index = len(pub_date_list) - 1
    try:
        select_date = datetime.datetime.strptime(pub_date, '%Y-%m-%d').date()
        index_date = pub_date_list.index(select_date)
    except ValueError:
        # если в запросе неверный формат даты или нет ни одной записи по данной дате, то переход в общий каталог
        return redirect('books')
    pre_date = None
    next_date = None
    if index_date != 0:
        pre_date = str(pub_date_list[index_date - 1].strftime('%Y-%m-%d'))
    if index_date != max_index:
        next_date = str(pub_date_list[index_date + 1].strftime('%Y-%m-%d'))
    books_obj = all_books_obj.filter(pub_date=select_date)
    context = {'books': books_obj, 'pub_date': pub_date, 'pre_date': pre_date, 'next_date': next_date}
    return render(request, template, context)




