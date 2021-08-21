from djoser.serializers import UserSerializer
from rest_framework.serializers import SerializerMethodField

from .models import Subscription, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, author) -> bool:
        subscriber = self.context['request'].user
        return Subscription.objects.filter(
            author__id=author.id,
            subscriber__id=subscriber.id).exists()
