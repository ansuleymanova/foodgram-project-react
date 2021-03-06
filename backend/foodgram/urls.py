from django.contrib import admin
from django.urls import include, path

from users.views import SubscriptionList

urlpatterns = [
    path('api/users/subscriptions/', SubscriptionList.as_view()),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('djoser.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('recipes.urls')),
]

# schema_view = get_schema_view(
#    openapi.Info(
#        title="Foodgram API",
#        default_version='v1',
#        description="Документация для API проекта Foodgram",
#        # terms_of_service="URL страницы с пользовательским соглашением",
#        contact=openapi.Contact(email="suleymanova.dev@gmail.com"),
#        license=openapi.License(name="BSD License"),
#        ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

# urlpatterns += [
#   url(r'^swagger(?P<format>\.json|\.yaml)$',
#       schema_view.without_ui(cache_timeout=0), name='schema-json'),
#   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
#       name='schema-swagger-ui'),
#   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
#       name='schema-redoc'),
# ]
