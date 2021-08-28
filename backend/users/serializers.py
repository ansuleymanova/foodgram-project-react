from django.db.models.aggregates import Count
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from recipes.models import Recipe

from .models import Subscription, User


class MinifiedRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        extra_kwargs = {'email': {'required': False},
                        'first_name': {'max_length': 150},
                        'password': {'max_length': 150}
                        }

    def get_is_subscribed(self, author) -> bool:
        subscriber = self.context['request'].user
        return Subscription.objects.filter(
            author__id=author.id,
            subscriber__id=subscriber.id).exists()


class SubscriptionUserSerializer(UserSerializer):
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name',
                  'recipes', 'recipes_count')
        extra_kwargs = {'email': {'required': False},
                        'first_name': {'max_length': 150},
                        'password': {'max_length': 150}
                        }

    def get_recipes(self, user, limit=None):
        if not limit:
            limit = 10
        recipes = user.recipes.all()[:limit]
        return MinifiedRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, user) -> int:
        queryset = User.objects.annotate(recipe_count=Count('recipes'))
        return queryset.get(id=user.id).recipe_count

