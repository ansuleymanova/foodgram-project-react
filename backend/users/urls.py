from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('users/<user_id>/subscribe/',
         views.subscribe,
         name='subscribe'),
    path('users/subscriptions/',
         views.subscriptions,
         name='subscriptions'),
]