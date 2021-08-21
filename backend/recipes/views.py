from foodgram.settings import BASE_DIR, MEDIA_ROOT
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from users.permissions import IsAuthorAdminOrReadOnly

from .models import Recipe
from .serializers import RecipeSerializer


class QueryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['tags', 'is_favorited', 'author',
                        'is_in_shopping_cart']
    search_fields = ['name']
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'id'


class RecipeViewSet(QueryViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def shopping_cart(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'GET':
        shopping_cart = request.user.shopping_cart
        shopping_cart.add(recipe)
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        request.user.shopping_cart.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def download_shopping_cart(request):
    pass
