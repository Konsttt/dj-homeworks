from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    # Поле для метки Черновик
    draft = models.BooleanField(default=False)
    # Поле связи m2m с таблицей Избранное
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Favorite', related_name='favorites_adv')


# Таблицу для Избранного (промежуточная таблица между Users и Advertisement)
class Favorite(models.Model):
    user_has_favor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    favor_adv = models.ForeignKey(Advertisement, on_delete=models.CASCADE)