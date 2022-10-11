from django.contrib import auth

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from server.apps.accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'photo', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    photo = serializers.ImageField(read_only=True)
    password = serializers.CharField(max_length=68, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'access-token': user.get_tokens()['access-token'],
            'refresh-token': user.get_tokens()['refresh-token']
        }

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'photo', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = User.objects.filter(email=email).first()

        if user:
            if not user.is_active:
                raise AuthenticationFailed('Account disabled')

        user = auth.authenticate(username=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid user credentials")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled")

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'photo': user.photo,
            'email': user.email,
            'tokens': user.get_tokens()
        }


class UserSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'photo')


class PasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('password',)
