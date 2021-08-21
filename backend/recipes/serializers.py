from rest_framework import serializers

from ingredients.serializers import IngredientSerializer
from tags.serializers import TagSerializer

from .models import Favorite, Recipe


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        fields = ['id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time']
        model = Recipe

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user__id=user.id,
                                           recipe__id=recipe.id).exists()
        return False

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        if user.is_authenticated:
            return user.shopping_cart.recipes.filter(id=recipe.id).exists()
        return False
