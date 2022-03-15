from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, create_token, register_user

app_name = 'users'

router = DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('signup/',
         register_user,
         name='register_user'),

    path('token/',
         create_token,
         name='token_obtain'),

    path('', include(router.urls)),
]
