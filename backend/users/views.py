from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, status, generics
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
            serializer = SubscriptionUserSerializer(author)
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


# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def subscriptions(request):
#    queryset = User.objects.filter(subscription__subscriber_id=request.user.id)
#    paginator = PageNumberLimitPagination()
#    result_page = paginator.paginate_queryset(queryset, request)
#    serializer = SubscriptionUserSerializer(result_page,
#                                           many=True)
#    return Response(serializer.data)

class SubscriptionList(generics.ListAPIView):
    serializer_class = SubscriptionUserSerializer
    pagination_class = PageNumberLimitPagination
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = SubscriptionUserSerializer(queryset,
                                                many=True,
                                                context={'request': request})
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)

    def get_queryset(self):
        queryset = User.objects.filter(
            subscription__subscriber_id=self.request.user.id)
        return queryset
