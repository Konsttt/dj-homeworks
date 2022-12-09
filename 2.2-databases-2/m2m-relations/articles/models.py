from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название раздела')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    article_tags = models.ManyToManyField(Tag, through='ArticleTag')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class ArticleTag(models.Model):  # Назвал класс изначально Scope, но были ошибки при related_name='scopes'. Переименовал класс - всё заработало.
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Раздел')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='scopes')
    is_main = models.BooleanField(verbose_name='Основной')

    class Meta:
        verbose_name = 'Тематика Статьи'
        verbose_name_plural = 'Тематики Статьи'
        ordering = ['-is_main', 'tag']