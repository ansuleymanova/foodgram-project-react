from rest_framework import filters, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Subscription, User
from .serializers import CustomUserSerializer


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'id'

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        else:
            serializer = self.get_serializer(request.user)

        return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def subscribe(request, user_id):
    if request.method == 'GET':
        author = User.objects.get(id=user_id)
        subscriber = request.user
        Subscription.objects.create(author=author, subscriber=subscriber)
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        Subscription.objects.get(author_id=user_id,
                                 subscriber_id=request.user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def subscriptions(request):
    return Subscription.objects.filter(subscriber_id=request.user.id)