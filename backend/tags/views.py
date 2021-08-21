from rest_framework import viewsets

from users.permissions import IsAdminOrReadOnly

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None
    http_method_names = ['get']
    lookup_field = 'id'
