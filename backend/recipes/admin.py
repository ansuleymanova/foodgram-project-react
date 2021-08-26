from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', )
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)


class RecipeAdmin(admin.ModelAdmin):
    def favorites(self, recipe):
        return Favorite.objects.filter(recipe_id=recipe.id).count()

    list_display = ('name', 'author', 'favorites')
    search_fields = ('name', 'author')
    list_filter = ('author', 'name')
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ('user', )
    empty_value_display = '-пусто-'


admin.site.register(ShoppingCart, ShoppingCartAdmin)
