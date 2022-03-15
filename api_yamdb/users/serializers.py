from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import User

CUSTOM_ERR_TEXT = 'Name "me" is forbidden'
USERNAME_STOP_LIST = ('me',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate(self, attrs):
        if attrs.get('username', 'default').lower() in USERNAME_STOP_LIST:
            raise serializers.ValidationError(CUSTOM_ERR_TEXT)
        return attrs

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio',
                                          instance.bio)
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)
        if instance.is_admin:
            instance.role = validated_data.get('role',
                                               instance.role)
        instance.save()
        return instance


class AccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
                user,
                data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {"message": "confirmation_code is wrong"})
        return data
