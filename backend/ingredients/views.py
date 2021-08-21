from rest_framework import filters, viewsets

from users.permissions import IsAdminOrReadOnly

from .models import Ingredient
from .serializers import IngredientSerializer


class QueryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    pagination_class = None
    search_fields = ['name']
    http_method_names = ['get']


class IngredientViewSet(QueryViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
