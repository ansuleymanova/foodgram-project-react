from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User


class Recipe(models.Model):
    id = models.IntegerField(primary_key=True,
                             editable=False)
    name = models.CharField(max_length=200,
                            verbose_name='Название рецепта')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes')
    image = models.ImageField(upload_to='images/recipes',
                              max_length=100,
                              verbose_name='Иллюстрация')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(validators=[MinValueValidator(1), ],
                                       verbose_name='Время приготовления')
    pub_date = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(Ingredient)

    class Meta:
        ordering = ['-pub_date']


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='fans')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorite_recipes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')]


class ShoppingCart(models.Model):
    recipes = models.ManyToManyField(Recipe)
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='shopping_cart',
                                primary_key=True)
