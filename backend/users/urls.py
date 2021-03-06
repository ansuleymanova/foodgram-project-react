from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
    path('users/<user_id>/subscribe/',
         views.subscribe,
         name='subscribe'),
    path('', include(router.urls)),
]
