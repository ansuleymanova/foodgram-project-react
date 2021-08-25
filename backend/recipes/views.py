from django.http.response import HttpResponse
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from users.pagination import PageNumberLimitPagination
from rest_framework.response import Response
from users.permissions import IsAdminOrReadOnly

from .models import (Recipe,
                     Tag, Ingredient, IngredientRecipe,
                     #Favorite
                     )
from .serializers import (RecipeWriteSerializer,
                          RecipeReadSerializer,
                          TagSerializer,
                          IngredientSerializer,
                          IngredientRecipeSerializer,
                          #FavoriteRecipeSerializer
                          )


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    http_method_names = ['get']
    lookup_field = 'id'


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    http_method_names = ['get']
    lookup_field = 'id'
    #search_fields = 


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = PageNumberLimitPagination
    serializer_class = RecipeWriteSerializer
