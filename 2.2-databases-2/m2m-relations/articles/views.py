from django.db.models import Prefetch
from django.shortcuts import render

from articles.models import Article, ArticleTag, Tag


def articles_list(request):
    template = 'articles/news.html'
    # object_list = Article.objects.all()  # Без prefetch_related 13 sql-запросов, 10мс
    # С prefetch_related именно через класс Prefetch кол-во запросов снизилось до 3, 4мс
    # Если бы не было сортировок по имени, дате и т.д., то можно было обойтись только простым .prefetch_related()
    # Первый Prefetch кэширует промежуточную таблицу ArticleTag
    # Второй вложенный Prefetch кэширует таблицу Tag
    object_list = Article.objects.prefetch_related(
        Prefetch('scopes', ArticleTag.objects.prefetch_related(Prefetch('tag', Tag.objects.all())))).all()

    context = {'object_list': object_list}

    return render(request, template, context)
