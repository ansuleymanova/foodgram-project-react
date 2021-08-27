from django.http.response import HttpResponse
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.pagination import PageNumberLimitPagination
from users.permissions import IsAdminOrReadOnly

from .filters import RecipeFilterSet
from .models import Favorite, Ingredient, IngredientRecipe, Recipe, Tag
from .serializers import (IngredientRecipeSerializer, IngredientSerializer, MinifiedRecipeSerializer,
                          RecipeWriteSerializer, TagSerializer)


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
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    pagination_class = PageNumberLimitPagination
    serializer_class = RecipeWriteSerializer
    filterset_class = RecipeFilterSet


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'GET':
        Favorite.objects.create(user=request.user, recipe=recipe)
        return Response(MinifiedRecipeSerializer(recipe).data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        favorite = Favorite.objects.get(user=request.user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def shopping_cart(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'GET':
        request.user.shoppingcart.recipes.add(recipe)
        return Response(MinifiedRecipeSerializer(recipe).data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        request.user.shoppingcart.recipes.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def download_shopping_cart(request):
    recipes = request.user.shoppingcart.recipes.all()
    queryset = IngredientRecipe.objects.filter(recipe_id__in=recipes)
    shopping_list = {}
    for ingredient in queryset:
        name = ingredient.ingredient.name
        amount = ingredient.amount
        if name in shopping_list:
            shopping_list[name] = shopping_list[name] + amount
        else:
            shopping_list[name] = amount
    plain_list = ''
    for item in shopping_list.keys():
        plain_list += f'{item}: {shopping_list[item]}\n'
    response = HttpResponse(plain_list, content_type='text/plain')
    filename = 'shopping_list.txt'
    response['Content-Disposition'] = ('attachment; filename={0}'.
                                       format(filename))
    return HttpResponse(response)
