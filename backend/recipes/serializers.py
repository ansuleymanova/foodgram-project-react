from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from .models import (Recipe, 
                     Tag, Ingredient, IngredientRecipe
                     )


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

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'tags', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')


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

    def create(self, validated_data):
        context = self.context['request']
        ingredients = validated_data.pop("ingredientrecipe_set")
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=context.user,
                                       **validated_data)
        recipe.tags.set(tags)
        ingredients_req = context.data['ingredients']
        for ingredient in ingredients_req:
            print(context.data['ingredients'][0])
            ingredient_model = Ingredient.objects.get(id=ingredient['id'])
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient_model,
                amount=ingredient['amount'],
            )
        return recipe

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance)
        return serializer.data


class MinifiedRecipeSerializer():

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
