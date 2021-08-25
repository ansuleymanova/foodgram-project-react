from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'recipes',
                views.RecipeViewSet,
                basename='recipes')
router.register(r'tags',
                views.TagViewSet,
                basename='tags')
router.register(r'ingredients',
                views.IngredientViewSet,
                basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    #path('recipes/<recipe_id>/shopping_cart/',
    #     views.shopping_cart,
    #     name='shopping_cart'),
    #path('recipes/download_shopping_cart/',
    #     views.download_shopping_cart,
    #     name='download_shopping_cart'),
    #path('recipes/<recipe_id>/favorite/',
    #     views.favorite,
    #     name='favorite')
]