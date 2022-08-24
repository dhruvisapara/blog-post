from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from blog.models import Blog, Comment, Image
from rest_framework.serializers import  SerializerMethodField

from user.models import User


class BlogSerializer(ModelSerializer):
    # id = serializers.ReadOnlyField(read_only=True)
    # user_name = serializers.CharField(source='user.username')

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'pub_date', 'description', 'highlights']

    def validate_author(self, user):
        if user != serializers.CurrentUserDefault():
            raise serializers.ValidationError(
                'You cant update other authors book'
            )


class CommentSerializer(ModelSerializer):
    id = serializers.ReadOnlyField(read_only=True)

    # def create(self, validated_data):
    #     import pdb
    #     pdb.set_trace()
    #     validated_data["comment"] = self.context["request"].user
    #     return super().create(validated_data)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'active']


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['post_image']

    # def create(self, validated_data):
    #     post_image = validated_data.pop('body')
    #     instance = super().create(validated_data)
    #     if post_image:
    #         instance.cars.add(*post_image)
    #     return instance


class UpdateSerializer(ModelSerializer):
    class Meta:
        model = Blog

        def update(self, validated_data):
            super(UpdateSerializer, self).update(validated_data)
