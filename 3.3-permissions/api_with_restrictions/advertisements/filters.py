from django_filters import rest_framework as filters, ChoiceFilter, DateFromToRangeFilter, CharFilter

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    status = ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    created_at = DateFromToRangeFilter()
    updated_at = DateFromToRangeFilter()
    creator = CharFilter()

    class Meta:
        model = Advertisement
        fields = ['status', 'created_at', 'updated_at', 'creator']