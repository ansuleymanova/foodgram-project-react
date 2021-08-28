from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200,
                             null=True,
                             unique=True)
    slug = models.SlugField(max_length=200,
                            unique=True,
                            null=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes')
    image = models.ImageField(blank=False)
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(validators=[
        MinValueValidator(0), ])
    pub_date = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    ingredients = models.ManyToManyField(Ingredient)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.DO_NOTHING)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.DO_NOTHING)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(0), ],
                                         null=True,
                                         blank=True)


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')]


class ShoppingCart(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    recipes = models.ManyToManyField(Recipe)


@receiver(post_save, sender=get_user_model())
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(user=instance)
