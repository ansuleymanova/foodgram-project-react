from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'name', 'color', 'slug']
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'name', 'measurement_unit']
        model = Ingredient


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(),
                                            source="ingredient.id")
    name = serializers.CharField(read_only=True,
                                 source="ingredient.name")
    measurement_unit = serializers.CharField(
        read_only=True,
        source="ingredient.measurement_unit")

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True,
                                             source='ingredientrecipe_set')
    tags = TagSerializer(Tag, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'tags', 'ingredients',
                  'name', 'image', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        if Favorite.objects.filter(recipe_id=recipe.id,
                                   user_id=user.id).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        if user.shoppingcart.recipes.filter(id=recipe.id).exists():
            return True
        return False


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = IngredientRecipeSerializer(many=True,
                                             source='ingredientrecipe_set')
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ['ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time']

    @transaction.atomic
    def create(self, validated_data):
        context = self.context['request']
        ingredients = validated_data.pop("ingredientrecipe_set")
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=context.user,
                                       **validated_data)
        recipe.tags.set(tags)
        ingredients_req = context.data['ingredients']
        ingredient_list = []
        for ingredient in ingredients_req:
            ingredient_list.append(IngredientRecipe(
                recipe=recipe,
                # здесь все равно приходится отправлять запрос в цикле,
                # не понимаю, можно ли сделать иначе
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount']))
        IngredientRecipe.objects.bulk_create(ingredient_list)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        context = self.context['request']
        ingredients = validated_data.pop("ingredientrecipe_set")
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.tags.set(tags)
        IngredientRecipe.objects.filter(recipe_id=instance.id).delete()
        ingredients_req = context.data['ingredients']
        ingredient_list = []
        for ingredient in ingredients_req:
            ingredient_list.append(IngredientRecipe(
                recipe=instance,
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount']))
        IngredientRecipe.objects.bulk_create(ingredient_list)
        return instance

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance)
        serializer.context['request'] = self.context['request']
        return serializer.data
