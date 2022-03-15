from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsUserIsAdmin
from .serializers import UserSerializer, AccessTokenSerializer


def send_confirm_code(emails: list,
                      conf_code: str) -> None:
    send_mail('YaMDb-confirmation code',
              f'Hello from Mars. Your confirmation code is "{conf_code}"!',
              settings.EMAIL_YAMDB_ADDRESS,
              emails,
              fail_silently=False,
              )


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register_user(request):
    data = request.data
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(username=data['username'],
                                    email=data['email'])
    token = default_token_generator.make_token(user)
    send_confirm_code([user.email, ], token)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def create_token(request):
    data = request.data
    serializer = AccessTokenSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    access_tok = AccessToken.for_user(request.user)
    return Response({"token": str(access_tok)})


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsUserIsAdmin)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated], url_path='me')
    def user_profile(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(request.user,
                                        data=request.data,
                                        partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
