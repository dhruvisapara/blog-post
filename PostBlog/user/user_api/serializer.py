from django.contrib.auth import  get_user_model
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,SerializerMethodField

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from PostBlog.settings import EMAIL_HOST_USER
from user.models import User
# from user.user_api.task import send_confirmation_mail_task


class UserSerializer(ModelSerializer):
    """Serializers for User objects"""
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'auth_token')
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 5,
                                     'style': {
                                         'input_type': 'password'
                                     }}}

    def create(self, validated_data):
        """Create a new user with encrypter password"""
        user = get_user_model().objects.create_user(**validated_data)
        return user


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    # def create(self, validated_data):
    #     password = validated_data.pop['password', None]
    #     instance = self.Meta.model(validated_data)
    #
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #
    #     return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})
    #
    #     return attrs
    #
    # def validate_old_password(self, value,request):
    #     user = self.context['request'].user
    #     if not user.check_password(value):
    #         raise serializers.ValidationError({"old_password": "Old password is not correct"})
    #     return value
    #
    # def update(self, instance, validated_data):
    #
    #     instance.set_password(validated_data['password'])
    #     instance.save()
    #
    #     return instance