from django.urls import path

from users import views

urlpatterns = [
    path('users/<user_id>/subscribe/',
         views.subscribe,
         name='subscribe'),
    path ('users/subscriptions/',
          views.subscriptions,
          name='subscriptions')
]
