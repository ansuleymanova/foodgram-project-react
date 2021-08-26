from django_filters import rest_framework

from .models import Recipe, Tag


class RecipeFilterSet(rest_framework.FilterSet):
    is_favorited = rest_framework.BooleanFilter(method='favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='in_shopping_cart')
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug', to_field_name='slug',
        queryset=Tag.objects.all())

    def favorited(self, queryset, name, value):
        favorites = queryset.filter(favorite__user_id=self.request.user.id)
        if value == 1:
            return favorites
        elif value == 0:
            return queryset.exclude(id__in=favorites)
        return queryset

    def in_shopping_cart(self, queryset, name, value):
        cart = queryset.filter(shoppingcart__user_id=self.request.user.id)
        if value == 1:
            return cart
        elif value == 0:
            return queryset.exclude(id__in=cart)
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags',
                  'is_favorited', 'is_in_shopping_cart']
