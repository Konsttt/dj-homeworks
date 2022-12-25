from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'draft')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        count_open = Advertisement.objects.filter(creator=self.context["request"].user, status='OPEN').count()
        if count_open >= 10 and self.context["request"].method == 'POST':
            raise ValidationError('У вас уже 10 открытых объявлений (это лимит).'
                                  'Вы можете закрыть старое объявление и только потом добавить новое.')
        elif count_open >= 10 and self.context["request"].method == 'PATCH' and data['status'] == 'OPEN':
            raise ValidationError('У вас уже 10 открытых объявлений (это лимит).'
                                  'Чтобы открыть это объявление, закройте любое другое объявление.')
        return data

    # # !!!
    # ##### Вот здесь вопрос в def validate(self, data):  правильно ли я доставал метод из request-а ?   ###
    # #####      self.context["request"].stream.method                                                   ###
    # #####  Слишком монструозно )))  В дебаге посмотрел, где лежит. Может легче способ есть?            ###