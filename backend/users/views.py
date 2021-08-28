from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


from .models import Subscription, User
from .pagination import PageNumberLimitPagination
from .serializers import CustomUserSerializer, SubscriptionUserSerializer


class UserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberLimitPagination
    lookup_field = 'id'


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def subscribe(request, user_id):
    if request.method == 'GET':
        author = get_object_or_404(User, id=user_id)
        if author != request.user:
            Subscription.objects.create(author=author,
                                        subscriber=request.user)
            serializer =  SubscriptionUserSerializer(author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        raise serializers.ValidationError(
            'Нельзя подписаться на самого себя')
    elif request.method == 'DELETE':
        Subscription.objects.get(author_id=user_id,
                                 subscriber_id=request.user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def subscriptions(request):
    queryset = User.objects.filter(subscription__subscriber_id=request.user.id)
    serializer = SubscriptionUserSerializer(queryset, many=True)
    return Response(serializer.data)
