from django.contrib import admin

from .models import Recipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author')
    list_filter = ('author', 'name')
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
