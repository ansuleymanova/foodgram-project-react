from users.permissions import IsAuthorAdminOrReadOnly
from rest_framework import filters, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Subscription, User
from .serializers import (CustomUserSerializer,
                          SubscriptionUserSerializer
                          )
from .pagination import PageNumberLimitPagination
from djoser.views import UserViewSet


class UserViewSet(UserViewSet):
    permission_classes = [IsAuthorAdminOrReadOnly]
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberLimitPagination


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def subscribe(request, user_id):
    if request.method == 'GET':
        author = User.objects.get(id=user_id)
        Subscription.objects.create(author=author,
                                    subscriber=request.user)
        serializer =  SubscriptionUserSerializer(author)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        Subscription.objects.get(author_id=user_id,
                                 subscriber_id=request.user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def subscriptions(request):
    return Response(SubscriptionUserSerializer(request.user.subscriptions).data)
