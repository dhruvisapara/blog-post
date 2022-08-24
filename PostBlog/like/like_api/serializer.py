from rest_framework.serializers import ModelSerializer

from like.models import Likes


class LikeSerializer(ModelSerializer):
    # id = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = Likes
        fields = ['like']