from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from user.models import User


class UserSerializer(ModelSerializer):
    id = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']


class LoginSerializers(serializers.Serializer):
    class Meta:
        model = User

        email = serializers.CharField(max_length=255)
        password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email and password:

            user = authenticate(username=email, password=password)
            if user:
                data['user'] = user

            data['user'] = user
        return data
