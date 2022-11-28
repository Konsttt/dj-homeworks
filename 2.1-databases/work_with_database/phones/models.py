from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=30, unique=True, db_index=True)
    price = models.CharField(max_length=10)
    image = models.CharField(max_length=100)
    release_date = models.CharField(max_length=15)
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=50, verbose_name="URL")
