from django.core.serializers import serialize
from django.http import HttpResponse
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite
from advertisements.permissions import IsOwnerOrAdminOrReadOnly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all().select_related('creator')
    serializer_class = AdvertisementSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdvertisementFilter
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdminOrReadOnly()]
        return []

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # Вывод своего Избранного
    @action(methods=['get'], detail=False)
    def favorites(self, request):
        favorites = Advertisement.objects.filter(favorite__user_has_favor=self.request.user)
        favorites_json = serialize('json', favorites)
        return HttpResponse(favorites_json, content_type="application/json")

    # Добавление не своего объявления в своё Избранное
    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def add_favorite(self, request, pk):
        if Favorite.objects.filter(favor_adv=pk, user_has_favor=self.request.user):
            return Response(f'Объявление №{pk} уже в вашем Избранном.')
        advertisement = Advertisement.objects.get(pk=pk)
        if advertisement.creator != self.request.user:
            Favorite.objects.create(user_has_favor=self.request.user, favor_adv=advertisement)
            return Response(f'Объявление №{pk} пользователя {advertisement.creator} добавлено в Избранное.')
        else:
            return Response('Информация: в Избранное можно добавлять только чужие объявления.')

    # Удаление своих объявлений (pk - это номер id-шник объявления, а не номер записи в промежуточной таблице).
    @action(methods=['delete'], detail=True, permission_classes=[IsAuthenticated])
    def del_favorite(self, request, pk):
        del_fav = Favorite.objects.filter(favor_adv=pk, user_has_favor=self.request.user)
        if del_fav:
            del_fav.delete()
            return Response(f'Объявление №{pk} удалено из Избранного.')
        else:
            return Response('Информация: Объявление не удалено. Проверьте номер объявления в url.')

    # Видимость черновиков: админы видят все черновики, юзеры только свои черновики, анонимы не видят черновиков.
    def get_queryset(self):
        queryset = Advertisement.objects.all().select_related('creator')
        if self.request.user.is_superuser:
            return queryset
        elif self.request.user.is_anonymous:
            return queryset.exclude(draft=True)
        else:
            return queryset.exclude(draft=True) | queryset.filter(creator=self.request.user, draft=True)
