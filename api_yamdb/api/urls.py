from django.urls import include, path
from rest_framework.routers import DefaultRouter

import api.views

api_router = DefaultRouter()
api_router.register('categories', api.views.CategoryViewSet,
                    basename='categories')
api_router.register('genres', api.views.GenreViewSet,
                    basename='genres')
api_router.register('titles', api.views.TitleViewSet,
                    basename='titles')
api_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    api.views.ReviewViewSet,
    basename='reviews_v1'
)
api_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    api.views.CommentViewSet,
    basename='comments_v1'
)

app_name = 'api'
urlpatterns = [
    path('v1/', include(api_router.urls)),
    path('v1/auth/', include('users.urls', namespace='auth')),
    path('v1/users/', include('users.urls', namespace='users')),
]
